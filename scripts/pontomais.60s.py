#!/usr/bin/env python3

import requests
from datetime import datetime, timedelta

#### CONFIG ####
# credentials
import sys
import os

# Try to find secrets in multiple locations:
# 1. In secrets/ directory relative to script (development)
# 2. In ~/.config/argos/secrets/ (deployed)
# 3. In ../secrets/ relative to script (alternative)
script_dir = os.path.dirname(os.path.abspath(__file__))
possible_paths = [
    os.path.join(script_dir, '..', 'secrets'),
    os.path.expanduser('~/.config/argos/secrets'),
    os.path.join(script_dir, 'secrets'),
]

for path in possible_paths:
    abs_path = os.path.abspath(path)
    if os.path.exists(abs_path):
        sys.path.insert(0, abs_path)
        break

from pontomais import email, client, access_token, employee_id

working_hours = timedelta(hours=8, minutes=0)
tolerance = timedelta(minutes=10)
balance_warning = timedelta(hours=4, minutes=0)
# aviso de limite de jornada (6h)
max_sequential = timedelta(hours=6, minutes=0)
# aviso de limite de horas extras (2h)
max_extra = timedelta(hours=2, minutes=0)
# tempo antes que o aviso é dado
warning_alarm = timedelta(minutes=30)
days_delta = 0 # Use 0 for today, 1 for yesterday, etc.
#### end CONFIG ####


# Function to extract clock-in times from the API response JSON
def extract_clock_in_times(response_json):
    clock_in_times = []
    work_days = response_json.get('work_days', [])

    for day in work_days:
        time_cards = day.get('time_cards', [])
        for time_card in time_cards:
            date = time_card.get('date')
            time = time_card.get('time')
            if date and time:
                datetime_str = f"{date} {time}"
                clock_in_times.append(datetime_str)

    return clock_in_times

# Function to calculate worked intervals between pairs of times
def calculate_intervals(times):
    intervals = []
    for i in range(0, len(times), 2):
        start_time = datetime.strptime(times[i], "%d/%m/%Y %H:%M")
        if i + 1 < len(times):
            end_time = datetime.strptime(times[i + 1], "%d/%m/%Y %H:%M")
        else:
            # If the number of times is odd, use the current time
            end_time = datetime.now()

        interval = end_time - start_time
        intervals.append(interval)

    return intervals

# Function to format timedelta to hh:mm
def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}"

# --- First API Call ---
url = "https://api.pontomais.com.br/api/time_cards/work_days/current"
today = datetime.today() - timedelta(days=days_delta)
params = {
    "start_date": f'{today.strftime("%Y-%m-%d")}',
    "end_date": f'{today.strftime("%Y-%m-%d")}',
    "attributes": "time_cards"
}
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Access-Token": access_token,
    "Api-Version": "2",
    "Cache-Control": "no-cache",
    "Client": client,
    "Content-Type": "application/json",
    "Origin": "https://app2.pontomais.com.br",
    "Referer": "https://app2.pontomais.com.br/",
    "Uid": email
}
response = requests.get(url, headers=headers, params=params)

# Extract clock-in times
times = extract_clock_in_times(response.json())

def get_time_balance_info(headers, employee_id, balance_warning):
    url2 = f"https://api.pontomais.com.br/api/employees/statuses/{employee_id}"
    headers2 = headers  # Reuse headers from the first request

    response2 = requests.get(url2, headers=headers2)
    balance_output = ""

    if response2.status_code == 200:
        data = response2.json()
        time_balance_seconds = data.get('statuses', {}).get('time_balance', 0)
        time_balance = timedelta(seconds=abs(time_balance_seconds))
        formatted_time_balance = format_timedelta(time_balance)
        balance_output += "\n---\n"

        if abs(time_balance) > balance_warning:
            balance_output += "⚠️  "

        if time_balance_seconds < 0:
            balance_output += f"Banco de Horas: <span color='#ff0000'>-{formatted_time_balance}</span>"  # Red for negative
        else:
            balance_output += f"Banco de Horas: <span color='#00ff00'>+{formatted_time_balance}</span>"  # Green for positive

        unsigned_mirrors = data.get('statuses', {}).get('unsigned_closing_mirrors_count', 0)
        if unsigned_mirrors > 0:
            balance_output += "\n---\n"
            balance_output += f"📑 Espelhos de Ponto Pendentes: {unsigned_mirrors}"
    else:
        balance_output += "\n---\n"
        balance_output += "Erro ao obter dados do banco de horas."
    return balance_output

output = ""
if len(times) == 0:
    title = "📭 Nenhum ponto registrado hoje\n"
    output += title
    output += "---\n"
else:
    start = datetime.strptime(times[0], "%d/%m/%Y %H:%M")

    working = False
    if len(times) % 2 != 0:
        working = True

    # Calculate intervals
    intervals = calculate_intervals(times)
    # Calculate total time
    total_time = sum(intervals, timedelta())

    # Format the output for Argos
    title = "⚒️ Em jornada\n"

    if total_time + tolerance < working_hours and not working:
        title = "💤 Intervalo\n"

    if total_time + tolerance >= working_hours and working:
        title = "⌚ Pode sair\n"

    if total_time + tolerance >= working_hours and not working:
        title = "✅ Done\n"

    if total_time >= working_hours + tolerance and working:
        title = "⚠️ Horas extras\n"

    remaining_extra_hours = working_hours + max_extra - total_time
    remaining_sequential_hours = max_sequential - intervals[-1]

    if remaining_extra_hours <= warning_alarm and working:
        title = "🚨 Atenção ao limite de horas extras!\n"

    if remaining_sequential_hours <= warning_alarm and working and remaining_sequential_hours < remaining_extra_hours:
        title = "🚨 Atenção ao limite de jornada!\n"

    output += title
    output += "---\n"
    for t in times:
        dt = t.split()
        output += f"{dt[1]} / "

    output += "\n---\n"
    output += f"Total: {format_timedelta(total_time)}"

    output += "\n---\n"
    if working_hours > total_time:
        missing = working_hours - total_time
        if missing > tolerance:
            output += f"Faltam: {format_timedelta(missing)}"
            output += "\n---\n"
            end = datetime.now() + missing
            # soma horário de almoço
            if len(times) < 3:
                end = start + working_hours + timedelta(hours=1)
            output += f"Fim do expediente: {end.strftime('%H:%M')}"
    else:
        exceding_hours = total_time - working_hours
        output += f"Extras: {format_timedelta(exceding_hours)}"

output += get_time_balance_info(headers, employee_id, balance_warning)

# Print the formatted output
print(output)

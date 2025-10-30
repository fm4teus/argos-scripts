#!/usr/bin/env python3

import requests
from datetime import datetime, timedelta

#### CONFIG ####
# credentials
from secrets import email, client, access_token, employee_id

working_hours = timedelta(hours=8, minutes=0)
tolerance = timedelta(minutes=10)
balance_warning = timedelta(hours=4, minutes=0)
# aviso de limite de jornada (6h)
max_sequential = timedelta(hours=6, minutes=0)
# aviso de limite de horas extras (2h)
max_extra = timedelta(hours=2, minutes=0)
# tempo antes que o aviso é dado
warning_alarm = timedelta(minutes=30)
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
params = {
    "start_date": f'{datetime.today().strftime("%Y-%m-%d")}',
    "end_date": f'{datetime.today().strftime("%Y-%m-%d")}',
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
if len(times) == 0:
    print("🚫 404")
    exit()
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

output = ""
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

# --- Second API Call ---
url2 = f"https://api.pontomais.com.br/api/employees/statuses/{employee_id}"
headers2 = headers  # Reuse headers from the first request

response2 = requests.get(url2, headers=headers2)

if response2.status_code == 200:
    data = response2.json()
    time_balance_seconds = data.get('statuses', {}).get('time_balance', 0)
    time_balance = timedelta(seconds=abs(time_balance_seconds))
    formatted_time_balance = format_timedelta(time_balance)
    output += "\n---\n"

    if abs(time_balance) > balance_warning:
        output += "⚠️  "

    if time_balance_seconds < 0:
        output += f"Banco de Horas: <span color='#ff0000'>-{formatted_time_balance}</span>"  # Red for negative
    else:
        output += f"Banco de Horas: <span color='#00ff00'>+{formatted_time_balance}</span>"  # Green for positive


    unsigned_mirrors = data.get('statuses', {}).get('unsigned_closing_mirrors_count', 0)
    if unsigned_mirrors > 0:
        output += "\n---\n"
        output += f"📑 Espelhos de Ponto Pendentes: {unsigned_mirrors}"
else:
    output += "\n---\n"
    output += "Erro ao obter dados do banco de horas."

# Print the formatted output
print(output)

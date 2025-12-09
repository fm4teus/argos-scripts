# Argos Scripts

Repositório centralizado para scripts do [Argos](https://github.com/p-e-w/argos), uma extensão do GNOME Shell que permite exibir informações personalizadas na top bar.

## Estrutura do Repositório

```
argos-scripts/
├── scripts/          # Scripts do Argos (arquivos .py ou .sh com intervalo no nome, ex: script.60s.py)
├── secrets/          # Arquivos de configuração e credenciais
│   ├── *.sample.py  # Arquivos de exemplo Python (não versionados)
│   ├── *.sample.sh  # Arquivos de exemplo Bash (não versionados)
│   └── *.py, *.sh   # Arquivos reais (adicionados ao .gitignore)
├── Justfile         # Comandos para deploy e gerenciamento
└── README.md        # Este arquivo
```

## Como Adicionar um Novo Script

1. **Crie o script** em `scripts/` com o padrão de nome do Argos:
   - Formato: `nome-do-script.INTERVALO.py` ou `nome-do-script.INTERVALO.sh` (ex: `meu-script.60s.py`)
   - O intervalo indica com que frequência o script será executado (60s = 60 segundos)

2. **Configure credenciais** (se necessário):
   - Para scripts Python: Crie `secrets/nome-do-script.sample.py` com as variáveis necessárias
   - Para scripts Bash: Crie `secrets/nome-do-script.sample.sh` com as variáveis necessárias
   - Copie o arquivo `.sample.*` para o mesmo nome sem `.sample` e preencha com suas credenciais
   - Os arquivos reais (sem `.sample`) serão ignorados pelo git

3. **Atualize o script para ler configuração**:
   - **Python:** Use imports do diretório secrets (veja exemplo no script `pontomais.60s.py`)
   - **Bash:** Use `source` para carregar o arquivo de configuração (veja exemplo no script `bluetooth-battery.60s.sh`)

4. **Documente o script**:
   - Adicione uma seção neste README explicando o que o script faz
   - Inclua instruções de configuração específicas

## Deploy

### Deploy de Todos os Scripts

```bash
just deploy
```

Este comando copia todos os scripts de `scripts/` para `~/.config/argos/`.

### Deploy de um Script Específico

```bash
just deploy-script nome-do-script.60s.py
```

### Listar Scripts Disponíveis

```bash
just list
```

### Tornar Scripts Executáveis

Após o deploy, torne os scripts executáveis:

```bash
chmod +x ~/.config/argos/*.{py,sh}
```

## Scripts Disponíveis

### Pontomais

Script para buscar dados da API do Pontomais e exibir informações relevantes sobre a jornada de trabalho na top bar.

#### Configuração

**Credenciais:**

As credenciais devem ser configuradas no arquivo `secrets/pontomais.py`. Um arquivo `secrets/pontomais.sample.py` é fornecido como exemplo. Copie `secrets/pontomais.sample.py` para `secrets/pontomais.py` e preencha suas credenciais:

```python
# secrets/pontomais.py
email = ""  # Use seu email real
client = ""  # Use seu client ID real
access_token = ""  # Use seu access token real
employee_id = ""  # Use seu employee ID real
days_delta = 0 # Use 0 para hoje, 1 para ontem, etc.
```

Para encontrar suas credenciais, acesse o Pontomais e copie-as dos "request headers" na aba "network" das ferramentas de desenvolvedor do seu navegador.

**Variáveis de Configuração:**

As demais variáveis de configuração estão no topo do script `scripts/pontomais.60s.py`:

```python
working_hours = timedelta(hours=8, minutes=0)
tolerance = timedelta(minutes=10)
balance_warning = timedelta(hours=4, minutes=0)
# aviso de limite de jornada (6h)
max_sequential = timedelta(hours=6, minutes=0)
# aviso de limite de horas extras (2h)
max_extra = timedelta(hours=2, minutes=0)
# tempo antes que o aviso é dado
warning_alarm = timedelta(minutes=30)
```

#### Instalação

1. **Instale as dependências:** Certifique-se de ter o Python e as bibliotecas necessárias instaladas (`requests`).
2. **Configure suas credenciais:** Preencha o arquivo `secrets/pontomais.py` com suas informações.
3. **Deploy:** Utilize o `Justfile` para copiar o script:
   ```bash
   just deploy-script pontomais.60s.py
   ```
4. **Torne o script executável:**
   ```bash
   chmod +x ~/.config/argos/pontomais.60s.py
   ```

#### Exemplos

##### Alerta de limite de horas
![pontolimit](https://github.com/fm4teus/argos-scripts/assets/55215503/55d00b05-725b-4559-94c9-67e0587757b8)

##### Em intervalo
![pontolunch](https://github.com/fm4teus/argos-scripts/assets/55215503/817925fb-c226-480a-aad7-3b9e5978bab8)

##### Dia finalizado
![pontodone](https://github.com/fm4teus/argos-scripts/assets/55215503/0f32b601-1e44-4257-bf7c-ce2947c5c1ca)

##### Em jornada
![ponto1](https://github.com/fm4teus/argos-scripts/assets/55215503/2f54530f-83af-4e19-897e-3c2becd97f3e)

##### Saldo de banco de horas e aviso de espelhos de ponto pendentes
![image](https://github.com/user-attachments/assets/31fd8ba3-55f0-4afe-9817-5246f8d05703)

### Bluetooth Battery

Script para monitorar a bateria de dispositivos Bluetooth conectados e exibir o nível de bateria na top bar com uma barra visual colorida.

#### Configuração

**MAC Address do Dispositivo:**

O endereço MAC do dispositivo Bluetooth deve ser configurado no arquivo `secrets/bluetooth-battery.sh`. Um arquivo `secrets/bluetooth-battery.sample.sh` é fornecido como exemplo. Copie `secrets/bluetooth-battery.sample.sh` para `secrets/bluetooth-battery.sh` e preencha o MAC address:

```bash
# secrets/bluetooth-battery.sh
BLUETOOTH_MAC="F8:AB:..."
```

Para encontrar o MAC address do seu dispositivo Bluetooth, use:

```bash
bluetoothctl devices
```

Ou conecte o dispositivo e use:

```bash
bluetoothctl info
```

#### Funcionalidades

- Exibe o nível de bateria em porcentagem
- Barra visual com 10 níveis (█ preenchido, ░ vazio)
- Cores dinâmicas baseadas no nível:
  - 🔴 Vermelho: ≤ 20%
  - 🟡 Amarelo: ≤ 50%
  - 🟢 Verde: > 50%
- Mostra 🔴 quando o dispositivo não está conectado ou não fornece informação de bateria

#### Instalação

1. **Dependências:** Certifique-se de ter `bluetoothctl` instalado (geralmente incluído no `bluez`).
2. **Configure o MAC address:** Preencha o arquivo `secrets/bluetooth-battery.sh` com o MAC address do seu dispositivo.
3. **Deploy:** Utilize o `Justfile` para copiar o script:
   ```bash
   just deploy-script bluetooth-battery.60s.sh
   ```
4. **Torne o script executável:**
   ```bash
   chmod +x ~/.config/argos/bluetooth-battery.60s.sh
   ```

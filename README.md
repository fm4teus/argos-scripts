## Pontomais
script para fetch dos dados da API do pontomais e exibir informações relevantes sobre a jornada de trabalho na top bar

## Configuração

### Credenciais
As credenciais agora devem ser configuradas no arquivo `secrets.py`. Um arquivo `secrets.sample.py` é fornecido como exemplo. Copie `secrets.sample.py` para `secrets.py` e preencha suas credenciais:

```python
# secrets.py
email = ""  # Use seu email real
client = ""  # Use seu client ID real
access_token = ""  # Use seu access token real
employee_id = ""  # Use seu employee ID real
days_delta = 0 # Use 0 para hoje, 1 para ontem, etc.
```

Para encontrar suas credenciais, acesse o Pontomais e copie-as dos "request headers" na aba "network" das ferramentas de desenvolvedor do seu navegador.

### Variáveis de Configuração
As demais variáveis de configuração estão no topo do script `pontomais.60s.py`:

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

### Instalação e Deploy

1.  **Instale as dependências:** Certifique-se de ter o Python e as bibliotecas necessárias instaladas (`requests`).
2.  **Configure suas credenciais:** Preencha o arquivo `secrets.py` com suas informações.
3.  **Deploy com Just:** Utilize o `Justfile` para copiar o script para o diretório correto:
    ```bash
    just deploy
    ```
    Este comando criará o diretório `~/.config/argos/` se ele não existir e copiará o `pontomais.60s.py` para lá.
4.  **Torne o script executável:**
    ```bash
    chmod +x ~/.config/argos/pontomais.60s.py
    ```


## Exemplos
### alerta de limite de horas
![pontolimit](https://github.com/fm4teus/argos-scripts/assets/55215503/55d00b05-725b-4559-94c9-67e0587757b8)
### em intervalo
![pontolunch](https://github.com/fm4teus/argos-scripts/assets/55215503/817925fb-c226-480a-aad7-7b9e5978bab8)
### dia finalizado
![pontodone](https://github.com/fm4teus/argos-scripts/assets/55215503/0f32b601-1e44-4257-bf7c-ce2947c5c1ca)
### em jornada
![ponto1](https://github.com/fm4teus/argos-scripts/assets/55215503/2f54530f-83af-4e19-897e-3c2becd97f3e)
### saldo de banco de horas e aviso de espelhos de ponto pendentes
![image](https://github.com/user-attachments/assets/31fd8ba3-55f0-4afe-9817-5246f8d05703)
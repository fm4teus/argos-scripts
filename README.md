## Pontomais
script para fetch dos dados da API do pontomais e exibir informações relevantes sobre a jornada de trabalho na top bar

## config
Preencher variáveis do topo do script com as credenciais. Pra achar elas é só acessar o pontomais e copiar dos request headers na aba network das dev tools do seu navegador.
```python
#### CONFIG ####
# credentials
email = ""  # Use your actual email
client = ""  # Use your actual client ID
access_token = ""  # Use your actual access token
employee_id = ""  # Use your actual employee ID

# aviso de limite de jornada (6h)
limit = timedelta(hours=5, minutes=30)
working_hours = timedelta(hours=8, minutes=0)
tolerance = timedelta(minutes=10)
balance_warning = timedelta(hours=4, minutes=0)
#### end CONFIG ####
```

depois é só conferir a instalação do python e das libs, colar na pasta `~/.config/argos` e mandar um `chmod +x pontomais.60s.py`


## exemplos
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


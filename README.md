## Pontomais
script para fetch dos dados da API do pontomais e exibir informações relevantes sobre a jornada de trabalho na top bar

## config
Preencher variáveis do topo do script com as credenciais. Pra achar elas é só acessar o pontomais e copiar dos request headers na aba network das dev tools do seu navegador.
```python
#### CONFIG ####
# credentials
email = ""
client = ""
access_token = ""

# aviso de limite de jornada (6h)
limit = timedelta(hours=5,minutes=30)
working_hours = timedelta(hours=8)
tolerance=timedelta(minutes=10)
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

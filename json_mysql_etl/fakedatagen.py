import random
import uuid
import json
from datetime import datetime
# Inicializando ..
## DEFININDO ARQUIVO
jsonfile = "/home/sding/mysql/json/calls-"+datetime.today().strftime("%Y-%m-%d")+".json"

def generate_data(records,filename):    
    jsondata = []
    for n in range(records):
        data = {
        "id":                random.getrandbits(32),
        "tipo_midia":        random.choice(["WEB", "PHONE"]),
        "user_id":           random.choice(["1", "2"]),
        "customer_id":       random.choice(["1", "2", "3"]),
        "call_type":         random.choice(random.choices(["INBOUND", "OUTBOUND", "UNKNOWN"], weights=(80, 19.9, 0.1), k=1)),
        "project_name":      random.choice(["ATENDIMENTO_HOSP_A", "ATENDIMENTO_HOSP_B", "ATENDIMENTO_CLINICA_A", "ATENDIMENTO_CLINICA_B"]),
        "status_atendimento":random.choice(random.choices(["EM_ATENDIMENTO", "FINALIZADO_SUCESSO", "FINALIZADO_ERRO", "ERROR"], weights=(1, 98.8, 0.1, 0.1), k=1)),
        "protocolo":         str(uuid.uuid4()),
        "segundos_ligacao":  random.randint(60, 10800),
        "created_at":        str(datetime.now()),
        "updated_at":        None
        }
        jsondata.append(data)

    with open(filename, "w") as file:
        json.dump(jsondata, file)

generate_data(10000,jsonfile)

import json
import mysql.connector 
import logging as logger
from datetime import datetime
import os

logger.basicConfig(
    format="%(asctime)s (%(levelname)s) %(message)s", 
    datefmt="[%Y-%m-%d %H:%M:%S]", 
    level=logger.DEBUG
)
jsonfile = "/home/sding/mysql/json/calls-"+datetime.today().strftime("%Y-%m-%d")+".json"

if not os.path.exists(jsonfile):
    logger.info(f"Today's json file not exists, check: {jsonfile}")
    exit()

finalData = []
rows = totalrows = 0


def insertdb(finalData):
    query = """
        INSERT INTO tb_call (
            midia_id, 
            user_id, 
            customer_id, 
            tipo_id, 
            project_id, 
            status_id, 
            nm_protocol, 
            qtd_minutos_call, 
            created_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    conn = mysql.connector.connect(user="root", 
                                password="123123",
                                host="localhost",
                                database="brunow")
    conn.autocommit = False
    cursor = conn.cursor()
    try:
        cursor.executemany(query, finalData)
        conn.commit()
        logger.info(str(cursor.rowcount)+" registros inseridos...")
    except Exception as e:
        logger.error(e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            logger.debug("Removendo instancia da Database... OK")

with open(jsonfile,'r') as file:
    for readline in file.readlines():
        for line in json.loads(readline):
            tData = {};
#            tData["id"]               = int(line["id"])
            tData["midia_id"]         = 1 if line["tipo_midia"] == "WEB" else 2
            tData["user_id"]          = int(line["user_id"])
            tData["customer_id"]      = int(line["customer_id"])
            if (line["call_type"] == "INBOUND"):
                tData["tipo_id"] = 1
            elif (line["call_type"] == "OUTBOUND"):
                tData["tipo_id"] = 2
            else:
                tData["tipo_id"] = 3
            if (line["project_name"] == "ATENDIMENTO_HOSP_A"):
                tData["project_id"] = 1
            elif (line["project_name"] == "ATENDIMENTO_HOSP_B"):
                tData["project_id"] = 2
            elif (line["project_name"] == "ATENDIMENTO_CLINICA_A"):
                tData["project_id"] = 2
            else:
                tData["project_id"] = 4
            if (line["status_atendimento"] == "EM_ATENDIMENTO"):
                tData["status_id"] = 1
                line["segundos_ligacao"] = None
            elif (line["status_atendimento"] == "FINALIZADO_SUCESSO"):
                tData["status_id"] = 2
            elif (line["status_atendimento"] == "FINALIZADO_ERRO"):
                tData["status_id"] = 2
            else:
                tData["status_id"] = 4
                line["segundos_ligacao"] = None
            tData["nm_protocol"]      = str(line["protocolo"])
            tData["qtd_minutos_call"] = int(round(line["segundos_ligacao"]) / 60) if line["segundos_ligacao"] != None else None # minutos
            tData["created_at"]       = line["created_at"]
            
            finalData.append(tuple(tData.values()))
            rows += 1
        
            if rows >= 1000:
                insertdb(finalData)
                totalrows += rows
                print(f'{totalrows} rows inserted')
                rows = 0
                finalData = []

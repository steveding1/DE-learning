from datetime import timedelta,datetime
from airflow.models import DAG
from taskgrp import taskgrp1,taskgrp2

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
with DAG(
    dag_id="modularized_dag",
    schedule_interval="@once",
    start_date=datetime(2021, 1, 1),
    default_args=default_args,
    catchup=False,
    tags=['mylearn1'],
) as dag:
    dataproc = taskgrp1(dag=dag)
    message = taskgrp2(dag=dag)
    dataproc >> message
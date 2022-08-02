from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.decorators import dag
from datetime import datetime

@dag(schedule_interval=None, 
start_date=datetime(2021, 1, 1), 
catchup=False,
tags=['mylearn'])
def myfunc():
    trigtask = TriggerDagRunOperator(
        task_id='trigger_bash',
        trigger_dag_id='bash_test',
        wait_for_completion=True
    )

    trigtask

dagname = myfunc()
from datetime import timedelta,datetime
from airflow.models import DAG
from airflow.utils.task_group import TaskGroup
from airflow.operators.bash import BashOperator

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
    with TaskGroup('dataprocesses') as tg1:

        dataproc1 = BashOperator(
            task_id="datatask1",
            bash_command='echo data_cleaning',
            dag=dag,
        )

        dataproc2 = BashOperator(
            task_id="datatask2",
            bash_command='echo send_to_DB', 
            retries=3,
            dag=dag,
        )

        dataproc1 >> dataproc2

    with TaskGroup('sendmessages') as tg2:

        messagetask1 = BashOperator(
            task_id="sendemail",
            bash_command='echo send email',
            dag=dag
        )

        messagetask2 = BashOperator(
            task_id="sendeslack",
            bash_command='echo to slack', 
            retries=3,
            dag=dag
        )

        messagetask1 >> messagetask2
        
    tg1 >> tg2
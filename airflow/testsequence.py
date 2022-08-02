from datetime import datetime,timedelta
from textwrap import dedent
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.helpers import chain


with DAG(
    'testsequ',
    default_args={
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'provide_context': True,
    
    # 'wait_for_downstream': False,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    },
    description='test parallel running',
    schedule_interval=timedelta(days=1),
    max_active_runs=3,
    concurrency=1,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['mylearn1'],
) as dag:
    task1 = BashOperator(
        task_id='date_sleep1',
        bash_command='/home/sding/airflow/scripts/date_sleep1.sh '
    )
    
    task2 = BashOperator(
        task_id='date_sleep10',
        bash_command='/home/sding/airflow/scripts/date_sleep10.sh '
    )
    
    task3 = BashOperator(
        task_id='date_sleep5',
        bash_command="""
        echo Start of schedule interval {{ data_interval_start }};
        sh /home/sding/airflow/scripts/date_sleep5.sh; 
        """
    )

[task1,task2,task3]
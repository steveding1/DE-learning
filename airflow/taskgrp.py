from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup

def taskgrp1(dag):
    taskgroup1 = TaskGroup(group_id='dataprocesses')

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
    return taskgroup1

def taskgrp2(dag):
    taskgroup2 = TaskGroup(group_id='message')

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
    return taskgroup2

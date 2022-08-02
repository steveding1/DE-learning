from random import choice
import pendulum
from airflow import DAG
from airflow.operators.python import BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.dummy import DummyOperator
from airflow.utils.edgemodifier import Label


start_date = pendulum.datetime(2021, 1, 1, tz="UTC")
options = ['br1','br2','br3','br4']

def _branch():
    accuracy = 4
    if accuracy > 5:
        return 'accurate'
    return ['inaccurate','super_accurate']

with DAG(
    dag_id="BranchPythontest",
    start_date=start_date,
    catchup=False,
    schedule_interval=None,
    tags=['mylearn1'],
) as mydag:
    run_this_first = DummyOperator(
        task_id='run_this_first',
    )

    task1 = BranchPythonOperator(
        task_id="logic_task",
        python_callable=_branch,
    )

    last = BashOperator(
        task_id = 'join',
        bash_command = '/home/sding/airflow/scripts/date_sleep1.sh ',
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )

    accurate = DummyOperator(
    task_id='accurate'
    )
    inaccurate = DummyOperator(
    task_id='inaccurate')

    super_accurate = DummyOperator(
    task_id='super_accurate')

    task1 >> [accurate, inaccurate,super_accurate] >> last
from h11 import Data
import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.exceptions import AirflowException
from airflow.decorators import task
from airflow.utils.trigger_rule import TriggerRule

start_date = pendulum.datetime(2022, 8, 1, tz="UTC")
@task(trigger_rule=TriggerRule.ONE_FAILED, retries=0)
def watcher():
    raise AirflowException('one or more upsteam tasks failed.')

with DAG(
    dag_id='watcher_test',
    start_date=start_date,
    schedule_interval='@hourly',
    catchup=False,
    tags=['mylearn1'],
)as dag:
    failing_task = BashOperator(task_id='failing',bash_command='exit 1',retries=0)
    passing_task = BashOperator(task_id='passing',bash_command='echo succeed',retries=0)
    teardown = BashOperator(
        task_id='teardown',
        bash_command='echo teardown',
        trigger_rule=TriggerRule.ALL_DONE
    )

    failing_task >> passing_task >> teardown
    list(dag.tasks) >> watcher()
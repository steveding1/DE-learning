from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
import pendulum

@dag(
    dag_id="decorator_test",
    schedule_interval=None,
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    tags=['mylearn1','test'],
)

def myfunc():
    task1 = BashOperator(
        task_id='hello',
        bash_command='echo hello >> /home/sding/airflow/scripts/hello.txt '
    )
    task2 = BashOperator(
        task_id='sleep1',
        bash_command='/home/sding/airflow/scripts/date_sleep1.sh >> /home/sding/airflow/scripts/hello.txt '
    )
    @task
    def printworld():
        with open('/home/sding/airflow/scripts/hello.txt', 'a') as f:
            f.write('world\n')

    task1>>task2>>printworld()

dag = myfunc()
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow import DAG
import pendulum

with DAG(
    dag_id="bash_test",
    schedule_interval=None,
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    tags=['mylearn','test']
) as dag:

    file_exist = FileSensor(
                    task_id="file_sensor_task_id",
                    filepath="/home/sding/nytaxi/csv/new/*.csv",
                    #fs_conn_id="fs_default" # default one, commented because not needed
                    poke_interval= 20,
                    mode="reschedule",
                    timeout=10,
                    dag=dag
                )

    mv_csv = BashOperator(
        task_id='mv_to_import',
        bash_command='mv /home/sding/nytaxi/csv/new/*.csv /home/sding/nytaxi/csv/import'
    )#mv /home/sding/nytaxi/csv/import/*.csv /home/sding/nytaxi/csv/new

file_exist >> mv_csv
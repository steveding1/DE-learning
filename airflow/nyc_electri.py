from airflow.models import DAG
from airflow.operators.python import PythonOperator
import pendulum
from util import downld_electr,downld_weather

def on_failure_callback(context):
    dag_run = context.get('dag_run')
    task_instances = dag_run.get_task_instances()
    print(task_instances)

with DAG(
    dag_id="nyc_weather_vs_ele",
    description="provide visulizations for NYC electricity comumption vs weather conditions (hourly)",
    schedule_interval='0 12 * * *',
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    tags=['mylearn1'],
#    default_view='gantt',
    orientation = 'TB',
    on_failure_callback=on_failure_callback,
    max_active_runs = 3
) as dag:

    weather_csv = PythonOperator(
        task_id = 'weather_csv',
        python_callable = downld_weather,
        dag=dag,
    )
    electr_csv = PythonOperator(
        task_id = 'electr_csv',
        python_callable = downld_electr,
        dag=dag,
    )

[weather_csv, electr_csv]
from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator
from airflow.operators.python import PythonOperator
import pendulum

def load_csv():
    import pandas as pd
    from sqlalchemy import create_engine
    from time import perf_counter

    if_exists = "replace"
    engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
    for df in pd.read_csv('/home/sding/nytaxi/tripdata.csv',chunksize=100000):
        start = perf_counter()
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.to_sql('trips', con=engine, if_exists=if_exists)
        print('insert rows using',perf_counter()-start,'seconds')
        if_exists = "append"

    print(
        'checking rows in the table:',
        pd.read_sql('select count(*) from trips',con=engine).count
    )

with DAG(
    dag_id="csv_to_postgr",
    schedule_interval=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=['mylearn']
) as dag:

    virtualenv_task = PythonVirtualenvOperator(
        task_id="virtualenv_task", 
        python_callable=load_csv,
        requirements=["pandas==1.4.2", "sqlalchemy", "psycopg2"], 
        system_site_packages=False,
        dag=dag
)


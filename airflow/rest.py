from airflow.models import DAG
from airflow.operators.python import PythonOperator
import pendulum

def get(url: str) -> None:
    from datetime import datetime
    import requests
    import json
    endpoint = url.split('/')[-1]
    now = datetime.now()
    now = f"{now.year}-{now.month}-{now.day}T{now.hour}-{now.minute}-{now.second}"
    response = requests.get(url)
    jsn = json.loads(response.text)
    path = '/home/sding/airflow/csvfiles/json/'
    with open(path+now+endpoint+'.json', 'w') as file:
      json.dump(jsn,file)

with DAG(
    dag_id="rest_parall",
    description="test",
    schedule_interval='0 12 * * *',
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    tags=['mylearn1'],
    default_view='gantt',
    orientation = 'TB',
    max_active_runs = 4
) as dag:
    urls = ['https://gorest.co.in/public/v2/users',
    'https://gorest.co.in/public/v2/posts',
    'https://gorest.co.in/public/v2/comments',
    'https://gorest.co.in/public/v2/todos']

    for i,url in enumerate(urls):
         getloop = PythonOperator(
            task_id='get_'+url.split('/')[-1],
            python_callable=get,
            op_kwargs={'url': url},
            retries=2,
        )

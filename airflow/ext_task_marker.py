import pendulum
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.sensors.external_task import ExternalTaskMarker, ExternalTaskSensor
from airflow.operators.python import PythonOperator

start_date = pendulum.datetime(2022, 8, 1, tz="UTC")

with DAG(
    dag_id="example_external_task_marker_parent",
    start_date=start_date,
    catchup=False,
    schedule_interval='*/1 * * * *',
    tags=['mylearn1'],
) as parent_dag:
    # [START howto_operator_external_task_marker]
    import time
    parent_task = ExternalTaskMarker(
        task_id="parent_task",
        external_dag_id="example_external_task_marker_child",
        external_task_id="child_task1",
    )
    # [END howto_operator_external_task_marker]
    parent_py_task = PythonOperator(
        task_id="parent_py_task",
        python_callable=lambda:time.sleep(14),
    )
    parent_py_task >> parent_task

with DAG(
    dag_id="example_external_task_marker_child",
    start_date=start_date,
    schedule_interval='*/1 * * * *',
    catchup=False,
    tags=['mylearn1'],
) as child_dag:
    # [START howto_operator_external_task_sensor]
    child_task1 = ExternalTaskSensor(
        task_id="child_task1",
        external_dag_id=parent_dag.dag_id,
        external_task_id=parent_task.task_id,
        timeout=600,
        allowed_states=['success'],
        failed_states=['failed', 'skipped'],
        mode="reschedule",
    )
    # [END howto_operator_external_task_sensor]
    child_task2 = DummyOperator(task_id="child_task2")
    child_task1 >> child_task2
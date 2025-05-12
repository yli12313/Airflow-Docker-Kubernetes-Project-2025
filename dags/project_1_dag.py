# Placeholder DAG. Working on dockerizing the app and deploying
# to Kubernetes first before coming back to the DAG.

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def print_hello():
    print("Hello from Airflow!")

with DAG(
    dag_id='my_dag',
    start_date=datetime(2025, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:
    task = PythonOperator(
        task_id='print_hello',
        python_callable=print_hello
    )

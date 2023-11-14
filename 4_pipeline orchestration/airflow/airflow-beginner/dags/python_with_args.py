from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
from py_modules import test

default_args ={
    'owner' : 'tharhtet',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}
with DAG(
    dag_id = "python_dag_v1",
    default_args=default_args,
    description="This is python dag testing",
    start_date=datetime(2023,11,14,2),
    schedule_interval='@daily'
) as dag:
    hello_task = PythonOperator(
        task_id = "greeting_task",
        python_callable = test.greeting
    )
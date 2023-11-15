from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import time

default_args ={
    'owner' : 'tharhtet',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

def greeting(some_dict,ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name') 
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    
    print("Hello : {}: ".format(first_name+" "+last_name))
    
    
    age = ti.xcom_pull(task_ids='get_age', key='age')
    print("I'm {} old ".format(age))

    
def get_name(ti):
    ti.xcom_push(key='first_name', value='Thar Htet')
    ti.xcom_push(key='last_name', value='San')


def get_age(ti):
    time.sleep(10)
    ti.xcom_push(key='age', value=19)

with DAG(
    dag_id = "python_operator_v1",
    default_args=default_args,
    description="This is python dag testing",
    start_date=datetime(2023,11,15),
    schedule_interval='@daily'
) as dag:
    hello_task = PythonOperator(
        task_id = 'greeting_task',
        python_callable=greeting,
        op_kwargs={'some_dict': {'a': 1, 'b': 2}}
    )

    get_age_task = PythonOperator(
        task_id = 'get_age',
        python_callable=get_age,
    )
    
    get_name_task = PythonOperator(
        task_id = 'get_name',
        python_callable=get_name,
    )

get_name_task >> hello_task
get_age_task >> hello_task
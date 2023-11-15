from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'tharhtet',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}


def greeting():
    print("hello tharhtet")

def greet(some_dict, ti):
    print("hello noob")
    print("some dict: ", some_dict)
    #first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    #last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    #age = ti.xcom_pull(task_ids='get_age', key='age')
    #print(f"Hello World! My name is {first_name} {last_name}, "
    #      f"and I am {age} years old!")

def get_name(ti):
    print("get_name work")
    #ti.xcom_push(key='first_name', value='Jerry')
    #ti.xcom_push(key='last_name', value='Fridman')

def get_age(ti):
    print("get_age work")
    #ti.xcom_push(key='age', value=19)



with DAG(
    default_args=default_args,
    dag_id='our_dag_with_python_operator_v04',
    description='Our first dag using python operator',
    start_date=datetime(2023, 11, 15,11),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greeting,
        #op_kwargs={'some_dict': {'a': 1, 'b': 2}}
    )
"""
    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )

    task3 = PythonOperator(
        task_id='get_age',
        python_callable=get_age
    )
    """

task1
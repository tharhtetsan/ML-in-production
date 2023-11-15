from datetime import datetime,timedelta
from airflow.decorators import dag,task
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'tharhtet',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}


@dag(
    dag_id = 'dag_with_taskflow_api_v01',
    default_args=default_args, 
    start_date=datetime(2023, 11, 15,11),
    schedule_interval='@daily'
)
def hello_world_etl():

    @task(multiple_outputs=True)
    def get_name():
        return {
            'first_name': 'Thar Htet',
            'last_name': 'San'
        }
    
    @task()
    def get_age():
        return 18
    
    @task()
    def greeting(first_name, last_name, age):
        print("Hello gg.....")
        print(f"Hello World! My name is {first_name} {last_name} "
              f"and I am {age} years old!")
        
    name_dict = get_name()
    age = get_age()
    greeting(first_name=name_dict['first_name'],last_name=name_dict['last_name'],
            age=age)
        
hello_world_etl()

**Airflow for beginner**


Airflow has some problems with python versions. so we need set some specific python version.
```bash
conda create --name airflow_env python=3.9 -y
conda activate airflow_env
pip install "apache-airflow==2.2.3" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.2.3/constraints-no-providers-3.9.txt"

```

Initial Airflow setup
```
export AIRFLOW_HOME=.
airflow db init
```

Create one user for login
```
airflow users create --username admin --firstname tharhtet --lastname san --role Admin --email tharhtet@ai.com
airflow webserver -p 5000 

```


### Airflow with docker
```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.7.3/docker-compose.yaml'

mkdir -p ./dags ./logs ./plugins ./config
docker-compose up airflow-init
docker-compose up
```

#### References
- [airflow-docker-reference](https://github.com/coder2j/airflow-docker/blob/main/docker-compose.yaml)



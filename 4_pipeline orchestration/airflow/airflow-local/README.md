
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
airflow webserver -p 8080 

```


```

```

#### References


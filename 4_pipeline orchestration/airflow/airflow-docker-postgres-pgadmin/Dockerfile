FROM puckel/docker-airflow

RUN pip install -U pip
RUN pip install pipenv

COPY .  .



RUN pipenv install --system --deploy

# initialize the database
RUN airflow initdb
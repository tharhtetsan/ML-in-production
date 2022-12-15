
FROM python:3.8


WORKDIR /app
COPY . /app

ENV GOOGLE_APPLICATION_CREDENTIALS=/app/secrets/serviceAccount.json


RUN pip3 install mlflow boto3 psycopg2-binary




#RUN mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri postgresql://DB_USER:DB_PASSWORD@DB_ENDPOINT:5432/DB_NAME --default-artifact-root s3://S3_BUCKET_NAME

ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--","/app/start.sh"]

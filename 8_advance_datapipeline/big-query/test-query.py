
import os
from google.cloud import bigquery

print("Service Account KEY:", os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

client = bigquery.Client()
query = """
    SELECT name, SUM(number) as total_people
    FROM `bigquery-public-data.usa_names.usa_1910_2013`
    WHERE state = 'TX'
    GROUP BY name, state
    ORDER BY total_people DESC
    LIMIT 20

"""
import time
start_time = time.time()
query_job = client.query(query)
print(time.time() - start_time)
print(type(query_job))
print(query_job)



# Run a Standard SQL query using the environment's default project
df = query_job.to_dataframe()


print("Top 20 USA Names:\n")
for row in query_job:
    print("name={}, count={}".format(row[0], row["total_people"]))

from google.cloud import bigquery
import time

client = bigquery.Client()

start = time.time()
query = """
    SELECT corpus AS title, COUNT(word) AS unique_words
    FROM `bigquery-public-data.samples.shakespeare`
    GROUP BY title
    ORDER BY unique_words
    DESC LIMIT 10
"""
results = client.query(query)
print(time.time() - start)


for row in results:
    title = row['title']
    unique_words = row['unique_words']
    print(f'{title:<20} | {unique_words}')


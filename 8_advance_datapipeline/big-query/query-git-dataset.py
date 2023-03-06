from google.cloud import bigquery

client = bigquery.Client()

query = """
    SELECT subject AS subject, COUNT(*) AS num_duplicates
    FROM bigquery-public-data.github_repos.commits
    GROUP BY subject
    ORDER BY num_duplicates
    DESC LIMIT 10
"""
results = client.query(query)

for row in results:
    subject = row['subject']
    num_duplicates = row['num_duplicates']
    print(f'{subject:<20} | {num_duplicates:>9,}')
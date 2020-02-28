import psycopg2
import re

conn = psycopg2.connect(host="lionscale.live",database="brandidb", user="brandiadmin", password="qnHQJT2FZpKG4KqV")
cur = conn.cursor()
cur.execute("SELECT * FROM education")
results = cur.fetchall()

for result in results:
    # lowercase the key
    key = result[1].lower()
    # replace all non-alphanumeric chars with _
    key = re.sub('[^a-z0-9]','_', key)
    print(f'{key} = "{result[0]}"')
cur.close()
conn.close()

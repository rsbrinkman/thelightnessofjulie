import csv

def query_db(query):
  conn = psycopg2.connect(host="localhost", database="light", user="postgres")
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute(query)
  results = cur.fetchall()
  res = [dict(record) for record in results]
  cur.close()
  conn.close()

  return res

def insert_db(query, query_params):
  conn = psycopg2.connect(host="localhost", database="performance", user="hireology")
  conn.autocommit = True
  cur = conn.cursor()
  cur.execute(query, query_params)

def read_settings():
  with open('settings.csv') as f:
    records = csv.DictReader(f)
    # Tacky - there should only every be one row. Famous Last Words.
    for row in records:
      return row

def write_settings(k, v):
  settings = read_settings()
  if k in settings:
    settings[k] = v

  with open('settings.csv', 'wb') as f:
    w = csv.DictWriter(f, settings.keys())
    w.writeheader()
    w.writerow(settings)


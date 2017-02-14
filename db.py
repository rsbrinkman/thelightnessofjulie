import psycopg2


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

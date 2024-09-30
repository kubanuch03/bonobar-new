import psycopg2
from multiprocessing import Pool

def connect_to_db(i):
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="postgres",
            dbname="bono_bar"
        )
        conn.close()
        return f"Connection {i} successful"
    except Exception as e:
        return f"Connection {i} failed: {e}"

if __name__ == "__main__":
    with Pool(10) as p:
        results = p.map(connect_to_db, range(100))
        for result in results:
            print(result)



'''
createdb -h 172.18.0.4 -p 5432 -U postgres test_db  
docker-compose exec db pgbench -h 172.18.0.4 -p 5432 -U postgres -i -s 10 test_db

'''
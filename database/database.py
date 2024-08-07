from mysql.connector.pooling import MySQLConnectionPool, CNX_POOL_MAXSIZE
import os
import dotenv

dotenv.load_dotenv()

dbconfig = {
    "host": "localhost",
    "database": "crispydogDB",
    "user": os.getenv("MYSQL_USERNAME"),
    "password": os.getenv("MYSQL_PASSWORD")
}

pool = MySQLConnectionPool(
    pool_name="my_pool",
    pool_size=CNX_POOL_MAXSIZE,
    **dbconfig
)
from mysql.connector.pooling import MySQLConnectionPool
import os
import dotenv

dotenv.load_dotenv()

dbconfig = {
    "host": os.getenv("MYSQL_HOST"),
    "database": "crispydogDB",
    "user": os.getenv("MYSQL_USERNAME"),
    "password": os.getenv("MYSQL_PASSWORD")
}

pool = MySQLConnectionPool(
    pool_name="my_pool",
    pool_size=32,
    **dbconfig
)
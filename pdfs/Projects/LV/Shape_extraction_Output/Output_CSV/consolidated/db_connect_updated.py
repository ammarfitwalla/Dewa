import mysql.connector
from mysql.connector import errorcode, ClientFlag


def fetch_from_madb():
    vals = {}
    config = {
        'host': 'gbm-db-2021.mysql.database.azure.com',
        'user': 'rashid',
        'password': 'Matrix@2021',
        'database': 'gbm',
        'client_flags': [ClientFlag.SSL],
        'ssl_ca': 'ssl/BaltimoreCyberTrustRoot.crt.pem'
    }

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gbm.object_repo_tbl;")
        for i in cursor.fetchall():
            vals[i[1]] = i[2]

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
            return None
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return None
        else:
            print(err)
            return None
    print("------------------------------------------------------")
    print(vals)
    print("------------------------------------------------------")
    return vals

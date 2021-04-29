import mysql.connector
from mysql.connector import errorcode, ClientFlag


def fetch_from_localdb():
    vals = {}
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'admin',
        'database': 'sld_db',
    }

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sld_db.sld_symbols;")
        for i in cursor.fetchall():
            # print(i)
            vals[i[0]] = i[2]

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


# fetch_from_localdb()
#this one is for automatic updates
import psycopg2  
import psycopg2.extras
import sys
con = None

try:
    connection = psycopg2.connect(user="postgres",  # same as pgAdmin
                                  password="",  # same as pgAdmin
                                  host="127.0.0.1",
                                  port="5432",
                                  database="PersonalManagement")  # same as the name of the 
                                                       # company database in pgAdmin

    cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)

    cursor.execute("SELECT * FROM groceries order by to_date(expirdate, 'MM/DD/YYYY') desc limit 10")
    row = cursor.fetchone()
    print("Food Best By Date Update")
    print("ID\t\tName\t\tExpiration Date\t\tNumber")
    print("---------------------------------------------------------")
    while row:
        print(row["itemid"], '\t\t', row["itemname"], '\t\t', row["expirdate"], '\t\t', row["numitems"], )
        row = cursor.fetchone()
                
except (Exception, psycopg2.Error) as error :    
    print ("Error while connecting to PostgreSQL", error)
    if connection:
        #reverses changes before commit
        connection.rollback()
    sys.exit(-1)

finally:
    if (connection):
        connection.close()
        print("PostgreSQL connection is closed")
input("Press Enter to exit...")

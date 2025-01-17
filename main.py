#add password and update other connection/database/table info accordingly
#read in new items
#remove items
#output upcoming dates
import psycopg2  
import psycopg2.extras
import sys
con = None

try:
    connection = psycopg2.connect(user="postgres",  # same as pgAdmin
                                  password="",  # same as pgAdmin
                                  host="127.0.0.1",
                                  port="5432",
                                  database="PersonalManagement")   
                                                       

    cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)
    '''
    cursor.execute("SELECT * FROM groceries")
    row = cursor.fetchone()
    while row:
        print(row["employee_id"], row["employee_phone"], row["employee_email"],)
        row = cursor.fetchone()
    '''
    """cursor.execute(""SELECT pname, dname, COUNT(*) AS emp, SUM(hours) AS total_hours FROM (project JOIN department ON dnum=dnumber) JOIN works_on ON pnumber=pno GROUP BY pname, dname"")
    print("Project\t\tDepartment\t#Emp\tTotal Hours")
    print("---------------------------------------------------------")
    row = cursor.fetchone()
    while row:
        print(row["pname"], row["dname"], row["emp"], row["total_hours"], sep="\t")
        #print(row)
        row = cursor.fetchone()

    # Print PostgreSQL Connection properties
    print(connection.get_dsn_parameters(), "\n")"""

    """# Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")"""




    choice = -1
    choice2 = -1
    errorBit = False
    name = "string"
    expirDate = "string"
    numItems = "string"
    print("Welcome to grocery mangement!")
    while(choice != 0):
        choice = int(input("\nSelect option\n0 to exit\n1 to add items\n2 to remove items\n3 to see the next ten items to expire\n4 to see all items\n"))
        #add items
        if(choice == 1):
            while (choice2 != 0):
                choice2 = int(input("\nSelect option\n0 to go back\n1 to start\n"))
                if(choice2 == 1):
                    name = input("\nName of item: ")
                    expirDate = input("\nWhen it expires(mm/dd/yyyy): ")
                    numItems = int(input("\nNumber of that item:"))
                    cursor.execute('select max(itemid) from groceries;')
                    fetchTuple = cursor.fetchone()
                    if(len(fetchTuple) == 0): 
                        HiId = 0
                    else:
                        HiId = int(fetchTuple[0])+1
                    new_contracts = (HiId, name, expirDate, numItems)
                    insert_string = "INSERT INTO groceries(itemid, itemname, expirdate, numitems) VALUES(%s, %s, %s, %s);"
                    
                    cursor.execute(insert_string, new_contracts)
                    connection.commit()
                    
                    print("\nItem Added")
            choice2 = -1
        #remove items
        if(choice == 2):
            while (choice2 != 0):
                choice2 = int(input("\nSelect option\n0 to go back\n1 to lookup by due date\n2 to remove by id\n"))
                if(choice2 == 1):
                    expirDate = input("\nBest by Date: \n")
                    selectString = "Select * from groceries where expirdate = %s"
                    cursor.execute(selectString, expirDate)
                    #connection.commit()
                #remove by id
                if(choice2 == 2):
                    itemId = input("Item ID: ")
                    cursor.execute("Select numitems from groceries where itemid = %s", itemId)
                    numberofItems = cursor.fetchone()[0]
                    if numberofItems > 1:
                        cursor.execute("update groceries set numitems = %s where itemid = %s", numberofItems-1, itemId)
                    else:
                        deleteString = "delete from groceries where itemid = %s"
                        cursor.execute(deleteString, itemId)
                    connection.commit()
            choice2 = -1
        if(choice == 3):
            cursor.execute("SELECT * FROM groceries order by to_date(expirdate, 'MM/DD/YYYY') desc limit 10")
            row = cursor.fetchone()
            print("ID\t\tName\t\tExpiration Date\t\tNumber")
            print("---------------------------------------------------------")
            while row:
                print(row["itemid"], '\t\t', row["itemname"], '\t\t', row["expirdate"], '\t\t', row["numitems"], )
                row = cursor.fetchone()
        if(choice == 4):
            cursor.execute("SELECT * FROM groceries order by to_date(expirdate, 'MM/DD/YYYY') desc")
            row = cursor.fetchone()
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

# manage_reservations.py
# CSC 370 - Summer 2020 - Assignment 6
#
#
# Jordan Watson - 08/01/2020

import sys, csv, psycopg2

if len(sys.argv) < 2:
    print("Usage: %s <input file>"%sys.argv[0],file=sys.stderr)
    sys.exit(1)
    
input_filename = sys.argv[1]

# Open your DB connection here
psql_user = 'jordanwatson1'
psql_db = 'jordanwatson1'
psql_password = 'p1n3appl3'
psql_server = 'studdb1.csc.uvic.ca'
psql_port = 5432

conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)

cursor = conn.cursor()

cursor.execute("start transaction;")
cursor.execute("set constraints all deferred;")

with open(input_filename) as f:
    for row in csv.reader(f):
        if len(row) == 0:
            continue #Ignore blank rows
        if len(row) != 4:
            print("Error: Invalid input line \"%s\""%(','.join(row)), file=sys.stderr)
            #Maybe abort the active transaction and roll back at this point?
            conn.rollback()
            break
        action,flight_id,passenger_id,passenger_name = row
        
        if action.upper() not in ('CREATE','DELETE'):
            print("Error: Invalid input line \"%s\""%(','.join(row)), file=sys.stderr)
            #Maybe abort the active transaction and roll back at this point?
            conn.rollback()
            break
        #Do something with the data here
        #Make `sure to catch any exceptions that occur and roll back the transaction if a database error occurs.
        try:
            if action.upper() == 'CREATE':
                cursor.execute("insert into passengers values(%s, %s);",(passenger_id, passenger_name))
                cursor.execute("insert into reservations values(%s, %s);",(flight_id, passenger_id))
            else:
                cursor.execute("delete from reservations where passenger_ID = %s and flight_ID_num = %s;", (passenger_id, flight_id))
        except psycopg2.ProgrammingError as err:
            #ProgrammingError is thrown when the database error is related to the format of the query (e.g. syntax error)
            print("Caught a ProgrammingError:",file=sys.stderr)
            print(err,file=sys.stderr)
            conn.rollback()
        except psycopg2.IntegrityError as err:
            #IntegrityError occurs when a constraint (primary key, foreign key, check constraint or trigger constraint) is violated.
            print("Caught an IntegrityError:",file=sys.stderr)
            print(err,file=sys.stderr)
            conn.rollback()
        except psycopg2.InternalError as err:
            #InternalError generally represents a legitimate connection error, but may occur in conjunction with user defined functions.
            #In particular, InternalError occurs if you attempt to continue using a cursor object after the transaction has been aborted.
            #(To reset the connection, run conn.rollback() and conn.reset(), then make a new cursor)
            print("Caught an IntegrityError:",file=sys.stderr)
            print(err,file=sys.stderr)
            conn.rollback()
try:
    conn.commit()
except psycopg2.ProgrammingError as err:
    #ProgrammingError is thrown when the database error is related to the format of the query (e.g. syntax error)
    print("Caught a ProgrammingError:",file=sys.stderr)
    print(err,file=sys.stderr)
    conn.rollback()
except psycopg2.IntegrityError as err:
    #IntegrityError occurs when a constraint (primary key, foreign key, check constraint or trigger constraint) is violated.
    print("Caught an IntegrityError:",file=sys.stderr)
    print(err,file=sys.stderr)
    conn.rollback()
except psycopg2.InternalError as err:
    #InternalError generally represents a legitimate connection error, but may occur in conjunction with user defined functions.
    #In particular, InternalError occurs if you attempt to continue using a cursor object after the transaction has been aborted.
    #(To reset the connection, run conn.rollback() and conn.reset(), then make a new cursor)
    print("Caught an IntegrityError:",file=sys.stderr)
    print(err,file=sys.stderr)
    conn.rollback()
cursor.close()
conn.close()

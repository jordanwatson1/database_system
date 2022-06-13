# add_airports.py
# CSC 370 - Summer 2020 -
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

with open(input_filename) as f:
    for row in csv.reader(f):
        if len(row) == 0:
            continue #Ignore blank rows
        if len(row) != 4:
            print("Error: Invalid input line \"%s\""%(','.join(row)), file=sys.stderr)
            #Maybe abort the active transaction and roll back at this point?
            conn.rollback()
            break
        airport_code,airport_name,country,international = row
        if international.lower() not in ('true','false'):
            print('Error: Fourth value in each line must be either "true" or "false"',file=sys.stderr)
            #Maybe abort the active transaction and roll back at this point?
            conn.rollback()
            break
        international = international.lower() == 'true'
        
        #Do something with the data here
        #Make sure to catch any exceptions that occur and roll back the transaction if a database error occurs.
        try:
            cursor.execute("insert into airports values(%s, %s, %s, %s);", (airport_code, airport_name, country, international))
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
conn.commit()
cursor.close()
conn.close()

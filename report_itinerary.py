# report_itinerary.py
# CSC 370 - Summer 2020 - Assignment 6
#
#
# Jordan Watson - 08/01/2020

import psycopg2, sys

# Open your DB connection here
psql_user = 'jordanwatson1'
psql_db = 'jordanwatson1'
psql_password = 'p1n3appl3'
psql_server = 'studdb1.csc.uvic.ca'
psql_port = 5432

conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)

cursor = conn.cursor()

def print_header(passenger_id, passenger_name):
    print("Itinerary for %s (%s)"%(str(passenger_id), str(passenger_name)) )
    
def print_entry(flight_id, airline, source_airport_name, dest_airport_name, departure_time, arrival_time, duration_minutes, aircraft_id, aircraft_model):
    print("Flight %-4s (%s):"%(flight_id, airline))
    print("    [%s] - [%s] (%s minutes)"%(departure_time, arrival_time,duration_minutes))
    print("    %s -> %s (%s: %s)"%(source_airport_name, dest_airport_name, aircraft_id, aircraft_model))


if len(sys.argv) < 2:
    print('Usage: %s <passenger id>'%sys.argv[0], file=sys.stderr)
    sys.exit(1)

passenger_id = sys.argv[1]


# passenger with given id does not exist
cursor.execute("select passenger_name from passengers where passenger_ID = %s;", (passenger_id,))
row_get_name = cursor.fetchone()
if row_get_name is None:
    print('No passenger with the id %s exisits'%sys.argv[1], file=sys.stderr)
    conn.rollback()
    sys.exit(1)

passenger_name = row_get_name[0]

# passenger with given id does exist but does not have any reservations
cursor.execute("select passenger_ID from reservations where passenger_ID = %s;", (passenger_id,))
row_resos = cursor.fetchone()
if row_resos is None:
    print_header(passenger_id, passenger_name)
    print('The passenger with the id %s does not contain any reservations'%sys.argv[1], file=sys.stderr)
    conn.rollback()
    sys.exit(1)

cursor.execute(""" with 
                source_airport_name as (select airport_name as source, flight_ID_num, aircraft_ID
                                            from airports
                                            natural join flights
                                            natural join aircrafts
                                            where IATA_code = source_IATA_code),
                dest_airport_name as (select airport_name as dest, flight_ID_num, aircraft_ID
                                            from airports
                                            natural join flights
                                            natural join aircrafts
                                            where IATA_code = dest_IATA_code)
                select flight_ID_num, airline_name, source, dest, departure_time, arrival_time, 
                    ((extract(epoch from arrival_time) - extract(epoch from departure_time))/60)::int as duration_minutes, 
                    aircraft_ID, model_name
                    from 
                        flights
                            natural join
                        aircrafts
                            natural join
                        source_airport_name
                            natural join
                        dest_airport_name
                        	natural join
                        reservations
                    where passenger_ID = %s
                    order by departure_time, flight_ID_num;""", (passenger_id,))

print_header(passenger_id, passenger_name)
while True:
    row = cursor.fetchone()
    if row is None:
        break
    print_entry(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]) 

conn.commit()
cursor.close()
conn.close()

# Mockup: Print itinerary for passenger 12345 (Rebecca Raspberry)
#passenger_id = 12345
#passenger_name = 'Rebecca Raspberry'
#print_header(passenger_id, passenger_name)
#print_entry(10,'WestJet','Vancouver International Airport','Victoria International Airport','2020-06-29 09:24','2020-06-29 09:55',31,'A1233','Dehavilland DHC-8')
#print_entry(12,'Air Canada','Vancouver International Airport','Lester B. Pearson International Airport','2020-06-29 15:00','2020-06-29 19:20',260,'A1234','Boeing 737-300')

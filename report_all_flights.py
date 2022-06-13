# report_all_flights.py
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

cursor.execute("""with 
                num_seats_full as (select count(*) as seats_full, flight_ID_num 
                                        from reservations
                                        group by flight_ID_num
                                    union
                                    select 0 as seats_full, flight_ID_num
                                        from 
                                            (select flight_ID_num from flights
                                            except 
                                            select flight_ID_num from reservations) as T1),
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
                    aircraft_ID, model_name, passenger_capacity, seats_full 
                    from 
                        flights
                            natural join
                        aircrafts
                            natural join
                        num_seats_full
                            natural join
                        source_airport_name
                            natural join
                        dest_airport_name
                    order by departure_time, flight_ID_num;
                """)

def print_entry(flight_id, airline, source_airport_name, dest_airport_name, departure_time, arrival_time, duration_minutes, aircraft_id, aircraft_model, seating_capacity, seats_full):
    print("Flight %s (%s):"%(flight_id,airline))
    print("    [%s] - [%s] (%s minutes)"%(departure_time,arrival_time,duration_minutes))
    print("    %s -> %s"%(source_airport_name,dest_airport_name))
    print("    %s (%s): %s/%s seats booked"%(aircraft_id, aircraft_model,seats_full,seating_capacity))

while True:
    row = cursor.fetchone()
    if row is None:
        break
    print_entry(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10])

cursor.close()
conn.close()

#Mockup: Print details for two flights 
#print_entry(10,'WestJet','Vancouver International Airport','Victoria International Airport','2020-06-29 09:24','2020-06-29 09:55',31,'A1233','Dehavilland DHC-8',70,35)
#print_entry(12,'Air Canada','Vancouver International Airport','Lester B. Pearson International Airport','2020-06-29 15:00','2020-06-29 19:20',260,'A1234','Boeing 737-300',140,101)

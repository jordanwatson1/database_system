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
	            count_flights as 
		        (select count(*) as num_flights, aircraft_ID 
			    from 
				flights 
			    group by 
				aircraft_ID
		    union
		    select 0 as num_flights, aircraft_ID
			from
			    (select aircraft_ID
			    	from
	        		    aircrafts
		            except
			    select aircraft_ID 
				from 
		    		    flights) as T1),
	            total_minutes as 
		        (select aircraft_ID, 
			    sum((extract(epoch from arrival_time) - extract(epoch from departure_time))/ 60) as sum
			    from 
				flights
			    group by aircraft_ID),
	            total_hours as
		        (select aircraft_ID, round((sum/60)::int, 0) as flight_hours
			    from 
                                total_minutes
		        union
		        select aircraft_ID, 0 as flight_hours
			    from
				(select aircraft_ID
				    from
					aircrafts
				except
				select aircraft_ID 
				    from 
					flights) as T1),
                    count_reservations as (
	                select count(*) as num_reservations, aircraft_ID 
		            from 
			        reservations 
			    natural join 
			        flights 
		            group by aircraft_ID
	                union
	                select distinct 0 as num_reservations, aircraft_ID
		            from
                                (select flight_ID_num, aircraft_ID 
                                    from
                                        (select aircraft_ID from flights
                                        except 
                                        select distinct aircraft_ID 
                                        	from (select distinct aircraft_ID, flight_ID_num 
                                        			from reservations natural join flights) as T5
                                      	) as T1
                                    natural join
                                        flights) as T2),
                    count_num_flights as 
	                (select count(*) as num_flights, aircraft_ID from flights group by aircraft_ID),
                    avg_seat_count as
	                (select (num_reservations/num_flights::real) as avg_seats_full, aircraft_ID from count_reservations natural join count_num_flights),
                    aircraft_report as
	                (select aircraft_id, airline_name, model_name, num_flights, flight_hours, avg_seats_full, passenger_capacity 
			    from aircrafts
				natural join
					count_flights
				natural join
					total_hours
				natural join
					avg_seat_count
		        union
		        select aircraft_id, airline_name, model_name, 0 as num_flights, 0 as flight_hours, 0 as avg_seats_full, passenger_capacity
			    from
				(select aircraft_ID from aircrafts
				except
				select aircraft_ID from flights) as T4
			            natural join aircrafts)
            select * from aircraft_report
	        order by aircraft_ID;
               """)

def print_entry(aircraft_id, airline, model_name, num_flights, flight_hours, avg_seats_full, seating_capacity):
    print("%-5s (%s): %s"%(aircraft_id, model_name, airline))
    print("    Number of flights : %d"%num_flights)
    print("    Total flight hours: %d"%flight_hours)
    print("    Average passengers: (%.2f/%d)"%(avg_seats_full,seating_capacity))

while True:
    row = cursor.fetchone()
    if row is None:
        break
    print_entry(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
    
cursor.close()
conn.close()

#Mockup: Print details for two aircraft
#print_entry('A1234','Air Canada','Boeing 737-300',0,0,0,140)
#print_entry('A1235','Air Canada','Boeing 777-333ER',10,100,16.7,140)

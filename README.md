# database_system

### CSC 370 - SUMMER 2020 DATABASE SYSTEMS ASSIGNMENT 6 UNIVERSITY OF VICTORIA

### Overview
This assignment covers applied database design and the use of database interfaces in a high level programming language (Python). The submission for this assignment consists of a database definition (CREATE statements and accompanying constraint definitions) in SQL (submitted as a .txt file due to conneX limitations) and a set of short Python3 programs to act as database front-ends. Some of the Python programs will read comma-separated input data and perform database insertion and update operations. The other programs will use SELECT statements to retrieve data from the DBMS and format it as a report for the user.

### Computing Environment 
The Python programs run in the Linux environment. I used the psycopg2 module (for PostgreSQL connectivity) and the Python standard library since the Python programs contain very little non-trival code.

### The Task: Tracking Flights, Aircrafts and Passengers
The task for this assignment is to design a database schema and a set of front-end programs for a flight tracking database. The database will contain information on airports, aircraft, flights, passengers and ticket reservations.

The following files were submitted below:

create_schema.txt: A schema creation file, consisting of an SQL script with DROP and CREATE statements for each table, along with DROP and CREATE statements for all required constraints. It must be possible to completely drop/recreate your database schema by running all of the commands in this file.
add_airports.py
add_aircraft.py
manage_flights.py
manage_reservations.py
report_all_flights.py
report_itinerary.py

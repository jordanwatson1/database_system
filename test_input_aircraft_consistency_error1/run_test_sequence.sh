# This script was used to generate the model output for this test case.
# It assumes that your solution is in the directory ../solution

# Re-run the create_schema.txt script to clear and re-populate the database
# psql -h studdb1.csc.uvic.ca your_db_here your_name_here < create_schema.txt

# All of the data entry commands below should succeed and generate no output.
# The report programs should all succeed (and pipe their output to files)

python3 ../add_airports.py  airports.txt
python3 ../add_aircraft.py  aircraft.txt
python3 ../manage_flights.py flights1.txt

python3 ../report_all_flights.py > output_report_all_flights_round1.txt
python3 ../report_aircraft.py > output_report_aircraft_round1.txt


# This command attempts to modify an existing flight (1008) then violates the
# aircraft consistency constraint by scheduling a flight too soon after an existing flight
# It should fail (and all of the attempted modification should be rolled back)
python3 ../manage_flights.py flights2.txt

python3 ../report_all_flights.py > output_report_all_flights_round2.txt
python3 ../report_aircraft.py > output_report_aircraft_round2.txt


# This command attempts to modify an existing flight (1008) then violates the
# aircraft consistency constraint by scheduling a flight too soon before an existing flight
# It should fail (and all of the attempted modification should be rolled back)
python3 ../manage_flights.py flights3.txt

python3 ../report_all_flights.py > output_report_all_flights_round3.txt
python3 ../report_aircraft.py > output_report_aircraft_round3.txt

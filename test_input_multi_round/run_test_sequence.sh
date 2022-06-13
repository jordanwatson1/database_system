# This script was used to generate the model output for this test case.
# It assumes that your solution is in the directory ../solution

# Re-run the create_schema.txt script to clear and re-populate the database
# psql -h studdb1.csc.uvic.ca your_db_here your_name_here < create_schema.txt

# All of the data entry commands below should succeed and generate no output.
# The report programs should all succeed (and pipe their output to files)

python3 ../add_airports.py  airports1.txt
python3 ../add_aircraft.py  aircraft1.txt
python3 ../manage_flights.py flights1.txt
python3 ../manage_reservations.py reservations1.txt

python3 ../report_all_flights.py > output_report_all_flights_round1.txt
python3 ../report_aircraft.py > output_report_aircraft_round1.txt
python3 ../report_itinerary.py 12348 > output_report_itinerary_12348_round1.txt

python3 ../add_aircraft.py  aircraft2.txt
python3 ../manage_flights.py flights2.txt
python3 ../add_airports.py  airports2.txt
python3 ../manage_flights.py flights3.txt
python3 ../manage_reservations.py reservations2.txt

python3 ../report_all_flights.py > output_report_all_flights_round2.txt
python3 ../report_aircraft.py > output_report_aircraft_round2.txt
python3 ../report_itinerary.py 12348 > output_report_itinerary_12348_round2.txt


python3 ../manage_reservations.py reservations3.txt
python3 ../manage_flights.py flights4.txt

python3 ../report_all_flights.py > output_report_all_flights_round2.txt
python3 ../report_aircraft.py > output_report_aircraft_round2.txt
python3 ../report_itinerary.py 12348 > output_report_itinerary_12348_round2.txt

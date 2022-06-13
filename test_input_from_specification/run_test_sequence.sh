# This script was used to generate the model output for this test case.
# It assumes that your solution is in the directory ../solution

# Re-run the create_schema.txt script to clear and re-populate the database
# psql -h studdb1.csc.uvic.ca your_db_here your_name_here < create_schema.txt

# All of the data entry commands below should succeed and generate no output.
# The report programs should all succeed (and pipe their output to files)

python3 ../solution/add_airports.py  airports.txt
python3 ../solution/add_aircraft.py  aircraft.txt
python3 ../solution/manage_flights.py flights.txt
python3 ../solution/manage_reservations.py reservations.txt

python3 ../solution/report_all_flights.py > output_report_all_flights.txt
python3 ../solution/report_aircraft.py > output_report_aircraft.txt
python3 ../solution/report_itinerary.py 12346 > output_report_itinerary_12346.txt
python3 ../solution/report_itinerary.py 12348 > output_report_itinerary_12348.txt    

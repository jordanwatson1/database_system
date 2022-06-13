# This script was used to generate the model output for this test case.
# It assumes that your solution is in the directory ../solution

# Re-run the create_schema.txt script to clear and re-populate the database
# psql -h studdb1.csc.uvic.ca your_db_here your_name_here < create_schema.txt

# All of the data entry commands below should succeed and generate no output.

python3 ../add_airports.py  airports.txt
python3 ../add_aircraft.py  aircraft.txt
python3 ../manage_flights.py flights.txt
python3 ../manage_reservations.py reservations1.txt
# Note: reservations2.txt contains several add and remove entries that, together
#       do not overfill any flight (as long as constraints are deferred)
python3 ../manage_reservations.py reservations2.txt


# Now, try to add too many passengers to a flight and leave them there (which should result in an error)
echo 'Attempting to add too many passengers to Flight 1 (should fail)'
python3 ../manage_reservations.py reservations3.txt

# One of the passengers in the reservations3.txt file had ID 123456
# Since the reservations3.txt file contained errors, that passenger should not have been added
# to the database, so the command below should fail as well.
echo 'Trying to generate an itinerary (should fail)'
python3 ../report_itinerary.py 123456

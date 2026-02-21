''' 
Welcome Pilot-In-Training! This is your fully functioning weight and balance 
calculator to determine if you are able to fly to your desired destination. 

For this trip, you and your passenger(s) will be travelling to Muskoka for the 
weekend! This will act as your weight and balance calculator for your flight, 
to ensure that everything goes smoothly and that we are even able to takeoff/land. 
All this information will then be produced into a separate file for your flight 
briefing. 

This program will take into consideration: aircraft limitations, fuel, take-off/landing 
conditions, centre of gravity and more. 

NOTE: the plane is a G1000 C-172 plane with 4 seats and a max takeoff/landing weight of 2550lbs.

Have a safe flight! 
'''

# ------------------------------------------------------------------------------------------------------------
# This first section will acquire the necessary information to perform our calculations
# ------------------------------------------------------------------------------------------------------------

pilot_wgt = int(input('Please enter your weight in lbs: '))

if pilot_wgt > 500:    
    while pilot_wgt > 500: 
        print("Please enter a reasonable number.")
        pilot_wgt = int(input('Please enter your weight in lbs: '))


passengers = int(input('Please enter the number of passengers: '))
passenger_wgt_list = []

if passengers > 4: 
    while passengers > 4: 
        print("Sorry, there is not enough seats on the plane!") 
        passengers = int(input('Please enter the number of passengers: '))
    
elif passengers < 0:
    while passengers < 0: 
        print("Please enter a number greater than 0.")
        passengers = int(input('Please enter the number of passengers: '))

else: 
    for i in range(passengers):
        passenger_wgt = int(input('Please enter the weight of each passenger: '))
        passenger_wgt_list.append(passenger_wgt)
    

bags = int(input('How many pounds does your luggage weigh?: '))

i = 0
total_wgt = pilot_wgt + bags
pass_total_wgt = 0

while i != len(passenger_wgt_list):
    total_wgt += passenger_wgt_list[i]   # weight with bags, pilot and passengers
    pass_total_wgt += passenger_wgt_list[i]  # weight of only passengers
    i += 1

# ------------------------------------------------------------------------------------------------------------
# This next function will calculate the initial centre of gravity, without taking into account the fuel
# ------------------------------------------------------------------------------------------------------------

arm = 37  # given value in each plane
empty_weight = 1710.7  # weight of aircraft without fuel or passengers
empty_moment = 63.29

def centre_of_gravity(pass_total_wgt, arm):
    pass_mmt = (pass_total_wgt * arm) / 1000
    bags_mmt = (bags * arm) / 1000
    centreofg1 = ((pass_mmt + bags_mmt + empty_moment) / (total_wgt + empty_weight)) * 1000
    return centreofg1, pass_mmt, bags_mmt

# -----------------------------------------------------------------------------------------------------------------
# This next function will calculate the 2nd centre of gravity, but considering the fuel needed to reach our destination
# -----------------------------------------------------------------------------------------------------------------

def fuel_centre_of_gravity(pass_mmt, bags_mmt, empty_moment):
    fuel_loading = 318  # another given value for the specified aircraft
    fuel_moment = 11.766

    # calculates the total weight on the ramp before takeoff (includes passengers, fuels, etc.)
    ramp_condition = (total_wgt + empty_weight) + fuel_loading
    ramp_mmt = (pass_mmt + bags_mmt + empty_moment) + fuel_moment

    # calculates the aircrafts weight and balance at the moment of takeoff
    # -8.4 is a constant
    takeoff_conditions = ramp_condition - 8.4
    takeoff_mmt = ramp_mmt - ((-8.4 * arm) / 1000)

    centreofg2 = (takeoff_mmt / takeoff_conditions) * 1000
    return centreofg2, takeoff_conditions, takeoff_mmt

# ---------------------------------------------------------------------------------------------------------
# This next function will calculate the final centre of gravity, which is when we land with the remaining fuel
# ---------------------------------------------------------------------------------------------------------

def destination_fuel(takeoff_conditions, takeoff_mmt):
    muskoka = 182.6  # km
    burn_rate = 38  # liters/hour

    # calculates the fuel required to arrive at Muskoka
    fuel_required = ((burn_rate / muskoka) * 100) * 6

    # calculates the centre of gravity at the time of landing
    landing_cofg = ((takeoff_mmt - (fuel_required * arm / 1000)) / (takeoff_conditions - fuel_required)) * 1000
    return landing_cofg

# --------------------------------------------------------------------------------------------------------------
# This checks all calculations and will see if we can fly
# --------------------------------------------------------------------------------------------------------------

def check(centreofg1, centreofg2, landing_cofg, takeoff_conditions):
    # if the total weight exceeds 2550lbs, it wont be able to conduct takeoff or landing
    # if any of the centre of gravities are out of this range, the plane will be unbalanced and unsafe to fly
    if takeoff_conditions <= 2550 and 35 <= centreofg1 <= 40 and 35 <= centreofg2 <= 40 and 35 <= landing_cofg <= 40:
        return 'Ready to fly!!'
    else:
        return 'Sorry, but we are not able to fly'

# -----------------------------------------------------------------------------------------------------------------
# This section will call and execute all the functions
# -----------------------------------------------------------------------------------------------------------------

centreofg1, pass_mmt, bags_mmt = centre_of_gravity(pass_total_wgt, arm)
centreofg2, takeoff_conditions, takeoff_mmt = fuel_centre_of_gravity(pass_mmt, bags_mmt, empty_moment)
landing_cofg = destination_fuel(takeoff_conditions, takeoff_mmt)
result = check(centreofg1, centreofg2, landing_cofg, total_wgt)

# ---------------------------------------------------------------------------------------------------------------
# This section will create and output a report on a separate file with all information for a flight briefing
# ---------------------------------------------------------------------------------------------------------------

report_file = 'report.txt'

with open(report_file, 'w') as report_file:
    report_file.write('\n==========================\n')
    report_file.write('FLIGHT BRIEFING REPORT')
    report_file.write('\n==========================\n')
    report_file.write('Welcome Future Pilot!\n')
    report_file.write('\nHere is a summary of your data for your trip to Muskoka:\n')

    # Writes basic information into report
    report_file.write('\n==== INITIAL INFORMATION ====\n')
    report_file.write(f'\nEmpty Weight: {empty_weight} lbs')
    report_file.write(f'\nPilot Weight: {pilot_wgt} lbs')
    report_file.write(f'\nNumber of Passengers: {passengers}')
    report_file.write(f'\nTotal Weight of Passengers: {pass_total_wgt} lbs')
    report_file.write(f'\nTotal Weight of Bags: {bags} lbs\n')

    # Centre of Gravity Calculations
    report_file.write('\n==== CENTRE OF GRAVITY CALCULATIONS ====\n')
    report_file.write(f'\nInitial Centre of Gravity: {centreofg1: .2f}')
    report_file.write(f'\nCentre of Gravity with Fuel: {centreofg2: .2f}')
    report_file.write(f'\nLanding Centre of Gravity: {landing_cofg: .2f}\n')

    # Final Flight Checks
    report_file.write('\n==== FINAL CHECKS ====\n')
    report_file.write(f'\nAircraft Status: {result}')
    report_file.write('\nMax Takeoff and Landing Weight: 2550\n')
    report_file.write('\n================================\n')
    report_file.write('FLIGHT BRIEFING REPORT COMPLETE')
    report_file.write('\n================================\n')
    report_file.write('\nThank you!!\n')

# indicates if information was added successfully
print(f"\nFlight Briefing Successfully Added to Report: {report_file}")

# Main loop execution
import re
from final_ir import run_query

if __name__ == '__main__':
    print("Welcome to the Baltimore-NYC travel crawler!\n")
    print("This program allows you to find travel options for a one-way trip between Baltimore and New York City. You will need to input some information to help us with your search.\n\n")
    while True:
        # Display options and prompt user for input
        destination = input("Are you going to Baltimore or New York? Input BWI or NYC:\n")

        while destination.upper() != "BWI" and destination.upper() != "NYC":
            destination = input("You must input either BWI or NYC as your destination:\n")

        date = input("What date would you like to depart? (MM/DD/YYYY):\n")
        pattern = r'^\d{2}/\d{2}/\d{4}$'

        while re.match(pattern, date) is None:
            date = input("You must input a date of the format MM/DD/YYYY:\n")

        time = input("What time do you need to arrive by? (00:00 AM/PM):\n")
        pattern = r'^\d{2}:\d{2} (?:AM|PM)$'
        while re.match(pattern, time) is None:
            time = input("You must enter time of the format 00:00 AM/PM:\n")

        run_query(date, time, destination)

        option = input("Press 1 if you want to do another search, or 0 to exit\n")

        while int(option) != 1 and int(option) != 0:
            option = input("You need to either input a 1 or 0\n")
        
        if int(option) == 0:
            exit()

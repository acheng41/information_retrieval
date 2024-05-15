# Main loop execution
import re
from transport_search import get_data, get_sortedData

if __name__ == '__main__':
    print("Welcome to the Baltimore-NYC travel crawler!\n")
    print("This program allows you to find travel options for a one-way trip between Baltimore and New York City. You will need to input some information to help us with your search.\n\n")
    while True:
        # Display options and prompt user for input
        destination = input("Are you going to Baltimore or New York? Input BWI or NYC:\n")

        while destination.upper() != "BWI" and destination.upper() != "NYC":
            destination = input("You must input either BWI or NYC as your destination:\n")

        if destination == "BWI": 
            origin = "NYC"
        else: 
            origin = "BWI"
        
        date = input("What date would you like to depart? (MM/DD/YYYY):\n")
        pattern = r'^\d{2}/\d{2}/\d{4}$'

        while re.match(pattern, date) is None:
            date = input("You must input a date of the format MM/DD/YYYY:\n")

        time = input("What time do you need to arrive by? (00:00 AM/PM):\n")
        pattern = r'^\d{2}:\d{2} (?:AM|PM)$'
        while re.match(pattern, time) is None:
            time = input("You must enter time of the format 00:00 AM/PM:\n")
        
        rank = input("How do you want results to be ordered? Please say cheapest, fastest, or recommended.\n")
        while rank.lower() != "cheapest" and rank.lower() != "fastest" and rank.lower() != "recommended":
            rank = input("You must input either cheapest, fastest, or recommended.\n")

        mode = input("Do you have a preferred mode of transportation? Please enter all preferred methods separated by a comma (,): plane, bus, train, all.\n")
        pattern = r'^\s*(plane|bus|train|all)(?:\s*,\s*(plane|bus|train|all))*\s*$'
        while re.match(pattern, mode.lower()) is None: 
            mode = input("You must input plane, bus, train, car, or all.\n")


        res_df = get_data(time, origin, destination, date, mode)

        #Define Sort Type
        if rank == 'cheapest':
            sort_type = '1'
        elif rank == 'fastest':
            sort_type = '2'
        else:
            sort_type = '3'
        get_sortedData(sort_type, res_df, time)


        print(" ")
        option = input("Press 1 if you want to do another search, or 0 to exit\n")

        while int(option) != 1 and int(option) != 0:
            option = input("You need to either input a 1 or 0\n")
        
        if int(option) == 0:
            exit()

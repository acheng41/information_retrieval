# INFORMATION RETRIEVAL FINAL PROJECT 
EN.601.466, Section 1

Taylor Rohovit (trohovi1@jh.edu), Andrea Cheng (acheng41@jh.edu) 

## Summary of project focus:
This project extracts information from multiple sites in order to provide the user with useful travel information between 
Baltimore and New York City. The user provides the program with some additional information to help give more context, 
such as origin, destination, date, arrival time, and their preferences (cheapest, fastest, or our recommended ranking).

## Installation (using Visual Studio Code):
In Git Bash:
git clone https://github.com/acheng41/information_retrieval/tree/main/FinalProject 

Then:
1) To create a new conda environment:
conda create -n transportsearch python=3.8.8
conda activate transportsearch
pip install -r requirements.txt

OR

2) To use an existing environment:
pip install -r requirements.txt


## Usage:
To run the commandline interface:
```
python main.py
```
## Project Achievements
1. Successfully implemented an ethical crawler and extracted information from travel listings on multiple websites.
2. Standardizes and cleanly presents mode of transportation, departure time, arrival time, duration of travel, price, 
   and airline/bus line/train information.
3. Allows user to specify preferred modes of transportation (plane, train, bus, or all)  and preferred ranking 
   mechanisms (cheapest, fastest, recommended)
4. Rankings and suggested transportation accounts for travel time from bus/train stations and airports. 30 min was 
   added to arrival times of buses and trains, and 1 hour to arrival of planes to account for exiting the stations/airports, 
   prioritizing user safety in arriving at their destination within each city.  
5. Robust error handling is performed to mitigate errors from web crawling, and a pre-saved file is included to 
   demonstrate ranking mechanism upon failure.

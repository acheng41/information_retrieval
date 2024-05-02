## Summary of project focus:
The aim of this project is to implement a collection fusion application to compile rental housing information based on an input search query in the form of a neighborhood, city, or zip code. A user can
then view all the preferred apartment listings compiled from multiple housing websites, thus simplifying the housing search process to avoid searching and comparing the different sites individually.

## Installation (these instructions assume a working Anaconda/Miniconda in system or a working Visual
Studio Code environment):
In Git Bash:
git clone https://github.com/kunalkotkar10/IRWA_Project_2023.git
Then:
1) In Miniconda Command Prompt:
conda create -n apartments python=3.10
conda activate apartments
pip install -r requirements.txt
OR
2) In Visual Studio Code:
pip install -r requirements.txt
Usage:
To run the Interface, run
python website.py
And open the localhost link (http://127.0.0.1:5000/) in your browser.

## Project Achievements
1. Successfully demonstrates the ability to fuse
and output search results extracted from
multiple websites.
2. Implements an ethical crawler to extract
information from search results and individual
rental listing pages linked from those search
results.
3. Stores, cleans, and standardizes rental
information so it can be presented in a
concise, easy-to-read way.
4. Implements a web interface for accessible
user interaction that includes a search function
and an interactive output table.
5. The model is capable of sorting the extracted
apartments list according to the prices,
number of beds, number of baths depending
on the user’s preferences.
6. The model removes any duplicate apartments
which it might extract from different websites.

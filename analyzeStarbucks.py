"""
MAT 2170: Lab 7
Analyze a CSV file giving information about location of Starbucks stores

Submitted by:
"""

import lab7Functions as f7
import csv


# Get the state/region information
states = f7.makeMapping('states.csv')
regions = f7.makeInverseMapping(states)

# Present a list of options -- which region to analyze
region_list = list(regions.keys())
region_choice = f7.offerMenuItems(region_list)

# Create a list of states in this region
r_states = regions[region_list[region_choice]]

f = open("starbucks.csv", 'r')
csvf = csv.reader(f)
# Process the Starbucks data file. For each line of the file, determine if
# it appears in one of the desired states.  If so, append the state
# to the list of states; otherwise ignore it
freq_states = []
for line in csvf:
    state_abrev = f7.state(line[3],states)
    if state_abrev in r_states:
        freq_states.append(state_abrev)

f.close()

# Produce a histogram showing the frequency of stores by state
f7.frequencyChart(freq_states)

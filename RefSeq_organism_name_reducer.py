#!/usr/bin/env Python
import operator
import sys
import csv
import random
import os
import time

# Remember this: it lets raw_input do tab completion!
import readline
readline.parse_and_bind("tab: complete")

# RefSeq_output_reducer_v1.py
# Created 3/30, Sam Westreich (swestreich@gmail.com)
# This should go through the RefSeq output file (filename.tab) and should take 
# each line and simplify it down to species names, removing strain names.

try:
	input_file_name = sys.argv[1]
except IndexError:
	input_file_name = raw_input("Specify the output file to be simplified: ")

input_file = open (input_file_name, "r")

# output file saving and renaming; feel free to change ####################

output_file_name = input_file_name[:-4] + "_simplified.tab"
output_file = open (output_file_name, "w")

line_counter = 0

# Start reading through the file
for line in input_file:
	line_counter += 1
	if line_counter > 1:
		splitline = line.split("\t")
		Species_name = splitline[3].strip()
		splitname = Species_name.split()
		
		output_file.write(splitline[0] + "\t" + splitline[1] + "\t" + splitline[2] + "\t" + splitname[0] + " " + splitname[1] + "\n")
		
	else:
		output_file.write(line)
		continue

input_file.close()
output_file.close()
#!/usr/bin/env Python
import operator
import sys
import subprocess
import os

# Remember this: it lets raw_input do tab completion!
import readline
readline.parse_and_bind("tab: complete")

# MG-RAST_API_downloader.py
# Created 12/09/2014 by Sam Westreich
# Purpose: With proper inputs, this should automatically generate the API calls to download MG-RAST sequences for the next steps in the metatranscriptome pipeline.

# Disclaimer
print ("This is Sam Westreich's EZ-downloader for MG-RAST annotations.")
print ("NOTE: The generated command will likely run for several hours.  For optimum flexibility, run this in a separate screen session to allow for logging out without disruption.")

# Pipeline usage (single command)
print ("For use in a pipeline, specify, in the following order:/n")
print ("Source, Data type, Authorization key, Annotation link, Save file\n")

# Connection testing
print ("\nTesting internet connection...")
proc = subprocess.Popen("ping -c 1 metagenomics.anl.gov", shell = True, stdout = subprocess.PIPE, )
output = proc.communicate()[0]
if "0.0% packet loss" in output:
	print ("Web connection is active and working.")
else:
	print ("Failure to connect to MG-RAST.  Is your internet connection active?")
	sys.exit()

# Source menu:
try:
	source = sys.argv[1]
	print ("Source: " + source)
except IndexError:
	print ("\n\t\tSOURCES:")
	print ("RefSeq\t\tProtein database - organism, function, or feature")
	print ("SwissProt\tProtein database - organism, function, or feature")
	print ("KEGG\t\tProtein database - organism, function, or feature")
	print ("Subsystems\tOntology database, for ontology only")
	print ("KO\t\tOntology database, for ontology only")
	print ("NOG\t\tOntology database, for ontology only")
	print ("COG\t\tOntology database, for ontology only")
	print ("\n(Other databases can be found listed at api.metagenomics.anl.gov/api.html#annotation .)\n")
	source = raw_input("Select annotation source from the list above: ").lower()
	source_options = ["refseq", "swissprot", "kegg", "subsystems", "ko", "nog", "cog", "genbank", "img", "seed", "trembl", "patric", "rdp", "greengenes", "lsu", "ssu"]
	if source not in source_options:
		sys.exit("WARNING: Selected source type is not a valid option.  Terminating...")
	
# Building the API command
try:
	seqtype = sys.argv[2]
	print ("Sequence type: " + seqtype)
except IndexError:
	# Type menu:
	print ("\n\t\tDOWNLOAD TYPES:")
	print ("Organism\tReturns organism matches for each annotation.")
	print ("Function\tReturns function matches for each annotation.")
	print ("Ontology\tReturns annotations listed by functional category [WARNING: currently broken downstream].\n")
	seqtype = raw_input("Select type of download from the list above: ").lower()
	seqtype_options = ["organism", "function", "ontology", "feature"]
	if seqtype not in seqtype_options:
		sys.exit("WARNING: Selected download type is not a valid option.  Terminating...")

try:
	auth = sys.argv[3]
	print ("Authorization key: " + auth)
except IndexError:
	auth = raw_input("Type in or copy/paste the MG-RAST authorization key: ")

try:
	annotation_ID = sys.argv[4]
	print ("Annotation ID number: " + annotation_ID)
except IndexError:
	annotation_ID = raw_input("Type in the annotation's ID number (including decimal point, e.g. '4577800.3'): ")

try:
	output_name = sys.argv[5]
	print ("Output name: " + output_name)
except IndexError:
	scoutput_name = raw_input("Type in the name of where output should be saved (NOTE: do not type a path): ")

# Assembling the html link
API_link = "http://api.metagenomics.anl.gov//annotation/sequence/mgm" + str(annotation_ID) + "?type=" + seqtype + "&source=" + source
print ("\nLink being used: " + API_link)

# Assembling the API command
API_command = "curl -o \"" + output_name + "\" -H \'auth:" + auth + "\' -X GET " + API_link

print ("\nCommand being used:\n" + API_command)

# Time to execute!
print ("\nNOTE: when the active text cursor is down BELOW the download display, press \'Enter\' to verify that the download has finished.")
os.system(API_command)

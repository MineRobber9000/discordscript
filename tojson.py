import parser as dsp
import csv
import argparse
import copy
import json

parser = argparse.ArgumentParser(description="Reads DiscordScript files")
parser.add_argument("script",type=argparse.FileType("r"),help="The script to read")
parser.add_argument("-c","--characters",type=argparse.FileType("r"),help="A CSV file of the characters' script names, display names, and avatars.")
parser.add_argument("-t","--time",help="The time to display on the clock thing. Will be consistent across all messages.")
args = parser.parse_args()

chars = dict()
if args.characters:
	r = csv.reader(args.characters)
	for row in r:
		if len(row)<2: continue
		chars[row[0].upper()]=tuple(row[1:])

messages = dsp.parse(args.script)

out = dict()
out["messages"]=messages
out["characters"]=chars

with open("out.json","w") as f:
	json.dump(out,f)

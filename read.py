import parser as dsp
import csv
import argparse
import copy
from collections import UserDict

class DefDict(UserDict):
	def __getitem__(self,k):
		if k not in self.data:
			self[k]=(k,"NONE")
		return self.data[k]

parser = argparse.ArgumentParser(description="Reads DiscordScript files")
parser.add_argument("script",type=argparse.FileType("r"),help="The script to read")
parser.add_argument("-c","--characters",type=argparse.FileType("r"),help="A CSV file of the characters' script names, display names, and avatars.")
args = parser.parse_args()

chars = DefDict()
if args.characters:
	r = csv.reader(args.characters)
	for row in r:
		if len(row)<2: continue
		chars[row[0].upper()]=tuple(row[1:])

messages = dsp.parse(args.script)
og_messages = copy.deepcopy(messages)
messages.sort(key=lambda x: (x["speaker"],-og_messages.index(x)),reverse=True)
del og_messages

for message in messages:
	print(message["speaker"],*chars[message["speaker"]])
	print(message["message"])
	input("Continue?")

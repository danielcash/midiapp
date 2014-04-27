#!/usr/bin/python

import sys

# Alteration.sharp5  = 0
# Alteration.flat9   = 1
# Alteration.sharp9  = 2
# Alteration.sharp11 = 3
# Alteration.sharp15 = 4
# Alteration.add2    = 5
# Alteration.add4    = 6

#----------------------------------------------#
# Globals
#----------------------------------------------#
pitches = [False] * 12
alterations = [False] * 7
quality = "WTF"
extension  = 0

pitch_array = ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
alteration_array = ["(#5)", "(b9)", "(#9)", "(#11)", "(#15)", "(add 2)", "(add 4)"]

#----------------------------------------------#
# function: analyzeChord
# description: Take as input a list of pitches
#   and return the corresponding chord
#----------------------------------------------#
def analyzeChord(args):
	global pitches
	global alterations
	global quality
	global extension

	pitches = [False] * 12

	for pitch in args:
		pitches[int(pitch) % 12] = True

	alterations = [False] * 7

	pitches[0] = True
	quality = "WTF"
	extension = 0

	if (pitches[4]):
		if (pitches[10]):
			quality = "Dominant"
			extension = 7
			if (pitches[11]):
				quality = "WTF"
		else:
			quality = "Major"
			if (pitches[11]):
				extension = 7
		if (extension == 7):
			if (pitches[2]):
				extension = 9
			if (pitches[9]):
				extension = 13
			if (pitches[5]):
				if (extension == 9):
					extension = 11
				else:
					alterations[6] = True
			if (pitches[1]):
				if (pitches[2]):
					if (quality == "Major"):
						alterations[4] = True
					else:
						quality = "WTF"
				else:
                            		alterations[1] = True

			if (pitches[3]):
				if (pitches[2]):
					quality = "WTF"
				else:
					alterations[2] = True

			if (pitches[6]):
				if (pitches[5]):
					quality = "WTF"
				else:
					alterations[3] = True
			if (pitches[8]):
				alterations[0] = True
				if (pitches[7]):
					quality = "WTF"
		else:
			if (pitches[9]):
				extension = 6
			elif (pitches[2]):
				alterations[5] = True
			if (pitches[8]):
				alterations[0] = True

	elif (pitches[3]):
		if (pitches[6]):
			if (pitches[10]):
				quality = "Half-Diminished"
				if (pitches[7]):
					quality = "WTF"
				if (pitches[2] and pitches[1]):
					quality = "WTF"
				if (pitches[2]):
					extension = 9
				if (pitches[1]):
					alterations[1] = True
				if (pitches[5]):
					extension = 11
			else:
				quality = "Diminished"
				if (pitches[10] or pitches[1] or pitches[4] or pitches[7]):
					quality = "WTF"
				if (pitches[9]):
					extension = 7
				if (pitches[2]):
					extension = 9
				if (sum([pitches[11],pitches[2],pitches[5],pitches[8]]) >= 3):
					quality = "Double-Diminished"
					extension = 0
					alterations = [False] * 7
		else:
			quality = "Minor"
			if (pitches[11]):
				if (pitches[10]):
					quality = "WTF"
				else:
					quality = "Minor-Major"
					extension = 7
			if (pitches[10]):
				extension = 7
			if (extension != 7 and pitches[9]):
				extension = 6
			else:
				if (pitches[2]):
					if (extension == 7):
						extension = 9
					else:
						alterations[5] = True
				if (pitches[5]):
					if (extension > 0):
						extension = 11
					else:
						alterations[6] = True
				if (pitches[9] and extension > 0):
					extension = 13
				if (pitches[8]):
					if (pitches[9]):
						quality = "WTF"
					else:
						alterations[1] = True

	elif (pitches[5]):
		quality = "Suspended"
		if (pitches[10]):
			if (pitches[11]):
				quality = "WTF"
			else:
				extension = 7
		if (pitches[2]):
			if (extension == 7):
				extension = 9
			else:
				alterations[5] = True
		if (pitches[9] and extension > 0):
			extension = 13
		if (pitches[8]):
			if (pitches[9]):
				quality = "WTF"
			else:
				alterations[0] = True
		if (pitches[1]):
			if (pitches[2]):
				quality = "WTF"
			else:
				alterations[1] = True

	else:
		quality = "WTF"

	return


#----------------------------------------------#
# function: chordSymbol 
# description: Print out the chord symbol
#----------------------------------------------#
def chordSymbol():
	if (quality == "WTF"):
		return "Invalid Chord"

	ret_val = ""

	root = -1
	for (counter, p) in enumerate(pitches):
		if (p):
			root = counter
			break

	ret_val += pitch_array[root]
	if (not (extension == 0 and quality == "Major") and quality != "Dominant"):
		ret_val += quality
	if (extension != 0):
		ret_val += str(extension)
	for (counter, alt) in enumerate(alterations):
		if (alt):
			ret_val += alteration_array[counter]
	return ret_val

#----------------------------------------------#
# function: main
# description: Main function
#----------------------------------------------#
def main(argv):
	if (len(argv) >= 3):
		analyzeChord(argv)
		print chordSymbol()
	return

if __name__ == "__main__":
	main(sys.argv[1:])

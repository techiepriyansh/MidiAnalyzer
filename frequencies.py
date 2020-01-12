#modified to support midi format

coreFQS = {
	'C' : 0,
	'D'	: 2,
	'E'	: 4,
	'F' : 5,
	'G'	: 7,
	'A'	: 9,
	'B' : 11
}

coreFQS_inverted = {
	0 : 'C',
	2 : 'D',
	4 : 'E',
	5 : 'F',
	7 : 'G',
	9 : 'A',
	11 : 'B'
}

permitted_diff = {0,2,4,5,7,9,11}

#-----------------------------------------------------------------#

#C-1 : 0

#Note String Format: eg: "A4#" or "B2b" or "C1"

def getNoteIndex(note_string):
	core_freq = note_string[0]
	octave_number = 0
	black_key_offset = 0

	if len(note_string) == 2:
		octave_number = int(note_string[1])

	elif len(note_string) == 3:
		if note_string[2] == '#':
			octave_number = int(note_string[1])
			black_key_offset = 1
		elif note_string[2] == 'b':
			octave_number = int(note_string[1])
			black_key_offset = -1
		else:
			octave_number =int(note_string[1:])
	else:
		if note_string[3] == '#':
			octave_number =int(note_string[1:-1])
			black_key_offset = 1
		elif note_string[3] == 'b':
			octave_number =int(note_string[1:-1])
			black_key_offset = -1
		else:
			octave_number =int(note_string[1:-1])


	index = 12 * (octave_number + 1) + coreFQS[core_freq] + black_key_offset

	return index

#-----------------------------------------------------------------#	

def getNoteFromIndex(index):
	octave_number = int(index / 12) - 1
	if not index % 12 in permitted_diff:
		core_index = (index % 12) - 1
		return coreFQS_inverted.get(core_index) + str(octave_number) + "#" 
	else:
		return coreFQS_inverted.get(index % 12) + str(octave_number)


#----------------------------------------------------------------#

tuning_freq_A4 = 440

def getNoteFreq(note_string):
	relative_index = getNoteIndex(note_string) - getNoteIndex('A4')
	note_freq = tuning_freq_A4 * (2**(relative_index/12))
	return note_freq


# A key is a set of notes which sound good together
# The words scale and key are sometimes used interchangeably
# Technically, a scale is a sequence of notes played in ..
# .. that order
# Root note can be note like "A4" or frequency like 440
# Returns all the scale notes' indexes as per MIDI convention
# Index 0 is 0 so as to match the standard indexing format in ..
# .. music theory. Here it will mean silence.
# Root note is either the index(as per MIDI convention) or note ..
# .. like "A4"
def getMajorKey(root_note):
	rn = root_note
	if type(root_note) == type("A4"):
		rn = getNoteIndex(root_note)

	return [0,
			rn,
			rn + 2,
			rn + 4,
			rn + 5,
			rn + 7,
			rn + 9,
			rn + 11,
			rn + 12]

def getMajorPentatonicKey(root_note):
	rn = root_note
	if type(root_note) == type("A4"):
		rn = getNoteIndex(root_note)

	return [0,
			rn,
			rn + 2,
			rn + 4,
			rn + 7,
			rn + 9,
			rn + 12]





























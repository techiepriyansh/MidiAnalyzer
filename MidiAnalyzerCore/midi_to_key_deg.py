import notes_to_midi as ntm
import frequencies as fqs
from mido import MidiFile
import sys
import os
import math

#------------------Getting Input--------------------------------
midi_file_path = sys.argv[1]
midi_track_index = int(sys.argv[2]) - 1




#-------------------Setting things up---------------------------
song = MidiFile(midi_file_path, clip=True)

raw_pn = song.tracks[midi_track_index]
pn = []									#Will contain a list of all the notes' midi index in the song

for msg in raw_pn:
	if msg.type == 'note_on':
		if msg.note >= 40 :	
			pn.append(msg.note)





#---------------------Finding Possible Root Notes----------------------------
#---------------------for the major key of the song--------------------------
pn_as_set = set(pn)
notes = (list(pn_as_set))
notes.sort()

			
permitted_diff = {0,2,4,5,7,9,11}	#permissible difference modulo 12 betwwen two notes if 
                                     #one note belongs to the major key the other

possible_root_notes=[]	

for root_note in notes:
	#Let that note be root note
	possible_root_notes.append(root_note)

	#Check if this note as root fits all other notes in its major key
	for s_note in notes:
		if  not (s_note - root_note) % 12 in permitted_diff :
			del possible_root_notes[-1]
			break





#----------------------Generating the Output File-------------------------------------
output_file_name = midi_file_path[:-4]+"_decoded.txt"		

if os.path.exists(output_file_name):				    #if an existing file with the name, delete it
	os.remove(output_file_name)

open(output_file_name,"w").close()						#create the file

for main_root_note in possible_root_notes:				 #write the key degrees with all possible root notes

	root_note_string = fqs.getNoteFromIndex(main_root_note)

	degrees = []
	coreDiffToDegrees = {
		0 : 1,
		2 : 2,
		4 : 3,
		5 : 4,
		7 : 5,
		9 : 6,
		11 : 7
	}

	for note in pn:
		difference = note - main_root_note
		octave_number = math.floor(difference/12)
		coreDiff = difference % 12
		coreDegree = coreDiffToDegrees[coreDiff]
		degree = octave_number * 7 + coreDegree
		degrees.append(degree)


	degrees_string = str(degrees)[1:-1].replace(",","")



	with open(output_file_name,"a") as f:
		f.write(root_note_string + "\n")
		f.write(degrees_string + "\n\n")
		f.close()







 
	


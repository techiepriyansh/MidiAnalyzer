import notes_to_midi as ntm
import frequencies as fqs
from mido import MidiFile
import math
import sys
import os


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

best_matches_till_now = [(0,0)]		#contains a tuple (root_note_midi_index, number_of_fits)
                                    #number_of_fits are always same for each element in the array   


for root_note in notes:
	#Let that note be root note
	#Check if this note as root fits all other notes in its major key
	number_of_fits = 0
	for s_note in notes:
		if (s_note - root_note) % 12 in permitted_diff :
			number_of_fits += 1

	if number_of_fits > best_matches_till_now[0][1]:
		best_matches_till_now = []
		best_matches_till_now.append((root_note,number_of_fits))
	elif number_of_fits == best_matches_till_now[0][1]:
		best_matches_till_now.append((root_note, number_of_fits))





#----------------------Generating the Output File-------------------------------------
output_file_name = midi_file_path[:-4]+"_decoded.txt"		

if os.path.exists(output_file_name):				    #if an existing file with the name, delete it
	os.remove(output_file_name)

with open(output_file_name,"w+") as f:					#create the file and write the track name
	f.write(song.tracks[midi_track_index].name + "\n\n")
	f.close

for main_root_note, n_o_f in best_matches_till_now:				 #write the key degrees with all possible root notes

	root_note_string = fqs.getNoteFromIndex(main_root_note)

	degrees = []
	coreDiffToDegrees = {
		0 : "1 ",
		1 : "1#",
		2 : "2 ",
		3 : "2#",
		4 : "3 ",
		5 : "4 ",
		6 : "4#",
		7 : "5 ",
		8 : "5#",
		9 : "6 ",
		10 : "6#",
		11 : "7 "
	}

	for note in pn:
		difference = note - main_root_note
		octave_number = math.floor(difference/12)
		coreDiff = difference % 12
		coreDegree = int(coreDiffToDegrees[coreDiff][0])
		baseDegree = octave_number * 7 + coreDegree                
		if baseDegree <= 0:                            #We defined scale degree number system as ... -2,-1,1,2,...
			baseDegree = baseDegree - 1                #Zero should not be there 
		degree = str(baseDegree) + coreDiffToDegrees[coreDiff][1]
		degrees.append(degree)


	degrees_string = str(degrees)[1:-1].replace(",","").replace("\'","")



	with open(output_file_name,"a") as f:
		f.write(root_note_string + "\n")
		f.write(degrees_string + "\n\n")
		f.close()







 
	


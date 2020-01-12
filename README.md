# MidiAnalyzer

Get the notes from a midi file as scale degrees of a major key.

A Web Application.


# MidiAnalyzerCore

A commandline utility to get the notes from a midi file as scale degrees.

**Quick Start**:

`python midi_decoder.py midi_file_path track_number`

*track_number ?* : A midi file consists of a number of tracks which are all played together to get the song.
                   track_number is simply the number of the track you want to get scale degrees of.
                   In most of the cases you might want to execute just by taking track_number as 1 , 2, 3 ... until you get the desired track.

This command will create a text file consisting of the output data.

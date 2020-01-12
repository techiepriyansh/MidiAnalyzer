import os
import midi_decoder
from bottle import template, request, route, run, static_file

@route('/')
def index():

	return static_file("index.html",root=".")

@route('/decoded', method = 'POST')
def get_midi_decoding_inputs():
	track_number_str = request.forms.get('track_number')
	midi_file_upload = request.files.get('upload')
	name, ext = os.path.splitext(midi_file_upload.filename)
	if not ext == '.mid':
		return "Invalid MIDI file extension"

	file_path = "midi_files/" + midi_file_upload.filename

	if os.path.exists(file_path):
		os.remove(file_path)

	midi_file_upload.save(file_path) 

	output_text = midi_decoder.decode_midi(file_path, int(track_number_str))
	return output_text

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8080))
	run(host='0.0.0.0', port=port, debug=True)

from database import *
from flask import *
import os
# from werkzeug import secure_filename
import face_recognition
import cv2
import numpy as np
import random
import PIL
from flask import request
from flask import jsonify
from flask import Flask, jsonify, request, redirect

PATH_MM = 'static/faces'
PATH_REC = 'static/recognize'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__)

app.config['SECRET_KEY'] = 'you-will-never-guess'

app.config['PATH_MM'] = PATH_MM
app.config['PATH_REC'] = PATH_REC

@app.route('/')
def welcome():
	return render_template("main.html")


@app.route("/ip", methods=["GET"])
def get_my_ip():
    ips = jsonify(request.remote_addr)
    return ips


@app.route('/identification_name.html', methods=['GET', 'POST'])
def matched_by_name():
	if request.method == 'GET':
		return render_template("identification_name.html")
	else:
		name_to = request.form['name']
		the_list = query_by_name(name_to)
		return render_template("matched_by_name.html", the_list=the_list, name_to=name_to)


@app.route('/matched_by_name.html')
def welcomen():
		return render_template("matched_by_name.html")


@app.route('/matched_by_picture.html')
def mathced_by_picture_moin():
	return render_template("matched_by_picture.html")



def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def upload_file(file):

    if file and allowed_file(file.filename):
#            filename = secure_filename(file.filename)
        filename = file.filename
        file.save(os.path.join(app.config['PATH_MM'], filename))

def save_file(file):

    if file and allowed_file(file.filename):
#            filename = secure_filename(file.filename)
        filename = file.filename
        image.save(r"C:\Users\moinm\OneDrive\Desktop\face_recognition\static\faces", filename)
        print("kos o5t lfun bere")





def moin_download(downlaoad_file):
	filename1 = downlaoad_file.filename
	downlaoad_file.save(os.path.join(app.config['PATH_MM'], filename1))
	iden_path = "static/faces/"+ filename1




@app.route('/error.html')
def couldnt_find_face():
	return render_template("error.html")

@app.route('/identification', methods=['GET', 'POST'])
def identification():
	if request.method =='POST':
		photo = request.files['ff']
		upload_file(photo)
		path1 = "static/faces/"+photo.filename
		known_image = face_recognition.load_image_file(path1)
		known_encoding = face_recognition.face_encodings(known_image)[0]
		people = query_all()
		for face in people:
			path = "static/faces/" + face.image
			unknown_image = face_recognition.load_image_file(path)
			unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
			results = face_recognition.compare_faces([known_encoding], unknown_encoding)
			if results[0]:
				return render_template('matched_by_picture.html', face=face)
			else:
				print("SORRY WE COULDN")
				return render_template("error.html")
	return render_template('identification.html')

@app.route('/add.html', methods=['GET','POST'])
def add_to_DB():
	if request.method == 'GET' :
		return render_template('add.html')
	else:
		name = request.form['name']
		image = request.files['ff']
		upload_file(image)
		description = request.form['description']
		name2 = request.form['name2']
		add_face(name,image.filename,description,name2)
		return redirect('/')


def rec():
	# Get a reference to webcam #0 (the default one)
	video_capture = cv2.VideoCapture(0)

	# Load a sample picture and learn how to recognize it.
	known_face_encodings=[]
	known_face_names=[]
	for face in query_all():
		path = "static/faces/"+face.image
		known_face_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(path))[0])
		known_face_names.append(face.name)	
	# Initialize some variables
	face_locations = []
	face_encodings = []
	face_names = []
	process_this_frame = True

	while True:
	    # Grab a single frame of video
	    ret, frame = video_capture.read()

	    # Resize frame of video to 1/4 size for faster face recognition processing
	    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

	    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
	    rgb_small_frame = small_frame[:, :, ::-1]

	    # Only process every other frame of video to save time
	    if process_this_frame:
	        # Find all the faces and face encodings in the current frame of video
	        face_locations = face_recognition.face_locations(rgb_small_frame)
	        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

	        face_names = []
	        for face_encoding in face_encodings:
	            # See if the face is a match for the known face(s)
	            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
	            name = "Unknown"

	            # # If a match was found in known_face_encodings, just use the first one.
	            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
	            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
	            best_match_index = np.argmin(face_distances)
	            if matches[best_match_index]:
	                name = known_face_names[best_match_index]

	            face_names.append(name)

	    process_this_frame = not process_this_frame


	    # Display the results
	    for (top, right, bottom, left), name in zip(face_locations, face_names):
	        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
	        top *= 4
	        right *= 4
	        bottom *= 4
	        left *= 4

	        # Draw a box around the face
	        cv2.rectangle(frame, (left, top), (right, bottom), ( random.randint(150,255), random.randint(150,255), random.randint(150,255)), 4)

	        # Draw a label with a name below the face
	        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (51,51,51), cv2.FILLED)
	        font = cv2.FONT_HERSHEY_DUPLEX
	        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255,255,255), 1)

	    # Display the resulting image
	    cv2.imshow('Video', frame)

	    # Hit 'q' on the keyboard to quit!
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break

	# Release handle to the webcam
	video_capture.release()
	cv2.destroyAllWindows()


@app.route('/detect.html', methods=['GET', 'POST'])
def open_webacm():
	rec()
	return redirect(url_for('welcome'))

if __name__ == '__main__':
  app.run(debug=True)
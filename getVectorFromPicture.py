import face_recognition 
import numpy as np 
import sys
import os
from pathlib import Path
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host':'localhost','port':9200}])

cwd = os.getcwd()
print("cwd: " + cwd)

# Get the images directory
rootdir = cwd + "/images"
print("rootdir: " + rootdir)

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        print(os.path.join(subdir, file))
        file_path = os.path.join(subdir, file)

        image = face_recognition.load_image_file(file_path)

        # detect the faces from the images
        face_locations = face_recognition.face_locations(image)

        # encode the 128-dimension face encoding for each face in the image
        face_encodings = face_recognition.face_encodings(image, face_locations)

        # Display the 128-dimension for each face detected
        for face_encoding in face_encodings:
            print("Face found ==>  ", face_encoding.tolist())
            print("name: " + Path(file_path).stem)
            name = Path(file_path).stem
            face_encoding = face_encoding.tolist()

            # format a dictionary to be indexed
            e = {
                "face_name": name,
                "face_encoding": face_encoding 
            }

            res = es.index(index = 'faces', doc_type ='_doc', body = e)
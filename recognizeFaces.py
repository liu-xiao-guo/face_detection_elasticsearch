import face_recognition
import numpy as np
from elasticsearch import Elasticsearch
import sys
import os

from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

cwd = os.getcwd()
# print("cwd: " + cwd)

# Get the images directory
rootdir = cwd + "/images_to_be_recognized"
# print("rootdir: {0}".format(rootdir))

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
        i = 0
        for face_encoding in face_encodings:
            i += 1
            print("Face", i)
            response = es.search(
                index="faces",
                body={
                    "size": 1,
                    "_source": "face_name",
                    "query": {
                        "script_score": {
                            "query": {
                                "match_all": {}
                            },
                            "script": {
                                "source": "cosineSimilarity(params.query_vector, 'face_encoding')",
                                "params": {
                                    "query_vector": face_encoding.tolist()
                                }
                            }
                        }
                    }
                }
            )

            # print(response)

            for hit in response['hits']['hits']:
                # double score=float(hit['_score'])
                print("score: {}".format(hit['_score']))
                if float(hit['_score']) > 0.92:
                    print("==> This face  match with ", hit['_source']['face_name'], ",the score is", hit['_score'])
                else:
                    print("==> Unknown face")

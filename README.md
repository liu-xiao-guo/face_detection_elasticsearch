This is a complete example for image recoginition based on the article at https://www.elastic.co/blog/how-to-build-a-facial-recognition-system-using-elasticsearch-and-python

The search is done through Elasticsearch

To get started, you can just simply run the following to index all of the pictures into Elasticsearch:

python3 getVectorFromPicture.py

In order to recognize the pictures, you can use the following command:

python3 recognizeFaces.py

This folder contains the code for the backend webservice

Currently the webservice supports 2 RESTfull API methods:

*Enroll* - to enroll a new user 

*Verify* - to obtain the score of the current image against the enrolled user

To perform the face recognition, [VGG Face Descriptor](http://www.robots.ox.ac.uk/~vgg/software/vgg_face/) built with Caffe is used.

## Instructions to deploy:

The caffe installation is assumed to be separate, however the code for obtaining the VGG features is part of the project.
Also the caffe model used can be found [here](https://drive.google.com/drive/folders/16xonkYUHWaVoQG_ZJkEkNjvuZvhSSko2?usp=sharing)

1) copy the contents of the vgg model to caffe-root/models/vgg_face_caffe
2) Update caffe_root @ projects/views.py to point to the correct path
3) create the folder project/data - this is where the backend service will store the enrolled data
4) Execute `python run.py` 
  
### ENROLL
url: http://localhost:5000/biosecure/api/v1/enroll

HTTP PUT multi-part request to be sent along with a json 
{image: binary_image_file}

Response will contain a json reporting the status of enrollment

### VERIFY
url: http://localhost:5000/biosecure/api/v1/verify

HTTP PUT multi-part request to be sent along with a json 
{image: binary_image_file}

Response will contain a json reporting the status. If successfull, it will contain a "score" key with the actual cosine distance 
Note that cosine distance is a measure of similarity and hence lower values mean better matches!

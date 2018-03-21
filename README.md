# BioSecure: Continous Authentication (Face)
This was developed to demonstrate continuous authentication as a viable authentication mechanism for mobile devices as part of GovernmentWare (GovWare) at [Singapore International Cyber Security Week 2017](https://www.sicw.sg/)

![alt text](https://github.com/div1090/BioSecure/blob/master/poster.PNG)


## Front-End

The app uses [Google's Mobile Vision API](https://developers.google.com/android/reference/com/google/android/gms/vision/face/package-summary) for Face Detection which is bundled with the front-end.
The code is based on this [sample code](https://github.com/googlesamples/android-vision/tree/master/visionSamples/FaceTracker) project with minor modifications made for UI.

## Back-End

A pre-trained [VGGFace](http://www.robots.ox.ac.uk/~vgg/software/vgg_face/) model built with caffe is for Face Recognition and served over REST API as the backend server.

### Deploy

The caffe installation is assumed to be separate, however the code for obtaining the VGG features is part of the project.
Also the caffe model used can be found [here](https://drive.google.com/open?id=0BzrIGPn419nlX20zUFZvWnl0aXc)

1. Copy the contents of the vgg model to caffe-root/models/vgg_face_caffe
2. Update caffe_root @ projects/views.py to point to the correct path
3. Create the folder project/data
   * this is where the backend service will store the enrolled data
4. Execute `python run.py` 

### APIs
* #### *ENROLL* - to enroll a new user 
  url: http://localhost:5000/biosecure/api/v1/enroll

  request: HTTP PUT multi-part request to be sent along with a json 
  {image: binary_image_file}

  response: contains a json reporting the status of enrollment

* ####  *VERIFY* - to obtain the score of the current image against the enrolled user
  url: http://localhost:5000/biosecure/api/v1/verify

  request: HTTP PUT multi-part request to be sent along with a json 
  {image: binary_image_file}

  response: contains a json reporting the status. If successfull, it will contain a "score" key with the actual cosine distance 
  Note that cosine distance is a measure of similarity and hence lower values mean better matches!

#### Contributors
Sanka Rasnayaka, Divya Sivasankaran

#### Contact
This was not meant to be a standalone project/app. If you are trying to adapt it for your own use case/facing issues with deploying or wish to share your comments/feedback, reach me at <div1090@gmail.com>.

#### [License](BioSecure/LICENSE.md)

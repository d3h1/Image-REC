# Backend Format
We use STATIC folder to:
    upload user files(images)
        uploaded files go into our Prediction model

We use APP.PY to:
    take the uploaded files 
        def predict()
            clothing_classifier_model_v2.h5
                OUTPUT
                IMAGE

# ACCURATE RATING so far
## 5/9 test photos are successful 
This is determined by the direction and clothing quality so far. 
    Next step is to use the image and direct the classifier to a certain part of the image to get more accurate readings
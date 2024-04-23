
from django.shortcuts import render, redirect
import cv2
import numpy as np
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from tensorflow.keras.models import load_model

# Load the trained emotion detection model
model = load_model("C:\\Users\\user\\Desktop\Python Project\emotion_detection_model.h5")

# Load the pre-trained face detector from OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Dictionary to map predicted labels to human-readable emotions
emotion_labels = {
    0: "Angry",
    1: "Disgust",
    2: "Fear",
    3: "Happy",
    4: "Neutral",
    5: "Sad",
    6: "Surprised"
}

# Function to preprocess the frame and perform emotion detection
def detect_emotion(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face_img = gray[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (48, 48))
        face_img = np.expand_dims(face_img, axis=0)
        face_img = np.expand_dims(face_img, axis=-1)
        face_img = face_img / 255.0

        # Make prediction
        prediction = model.predict(face_img)
        predicted_emotion = np.argmax(prediction)

        # Draw bounding box around the face and overlay emotion label
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, emotion_labels[predicted_emotion], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return frame

# Function to capture video from the camera and perform real-time emotion detection
def get_frame():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = detect_emotion(frame)
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# View to stream video with real-time emotion detection
@gzip.gzip_page
def video_feed(request):
    return StreamingHttpResponse(get_frame(), content_type="multipart/x-mixed-replace;boundary=frame")
def realtime_analyze_emotion(request):
     return render(request, 'realtime_analyze_emotion.html')
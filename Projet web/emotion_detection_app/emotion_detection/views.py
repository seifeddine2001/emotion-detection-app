
from django.shortcuts import render, redirect
from .forms import EmotionForm
from .models import Emotion
import cv2
import numpy as np
from tensorflow.keras.preprocessing import image # type: ignore
from tensorflow.keras.models import load_model # type: ignore

def detect_emotion(image_path):
    model = load_model("C:\Python Project\emotion_detection_model.h5")
    

    # Load and preprocess the image
    img = image.load_img(image_path, target_size=(48, 48), grayscale=True)
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    img_array = np.expand_dims(img_array, axis=-1)

    # Make predictions
    prediction = model.predict(img_array)[0]
    emotion_labels = {
        0: "Angry",
        1: "Disgust",
        2: "Fear",
        3: "Happy",
        4: "Neutral",
        5: "Sad",
        6: "Surprised"
    }
    predicted_emotion = emotion_labels[np.argmax(prediction)]
    return predicted_emotion

def analyze_emotion(request):
    if request.method == 'POST':
        form = EmotionForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded image
            form.save()

            # Get the path of the saved image
            image_path = form.instance.image.path

            # Analyze emotion using the model
            predicted_emotion = detect_emotion(image_path)

            # Update the model instance with the predicted emotion
            emotion = Emotion.objects.latest('id')
            emotion.predicted_emotion = predicted_emotion
            emotion.save()

            return redirect('result')
    else:
        form = EmotionForm()
    return render(request, 'analyze_emotion.html', {'form': form})

def show_result(request):
    emotion = Emotion.objects.latest('id')
    return render(request, 'result.html', {'emotion': emotion})


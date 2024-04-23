from django import forms
from .models import Emotion

class EmotionForm(forms.ModelForm):
    class Meta:
        model = Emotion
        fields = ['image']
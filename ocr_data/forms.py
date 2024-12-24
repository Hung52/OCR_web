# forms.py
from django import forms
from .models import AnnotatedImage

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = AnnotatedImage
        fields = ('image',)

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = AnnotatedImage
        fields = ('image',)
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'image': 'Tải ảnh lên',
        }
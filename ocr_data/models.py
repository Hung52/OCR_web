# models.py
from django.db import models
import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError

class AnnotatedImage(models.Model):
    image = models.ImageField(upload_to='annotated_images/')
    name = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or f"Image {self.id}"

class Region(models.Model):
    image = models.ForeignKey(AnnotatedImage, on_delete=models.CASCADE, related_name='regions')
    x = models.FloatField()
    y = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    label = models.CharField(max_length=255)

    def clean(self):
        if self.x < 0 or self.y < 0 or self.width <= 0 or self.height <= 0:
            raise ValidationError("Invalid region dimensions.")

class Annotation(models.Model):
    file = models.ForeignKey(AnnotatedImage, on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    shape_type = models.CharField(max_length=50)  # 'rectangle', 'polygon', etc.
    points = models.JSONField()  # Lưu tọa độ các điểm
    created_at = models.DateTimeField(auto_now_add=True)

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
@receiver(pre_delete, sender=Image)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        # Xóa tệp ảnh khỏi hệ thống tệp
        file_path = instance.image.path
        if os.path.isfile(file_path):
            os.remove(file_path)
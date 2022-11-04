from rest_framework import serializers
from generic.models import CompressedImage


class CompressedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompressedImage
        fields = ["image", "image_thumbnail"]

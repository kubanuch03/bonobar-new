from rest_framework import serializers
from .models import Gallery, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']


class GallerySerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(max_length=100000, allow_empty_file=False, use_url=False),
        write_only=True
    )
    image_set = ImageSerializer(source='images', many=True, read_only=True)

    class Meta:
        model = Gallery
        fields = ['id', 'title', 'description', 'images', 'image_set']

    def validate(self, data):
        images_data = data.get('images', [])
        if len(images_data) > 4:
            raise serializers.ValidationError("A gallery can only have a maximum of 4 images.")
        return data

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        gallery = Gallery.objects.create(**validated_data)
        for image_data in images_data:
            Image.objects.create(gallery=gallery, image=image_data)
        return gallery

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        if images_data:
            instance.images.all().delete()
            for image_data in images_data:
                Image.objects.create(gallery=instance, image=image_data)
        return instance

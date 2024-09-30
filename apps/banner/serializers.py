from rest_framework import serializers

from .models import BanerMain, BanerMiddle, BanerBook, BanerMainTopik
from validators.validator import validate_alphanumeric_and_symbols


class BanerTopikCreateSerializers(serializers.ModelSerializer):

    class Meta:
        model = BanerMainTopik
        fields = ['id','img','created_at']

    def validate(self, data):
        if BanerMainTopik.objects.count()>=3:
            raise serializers.ValidationError({"full":"Вы можете создать только 3 картинки банера"})
        
        return data

class BanerTopikUpdateSerializers(serializers.ModelSerializer):

    class Meta:
        model = BanerMainTopik
        fields = ['id','img','created_at']

  


class BanerListSerializers(serializers.ModelSerializer):
    topik_baner = BanerTopikCreateSerializers(many=True)
    class Meta:
        model = BanerMain
        fields = ['id','title','subtitle','topik_baner']

    def validate(self, data):
        if BanerMain.objects.count()>=1:
            raise serializers.ValidationError({"full":"Вы можете создать только 1 банер"})
        
        return data
    
class BanerUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = BanerMain
        fields = ['id','title','subtitle','topik_baner']

   
    

class BanerCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = BanerMain
        fields = ['id','title','subtitle','topik_baner']

    def validate(self, data):
        if BanerMain.objects.count()>=1:
            raise serializers.ValidationError({"full":"Вы можете создать только 1 банер"})
        
        return data

    def validate_title(self, value):
        return validate_alphanumeric_and_symbols(value)

    def validate_subtitle(self, value):
        return validate_alphanumeric_and_symbols(value)
    

    

# class BanerMiddleSerializers(serializers.ModelSerializer):

#     class Meta:
#         model = BanerMiddle
#         fields = ['id','title','img']


# class BanerBookSerializers(serializers.ModelSerializer):

#     class Meta:
#         model = BanerBook
#         fields = ['id','title','img']

    
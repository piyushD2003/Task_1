from rest_framework import serializers
# from .models import User, Doctor
from django.contrib.auth.hashers import make_password

# class Doctor_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = Doctor
#         fields = "__all__"

# class User_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id','username','email','password','Gender', 'DOB', 'number')
#         extra_kwargs = {
#             'password':{'write_only':True}
#         }

#     def create(self, validated_data):
#         user = User.objects.create(
#             username = validated_data['username'],
#             email=validated_data['email'],
#             password=make_password(validated_data['password']),
#             Gender =validated_data['Gender'],
#             DOB=validated_data['DOB'],
#             number=validated_data['number'],
                                   
#             )
        
#         return user
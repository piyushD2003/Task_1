from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets
from .models import User, Doctor
from .serializers import User_Serializer, Doctor_Serializer
from itsdangerous import URLSafeSerializer
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
import google.generativeai as genai
import PIL.Image
import json
# Create your views here.
Secret_key = "I am a good boy"

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = User_Serializer
    queryset = User.objects.all()
    print(queryset)
    @action(detail=False, methods=['post'])
    def Register(self, request, *args, **kwargs):
        userexist = User.objects.filter(email = request.data.get("email")).exists()
        serializer = User_Serializer(data=request.data)
        if serializer.is_valid() and not userexist:
            serializer.save()
            user = User.objects.get(email=request.data.get("email"))
            s = URLSafeSerializer(Secret_key)
            token = s.dumps({"user_id":user.id}, salt="activate")
            return Response(
                {
                    "token": token,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
                {"detail":"User already exist"},
                status = status.HTTP_208_ALREADY_REPORTED
            )
    
    @action(detail=False, methods=['post'])
    def Login(self, request, *args, **kwargs):
        print(request.data)
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
            print(user.id)
            print(check_password(password, user.password))
            if check_password(password, user.password):  # Use hashed password check with Django's methods in real scenarios
                s = URLSafeSerializer(Secret_key)
                token = s.dumps({"user_id":user.id}, salt="activate")
                print(token)

                return Response(
                    {
                    "detail": "Login successful",
                    "token": token,
                    "user": {"id": user.id, "name": user.username, "email": user.email},
                },
                    status=status.HTTP_200_OK,
                )
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = Doctor_Serializer
    queryset = Doctor.objects.all()
    print(queryset)
    @action(detail=False, methods=['post'])
    def Register(self, request, *args, **kwargs):
        userexist = Doctor.objects.filter(email = request.data.get("email")).exists()
        if not userexist:
            Doctor.objects.create(
                Doctorname=request.data.get('Doctorname'),
                email=request.data.get('email'),
                password=make_password(request.data.get('password')),
                Gender=request.data.get('Gender'),
                DOB=request.data.get('DOB'),
                number=request.data.get('number'),
                Medical_Degree=request.data.get('Medical_Degree'),
                University_Name=request.data.get('University_Name'),
                Graduation_Year=request.data.get('Graduation_Year'),
                Specialty=request.data.get('Specialty'),
                Address=request.data.get('Address'),
                Photo=request.FILES.get('Photo')
            )
            user = Doctor.objects.get(email=request.data.get("email"))
            s = URLSafeSerializer(Secret_key)
            token = s.dumps({"user_id":user.id}, salt="activate")
            return Response(
                {
                    "token": token,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
                {"detail":"Doctor already exist"},
                status = status.HTTP_208_ALREADY_REPORTED
            )
    
    @action(detail=False, methods=['post'])
    def Login(self, request, *args, **kwargs):
        print(request.data)
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = Doctor.objects.get(email=email)
            print(user.id)
            print(check_password(password, user.password))
            if check_password(password, user.password):  # Use hashed password check with Django's methods in real scenarios
                s = URLSafeSerializer(Secret_key)
                token = s.dumps({"user_id":user.id}, salt="activate")
                print(token)

                return Response(
                    {
                    "detail": "Login successful",
                    "token": token,
                    "user": {"id": user.id, "name": user.Doctorname, "email": user.email},
                },
                    status=status.HTTP_200_OK,
                )
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except Doctor.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        

    @action(detail=False, methods=['post'])
    def getdata(self, request, *args, **kwargs):
        Image = request.data.get("image")
        # organ = PIL.Image.open(Image)
        genai.configure(api_key="AIzaSyCebg0e7O3GuI-0_E5QBaI7kgsdsSVyJ88")
        model = genai.GenerativeModel("gemini-1.5-flash")
        organ = PIL.Image.open(Image)
        print(organ)
        response = model.generate_content(["give me the patient name, date (consider in right upper corner), pescription detail in medication:{ name and timing ( morning:true, afternoon: false, night:true)} in json, X indicate false, 1 indicate true written after the medication.", organ])
        print(type(response.text))
        json_str = response.text.strip().strip('```json').strip('```').strip()
        json_data = json.loads(json_str)
        print(type(json_data))
        return Response(json_data, status=status.HTTP_200_OK)
    
class imageprocess(viewsets.ViewSet):
    print("hello")
    @action(detail=False, methods=['post'])
    def getdata(self, request, *args, **kwargs):
        Image = request.data.get("image")
        # organ = PIL.Image.open(Image)
        genai.configure(api_key="AIzaSyCebg0e7O3GuI-0_E5QBaI7kgsdsSVyJ88")
        model = genai.GenerativeModel("gemini-1.5-flash")
        organ = PIL.Image.open(Image)
        print(organ)
        response = model.generate_content(["give me the patient name, date (consider in right upper corner), pescription detail in medication:{ name and timing ( morning:true, afternoon: false, night:true)} in json, X indicate false, 1 indicate true written after the medication.", organ])
        print(type(response.text))
        json_str = response.text.strip().strip('```json').strip('```').strip()
        json_data = json.loads(json_str)
        print(type(json_data))
        return Response(json_data, status=status.HTTP_200_OK)
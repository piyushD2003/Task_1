from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets
from .models import Records
# from .serializers import User_Serializer, Doctor_Serializer
from itsdangerous import URLSafeSerializer
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
import google.generativeai as genai
import PIL.Image
import json
# Create your views here.
Secret_key = "I am a good boy"

# class UserViewSet(viewsets.ModelViewSet):
#     serializer_class = User_Serializer
#     queryset = User.objects.all()
#     print(queryset)
#     @action(detail=False, methods=['post'])
#     def Register(self, request, *args, **kwargs):
#         userexist = User.objects.filter(email = request.data.get("email")).exists()
#         serializer = User_Serializer(data=request.data)
#         if serializer.is_valid() and not userexist:
#             serializer.save()
#             user = User.objects.get(email=request.data.get("email"))
#             s = URLSafeSerializer(Secret_key)
#             token = s.dumps({"user_id":user.id}, salt="activate")
#             return Response(
#                 {
#                     "token": token,
#                 },
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(
#                 {"detail":"User already exist"},
#                 status = status.HTTP_208_ALREADY_REPORTED
#             )
    
#     @action(detail=False, methods=['post'])
#     def Login(self, request, *args, **kwargs):
#         print(request.data)
#         email = request.data.get("email")
#         password = request.data.get("password")

#         try:
#             user = User.objects.get(email=email)
#             print(user.id)
#             print(check_password(password, user.password))
#             if check_password(password, user.password):  # Use hashed password check with Django's methods in real scenarios
#                 s = URLSafeSerializer(Secret_key)
#                 token = s.dumps({"user_id":user.id}, salt="activate")
#                 print(token)

#                 return Response(
#                     {
#                     "detail": "Login successful",
#                     "token": token,
#                     "user": {"id": user.id, "name": user.username, "email": user.email},
#                 },
#                     status=status.HTTP_200_OK,
#                 )
#             return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
#         except User.DoesNotExist:
#             return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
# class DoctorViewSet(viewsets.ModelViewSet):
#     serializer_class = Doctor_Serializer
#     queryset = Doctor.objects.all()
#     print(queryset)
#     @action(detail=False, methods=['post'])
#     def Register(self, request, *args, **kwargs):
#         userexist = Doctor.objects.filter(email = request.data.get("email")).exists()
#         if not userexist:
#             Doctor.objects.create(
#                 Doctorname=request.data.get('Doctorname'),
#                 email=request.data.get('email'),
#                 password=make_password(request.data.get('password')),
#                 Gender=request.data.get('Gender'),
#                 DOB=request.data.get('DOB'),
#                 number=request.data.get('number'),
#                 Medical_Degree=request.data.get('Medical_Degree'),
#                 University_Name=request.data.get('University_Name'),
#                 Graduation_Year=request.data.get('Graduation_Year'),
#                 Specialty=request.data.get('Specialty'),
#                 Address=request.data.get('Address'),
#                 Photo=request.FILES.get('Photo')
#             )
#             user = Doctor.objects.get(email=request.data.get("email"))
#             s = URLSafeSerializer(Secret_key)
#             token = s.dumps({"user_id":user.id}, salt="activate")
#             return Response(
#                 {
#                     "token": token,
#                 },
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(
#                 {"detail":"Doctor already exist"},
#                 status = status.HTTP_208_ALREADY_REPORTED
#             )
    
#     @action(detail=False, methods=['post'])
#     def Login(self, request, *args, **kwargs):
#         print(request.data)
#         email = request.data.get("email")
#         password = request.data.get("password")

#         try:
#             user = Doctor.objects.get(email=email)
#             print(user.id)
#             print(check_password(password, user.password))
#             if check_password(password, user.password):  # Use hashed password check with Django's methods in real scenarios
#                 s = URLSafeSerializer(Secret_key)
#                 token = s.dumps({"user_id":user.id}, salt="activate")
#                 print(token)

#                 return Response(
#                     {
#                     "detail": "Login successful",
#                     "token": token,
#                     "user": {"id": user.id, "name": user.Doctorname, "email": user.email},
#                 },
#                     status=status.HTTP_200_OK,
#                 )
#             return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
#         except Doctor.DoesNotExist:
#             return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        

#     @action(detail=False, methods=['post'])
#     def getdata0(self, request, *args, **kwargs):
#         Image = request.data.get("image")
#         # organ = PIL.Image.open(Image)
#         genai.configure(api_key="AIzaSyCebg0e7O3GuI-0_E5QBaI7kgsdsSVyJ88")
#         model = genai.GenerativeModel("gemini-1.5-flash")
#         organ = PIL.Image.open(Image)
#         print(organ)
#         response = model.generate_content(["give me the patient name, date (consider in right upper corner), pescription detail in medication:{ name and timing ( morning:true, afternoon: false, night:true)} in json, X indicate false, 1 indicate true written after the medication.", organ])
#         print(type(response.text))
#         json_str = response.text.strip().strip('```json').strip('```').strip()
#         json_data = json.loads(json_str)
#         print(type(json_data))
#         return Response(json_data, status=status.HTTP_200_OK)
    
class imageprocess(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def getdata(self, request, *args, **kwargs):

        Image = request.data.get("image")
        genai.configure(api_key="AIzaSyCebg0e7O3GuI-0_E5QBaI7kgsdsSVyJ88")
        model = genai.GenerativeModel("gemini-1.5-flash")
        organ = PIL.Image.open(Image)
        print(organ)
        response = model.generate_content([
            '''Extract the following details from the given prescription image:

                1. Patient Name: Extract the name of the patient mentioned.
                2. Date: Extract the date in the format (YYYY-MM-DD).
                3. Medications: For each medication, extract its name and dosage timing.

                Guidelines for determining medication timing:
                - The timing of the dosage is written after the medication name in the format (morning-afternoon-night), such as '1 -- (unrecognized character or symbol or anything) -- 1'. 
                - Multiple variations are possible, including:
                a. x-x-x / 1-x-x / x-1-x / x-x-1 / 1-1-x / 1-x-1 / x-1-1 
                b. 1----------0---------1 / 0----------0---------1 / 0-----------1--------0 
                c. x-----------x------------x / x----------x---------1 / x----------1-----------x / 1-----------x----------x 
                or any variations thereof.
                - Use these rules to determine the boolean values for timing:
                - Any digit (e.g., 1, 1/2, 2) = true (indicates the medication is taken at this time).
                - Any symbol (e.g., x, 0, >) = false (indicates the medication is not taken at this time).

                Handle potential cursive handwriting where characters may appear connected or ambiguous. Preprocess the image to enhance clarity and separation of characters if necessary. Account for common misinterpretations where 'x' may look like '>', and ensure accurate interpretation based on context. Include potential variations like '1------x------1', '1--0--1', and other similar patterns to ensure robust handling of different styles. Utilize image processing techniques like binarization, noise removal, and character separation to improve the clarity and accuracy of the handwritten text extraction.

                Provide the result in this exact JSON format:
                {
                    "patient_name": "Extracted Name",
                    "date": "YYYY-MM-DD",
                    "medications": [
                        {
                            "name": "Medication Name",
                            "timing": {
                                "morning": true/false,
                                "afternoon": true/false,
                                "night": true/false
                            }
                        },
                        ...
                    ]
                }
                Ensure accuracy in interpreting the timing, handle potential cursive handwriting, and extract only the required details.

            ''', organ])
        print(type(response.text))
        json_str = response.text.strip().strip('```json').strip('```').strip()
        json_data = json.loads(json_str)
        print(type(json_data))
        print(json_data['patient_name'])
        print(json_data['date'])
        print(json_data['medications'])
        Records.objects.create(
            patient_name = json_data['patient_name'] or"NA",
            date = json_data['date'] or "1111-02-10",
            medication = json_data['medications'] or "NA",
        )

        return Response(json_data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def getdata0(self, request, *args, **kwargs):
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
        Records.objects.create(
            patient_name = json_data['patient_name'],
            date = json_data['date'],
            medication = json_data['medications'],
        )
        return Response(json_data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def getdata1(self, request, *args, **kwargs):

        Image = request.data.get("image")
        genai.configure(api_key="AIzaSyCebg0e7O3GuI-0_E5QBaI7kgsdsSVyJ88")
        model = genai.GenerativeModel("gemini-1.5-pro")
        organ = PIL.Image.open(Image)
        print(organ)
        response = model.generate_content([
            '''Extract the following details from the given prescription image:

                1. Patient Name: Extract the name of the patient mentioned.
                2. Date: Extract the date in the format (YYYY-MM-DD).
                3. Medications: For each medication, extract its name and dosage timing.

                Guidelines for determining medication timing:
                - The timing of the dosage is written after the medication name in the format (morning-afternoon-night), such as '1 -- (unrecognized character or symbol or anything) -- 1'. 
                - Multiple variations are possible, including:
                a. x-x-x / 1-x-x / x-1-x / x-x-1 / 1-1-x / 1-x-1 / x-1-1 
                b. 1----------0---------1 / 0----------0---------1 / 0-----------1--------0 
                c. x-----------x------------x / x----------x---------1 / x----------1-----------x / 1-----------x----------x 
                or any variations thereof.
                - Use these rules to determine the boolean values for timing:
                - Any digit (e.g., 1, 1/2, 2) = true (indicates the medication is taken at this time).
                - Any symbol (e.g., x, 0, >) = false (indicates the medication is not taken at this time).

                Handle potential cursive handwriting where characters may appear connected or ambiguous. Preprocess the image to enhance clarity and separation of characters if necessary. Account for common misinterpretations where 'x' may look like '>', and ensure accurate interpretation based on context. Include potential variations like '1------x------1', '1--0--1', and other similar patterns to ensure robust handling of different styles. Utilize image processing techniques like binarization, noise removal, and character separation to improve the clarity and accuracy of the handwritten text extraction.

                Provide the result in this exact JSON format:
                {
                    "patient_name": "Extracted Name",
                    "date": "YYYY-MM-DD",
                    "medications": [
                        {
                            "name": "Medication Name",
                            "timing": {
                                "morning": true/false,
                                "afternoon": true/false,
                                "night": true/false
                            }
                        },
                        ...
                    ]
                }
                Ensure accuracy in interpreting the timing, handle potential cursive handwriting, and extract only the required details.

            ''', organ])
        print(type(response.text))
        json_str = response.text.strip().strip('```json').strip('```').strip()
        json_data = json.loads(json_str)
        print(type(json_data))

        print(json_data['patient_name'])
        print(json_data['date'])
        print(json_data['medications'])

        Records.objects.create(
            patient_name = json_data['patient_name'],
            date = json_data['date'],
            medication = json_data['medications'],
        )

        return Response(json_data, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['post'])
    def getdata2(self, request, *args, **kwargs):

        Image = request.data.get("image")
        genai.configure(api_key="AIzaSyCebg0e7O3GuI-0_E5QBaI7kgsdsSVyJ88")
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        organ = PIL.Image.open(Image)
        print(organ)
        response = model.generate_content([
            '''Extract the following details from the given prescription image:

                1. Patient Name: Extract the name of the patient mentioned.
                2. Date: Extract the date in the format (YYYY-MM-DD).
                3. Medications: For each medication, extract its name and dosage timing.

                Guidelines for determining medication timing:
                - The timing of the dosage is written after the medication name in the format (morning-afternoon-night), such as '1 -- (unrecognized character or symbol or anything) -- 1'. 
                - Multiple variations are possible, including:
                a. x-x-x / 1-x-x / x-1-x / x-x-1 / 1-1-x / 1-x-1 / x-1-1 
                b. 1----------0---------1 / 0----------0---------1 / 0-----------1--------0 
                c. x-----------x------------x / x----------x---------1 / x----------1-----------x / 1-----------x----------x 
                or any variations thereof.
                - Use these rules to determine the boolean values for timing:
                - Any digit (e.g., 1, 1/2, 2) = true (indicates the medication is taken at this time).
                - Any symbol (e.g., x, 0, >) = false (indicates the medication is not taken at this time).

                Handle potential cursive handwriting where characters may appear connected or ambiguous. Preprocess the image to enhance clarity and separation of characters if necessary. Account for common misinterpretations where 'x' may look like '>', and ensure accurate interpretation based on context. Include potential variations like '1------x------1', '1--0--1', and other similar patterns to ensure robust handling of different styles. Utilize image processing techniques like binarization, noise removal, and character separation to improve the clarity and accuracy of the handwritten text extraction.

                Provide the result in this exact JSON format:
                {
                    "patient_name": "Extracted Name",
                    "date": "YYYY-MM-DD",
                    "medications": [
                        {
                            "name": "Medication Name",
                            "timing": {
                                "morning": true/false,
                                "afternoon": true/false,
                                "night": true/false
                            }
                        },
                        ...
                    ]
                }
                Ensure accuracy in interpreting the timing, handle potential cursive handwriting, and extract only the required details.

            ''', organ])
        print(type(response.text))
        json_str = response.text.strip().strip('```json').strip('```').strip()
        json_data = json.loads(json_str)
        print(type(json_data))

        print(json_data['patient_name'])
        print(json_data['date'])
        print(json_data['medications'])

        Records.objects.create(
            patient_name = json_data['patient_name'],
            date = json_data['date'],
            medication = json_data['medications'],
        )
        return Response(json_data, status=status.HTTP_200_OK)
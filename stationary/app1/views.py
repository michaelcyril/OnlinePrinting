from urllib import response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import render,redirect
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializer import UserSerializer
from django.contrib.auth import authenticate, login, logout
from .token import get_user_token
from .models import *
from django.db.models import Q

# Create your views here.

@api_view(["POST", "GET"])
@permission_classes([AllowAny])
def RegisterUser(request):
    if request.method == "POST":
        data = request.data
        username = data['username']
        # user = None
        user = User.objects.filter(username=username)
        if user:
            message = {'message': 'user does exist'}
            return Response(message)

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            message = {'save': True}
            return Response(message)
        else:
            message = {'save': False}
            return Response(message)
    return Response({'message': "hey bro"})


# {
#     "first_name":"mike",
#     "last_name":"cyril",
#     "username":"mike",
#     "email":"mike@gmail.com",
#     "password":"123",
#     "phone":"11111111",
#     "type":"owner"
# }

@api_view(["POST"])
@permission_classes([AllowAny])
def LoginView(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        user_id = User.objects.values('id').get(username=username)['id']
        # profile_id = Profile.objects.values('id', 'ward_id', 'user_id', 'phone', 'description').get(user_id=user_id)

        response = {
            'msg': 'success',
            # 'profile_id': profile_id,
            'token': get_user_token(user),
        }

        return Response(response)
    else:
        response = {
            'msg': 'Invalid username or password',
        }

        return Response(response)

# {
#     "username": "mike",
#     "password": "123"
# }


@api_view(["GET"])
@permission_classes([AllowAny])
def stationery_list(request):
    stationeries = Stationery.objects.values("id", "name", "logo", "description", "user_id").all()
    response = {
        'data': stationeries
    }
    return Response(response)

  

@api_view(["POST"])
@permission_classes([AllowAny])
def create_stationery(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        logo = request.POST.get('logo')
        description = request.POST.get('description')
        location= request.POST.get('location')
        # price = request.POST.get('price')
        user_id= User.objects.get(id=request.POST.get('user_id'))
        
        # creating saving the stationery 
        stationery = Stationery.objects.create(name=name, logo=logo, description=description, location=location, created_by=user_id)
        stationery.save()
        response = {
            "message":"created successfully"
        }
        return Response(response)

# {
#     "name":"miko"
#     "logo":""
#     "description":"karibu sana"
    
# }

def calculate_cost(pages, no_copies, price):
    total_cost = int(price) * int(pages) * int(no_copies)

    return total_cost
     

@api_view(["POST"])
@permission_classes([AllowAny])
def create_doc(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        pages = request.POST.get('pages')
        file_doc=request.POST.get('file_doc')
        no_copies = request.POST.get('no_copies')
        user_id = User.objects.get(id=request.POST.get('user_id'))
        stationery_id = Stationery.objects.get(id=request.POST.get('stationery_id'))
        price = Cost.objects.values('print_cost').get(Q(stationery_id=stationery_id) and Q(is_active=True))['print_cost']
        total_cost = calculate_cost(pages, no_copies, price)
       
        document = Document.objects.create( name=name, pages=pages, file_doc=file_doc, no_copies=no_copies, user_id=user_id, stationery_id=stationery_id, total_cost=total_cost, )
        document.save()
        response = {
            'message': "create successfully"
            
        }
        return Response(response)

@api_view(["POST"])
@permission_classes([AllowAny])
def document_list(request):
    if request.method=='POST':
        stationery_id = Stationery.objects.get(id=request.POST.get('stationery_id'))
        documents = Document.objects.values('id', 'name', 'pages', 'no_copies', 'total_cost', 'status').filter(stationery_id=stationery_id)
    
    response ={
        'data' : documents
    }
    
    return Response(response)

# {
#     "stationary_id": 1
# }
@api_view(["POST"])
@permission_classes([AllowAny])
def update_status_printed(request):
    doc_id = request.data['doc_id']
    obj = Document.objects.get(id=doc_id)
    if obj.status == "pending":
        obj.status = "printed"
        obj.save()
        return Response({"message": "success"})
    
# {
#     "doc_id":1
# } 

@api_view(["POST"])
@permission_classes([AllowAny])
def update_status_taken(request):
    doc_id = request.data['doc_id']
    obj = Document.objects.get(id=doc_id)
    
    if obj.status == "printed":
        obj.status = "taken"
        obj.save()
        return Response({"message": "success"})



# {
#     "doc_id":1
# } 

        

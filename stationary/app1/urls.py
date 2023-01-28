from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views
app_name = 'app1'

urlpatterns = [
    path('register', RegisterUser),
    path('login', LoginView),
    path('refresh_token', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('newstationery',create_stationery ),
    path('stationerylist',stationery_list),
    path('document', create_doc),
    path('printed', update_status_printed),
    path('taken', update_status_taken),
    
    path('documents', document_list, name='document_list'),
    path('documents_ofst', document_list, name='document_list_by_stationery'),
]

# first URL pattern matches requests to /documents/ and passes them to the document_list view without a stationery id. The second URL pattern matches 
# requests to /documents/<int:stationery_id>/ and passes them to the document_list view along with the stationery id captured from the URL.
# Please note that this is just a basic example and you should also handle validation, error handling and security concerns in your production code.





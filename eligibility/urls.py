from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('form/', views.eligibility_form, name='eligibility_form'),
    path('submit/', views.submit, name='submit'),  
    path('chat/', views.chatbot_page, name='chatbot_page'),
    path("chatbot_ask/", views.chatbot_ask, name="chatbot_ask"),
     path('upload/', views.upload_document, name='upload_document'),

]
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect

from boards import views

urlpatterns = [
	path('', lambda request: redirect('boards/', permanent=True)),
	path('boards/', views.boards, name='boards'),
	path('boards/<pk>/', views.board_topics, name='board_topics'),
	path('boards/<pk>/new/', views.new_topic, name='new_topic'),
    path('admin/', admin.site.urls)    
]

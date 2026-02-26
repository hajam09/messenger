from django.urls import path

from core.views import (
    loginView,
    registerView,
    logoutView,
    chatListView,
    chatView,
)

app_name = 'core'

urlpatterns = [
    path('login/', loginView, name='login-view'),
    path('register/', registerView, name='register-view'),
    path('logout/', logoutView, name='logout-view'),
    path('', chatListView, name='chat-list-view'),
    path('chat/<int:room_id>/', chatView, name='chat-view')
]

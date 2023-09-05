from django.urls import path
from .views import login, chatbot, flot, index, morris, query, tables, redirect, logout
urlpatterns = [
    path('', redirect),
    path('login', login),
    path('chatbot', chatbot),
    path('flot', flot),
    path('index', index),
    path('morris', morris),
    path('query', query),
    path('tables', tables),
    path('logout', logout)
]
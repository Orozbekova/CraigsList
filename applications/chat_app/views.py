from django.shortcuts import render
from .models import Group,Chat

# Create your views here.

def index_view(request,group_name):
    group,created = Group.objects.get_or_create(name=group_name)
    chats = Chat.objects.filter(group=group)
    context = {
        "chats":chats,
    }
    return render(request, 'chat_app/index.html',context)

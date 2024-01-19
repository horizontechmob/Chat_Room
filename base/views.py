from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Room, Topic
from .forms import RoomForm
from django.db.models import Q


def home(request):
    q = request.GET.get('q')
    
    # Check if q is not None before using it in filter conditions
    if q is not None:
        rooms = Room.objects.filter(Q(topic__name__icontains=q) | 
                                    Q(name__icontains=q) |
                                    Q(description__icontains=q)
                                   )
    else:
        # If q is None, return all rooms
        rooms = Room.objects.all()
        
    room_count = rooms.count()

    topics = Topic.objects.all()
    context = {'rooms': rooms, 
               'topics': topics,
               'room_count' : room_count}
    return render(request, 'base/home.html', context)




def room(request, pk):
      room = Room.objects.get(id = pk)         
      context = {'room': room} 

      return render(request, 'base/room.html', context)


def createRoom(request):
     form = RoomForm()
     if request.method == 'POST':
          print(request.POST)
          form = RoomForm(request.POST)
          if form.is_valid():
               form.save()
               return redirect('home') #name of the url
          
     context = {'form': form}
     return render(request, 'base/room_form.html', context)


def updateRoom(request, pk):
     room = Room.objects.get(id=pk)
     form = RoomForm(instance=room)
     if request.method == 'POST':
          form = RoomForm(request.POST, instance=room)
          if form.is_valid():
               form.save()
               return redirect('home') #name of the url
     context = {'form' : form}
     return render(request, 'base/room_form.html', context)



def deleteRoom(request, pk):
     room = Room.objects.get(id=pk)
     if request.method == 'POST':
          room.delete()
          return redirect('home') #name of the url
     
     return render(request, 'base/delete.html', {'obj': room})

def loginPage(request):
     context = {}
     return(request, 'base/login_request.html', context)
     
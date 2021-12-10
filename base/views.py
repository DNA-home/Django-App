from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Room,Message,Topic
from .forms import RoomForm




def about(request):
    return render(request,'about.html')



def loginPage(request):
    page="login"

    if request.user.is_authenticated:
        return redirect('home')


    if request.method=="POST":
        username=request.POST.get('username').lower()
        password=request.POST.get("password")

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"user doesn't exist")

        user= authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'username or password does not exist')



    context={'page':page}
    return render(request,'login_register.html',context)



def logoutUser(request):
    logout(request)
    return redirect('home')



def registerPage(request):
    form=UserCreationForm()

    if request.method == "POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username=user.username.lower()
            user.save() 
            login(request,user)
            return redirect('home')

        else:
            messages.error(request,"an error occurred during registration.")

    return render(request,'login_register.html',{'form':form})




def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''

    

    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )

    
    messages=Message.objects.filter(Q(room__topic__name__icontains=q))


    topics=Topic.objects.all()
    

    room_count=rooms.count()


    context={'rooms':rooms,"topics":topics, 'room_count':room_count,
    'tot_messages': messages,'topic_count':topics.count()}
    return render(request,'base/home.html',context)



def room(request,pk):
    room=Room.objects.get(id=pk)
    messages=room.message_set.all().order_by('-created')
    participants=room.participants.all()

    if request.method == "POST":
        msg= Message.objects.create(
            user = request.user,
            room=room,
            body= request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)





    context={"room":room,"room_messages": messages,'participants':participants}
    return render(request,'base/room.html',context)



@login_required(login_url='/login')
def createRoom(request):
    topics=Topic.objects.all()
    form=RoomForm()

    if request.method =='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            room= form.save(commit=False)
            room.host=request.user
            room.save()
            return redirect('home')


    context={'form':form,'topics':topics}
    return render(request,'room_form.html',context)



@login_required(login_url='/login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You aren't allowed here mate")


    if request.method =='POST':
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,"room_form.html",context)



@login_required(login_url='/login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)

    if request.method=="POST":
        room.delete()
        return redirect('home')

    # context={}
    return render(request,"delete.html",{'obj':room})




@login_required(login_url='/login')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)


    if request.method=="POST":
        message.delete()
        return redirect('home')
    return render(request,'delete.html',{'obj':message})





# @login_required(login_url='/login')
def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()

    topics=Topic.objects.all()
    messages=user.message_set.all()

    # if user.id != request.id:
    #     return HttpResponse("YOU ARE NOT ALLOWED HERE.GO BACK!!!!!")

    

    context={'user':user,'rooms':rooms,'topics':topics,'tot_messages':messages}
    return render(request,'profile.html',context)
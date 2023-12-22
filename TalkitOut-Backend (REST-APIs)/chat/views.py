# from django.shortcuts import render
# from django.contrib.auth.models import User
from blog.models import Friend, Group
import hashlib
import urllib
import base64

# from .models import ChatMessage

# Create your views here.
# #for chatting
# from django.http import HttpResponse
# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
# from .models import ChatRoom, Message, UserInChatRoom
# from django.db.models import Q
# from django.core.exceptions import ObjectDoesNotExist
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# # chatroom


# def chatroom(request):
#     if request.user.is_authenticated:
#         chatrooms = ChatRoom.objects.all()
#         return render(request, 'chatroom/chatroom.html', {'chatrooms': chatrooms})
#     else:
#         return redirect('/login')

# def chatroom_create(request):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             name = request.POST['name']
#             description = request.POST['description']
#             chatroom = ChatRoom(name=name, description=description)
#             chatroom.save()
#             messages.success(request, 'Chatroom created successfully')
#             return redirect('/chatroom')
#         else:
#             return render(request, 'chatroom/chatroom_create.html')
#     else:
#         return redirect('/login')

# def chatroom_edit(request, id):
#     if request.user.is_authenticated:
#         chatroom = ChatRoom.objects.get(id=id)
#         if request.method == 'POST':
#             name = request.POST['name']
#             description = request.POST['description']
#             chatroom.name = name
#             chatroom.description = description
#             chatroom.save()
#             messages.success(request, 'Chatroom updated successfully')
#             return redirect('/chatroom')
#         else:
#             return render(request, 'chatroom/chatroom_edit.html', {'chatroom': chatroom})
#     else:
#         return redirect('/login')

# def chatroom_delete(request, id):
#     if request.user.is_authenticated:
#         chatroom = ChatRoom.objects.get(id=id)
#         chatroom.delete()
#         messages.success(request, 'Chatroom deleted successfully')
#         return redirect('/chatroom')
#     else:
#         return redirect('/login')

# def chatroom_join(request, id):
#     if request.user.is_authenticated:
#         chatroom = ChatRoom.objects.get(id=id)
#         user = User.objects.get(id=request.user.id)
#         user_in_chatroom = UserInChatRoom(user=user, chatroom=chatroom)
#         user_in_chatroom.save()
#         messages.success(request, 'You have joined the chatroom')
#         return redirect('/chatroom')
#     else:
#         return redirect('/login')

# def chatroom_leave(request, id):
#     if request.user.is_authenticated:
#         chatroom = ChatRoom.objects.get(id=id)
#         user = User.objects.get(id=request.user.id)
#         user_in_chatroom = UserInChatRoom.objects.get(user=user, chatroom=chatroom)
#         user_in_chatroom.delete()
#         messages.success(request, 'You have left the chatroom')
#         return redirect('/chatroom')
#     else:
#         return redirect('/login')

# def chatroom_view(request, id):
#     if request.user.is_authenticated:
#         chatroom = ChatRoom.objects.get(id=id)
#         user = User.objects.get(id=request.user.id)
#         user_in_chatroom = UserInChatRoom.objects.get(user=user, chatroom=chatroom)
#         messages = Message.objects.filter(chatroom=chatroom)
#         return render(request, 'chatroom/chatroom_view.html', {'chatroom': chatroom, 'messages': messages, 'user_in_chatroom': user_in_chatroom})
#     else:
#         return redirect('/login')

# def chatroom_message(request, id):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             chatroom = ChatRoom.objects.get(id=id)
#             user = User.objects.get(id=request.user.id)
#             user_in_chatroom = UserInChatRoom.objects.get(user=user, chatroom=chatroom)
#             message = request.POST['message']
#             message = Message(chatroom=chatroom, message=message)
#             message.save()
#             return redirect('/chatroom/' + str(id))
#         else:
#             return redirect('/chatroom/' + str(id))
#     else:
#         return redirect('/login')

# def chatroom_message_delete(request, id, message_id):
#     if request.user.is_authenticated:
#         message = Message.objects.get(id=message_id)
#         message.delete()
#         messages.success(request, 'Message deleted successfully')
#         return redirect('/chatroom/' + str(id))
#     else:
#         return redirect('/login')

# def chatroom_message_edit(request, id, message_id):
#     if request.user.is_authenticated:
#         message = Message.objects.get(id=message_id)
#         if request.method == 'POST':
#             message.message = request.POST['message']
#             message.save()
#             messages.success(request, 'Message updated successfully')
#             return redirect('/chatroom/' + str(id))
#         else:
#             return render(request, 'chatroom/chatroom_message_edit.html', {'message': message})
#     else:
#         return redirect('/login')

# def chatroom_search(request):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             query = request.POST['query']
#             chatrooms = ChatRoom.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
#             return render(request, 'chatroom/chatroom_search.html', {'chatrooms': chatrooms})
#         else:
#             return render(request, 'chatroom/chatroom_search.html')
#     else:
#         return redirect('/login')

# def chatroom_user(request, id):
#     if request.user.is_authenticated:
#         chatroom = ChatRoom.objects.get(id=id)
#         user_in_chatroom = UserInChatRoom.objects.filter(chatroom=chatroom)
#         return render(request, 'chatroom/chatroom_user.html', {'user_in_chatroom': user_in_chatroom})
#     else:
#         return redirect('/login')

# def chatroom_user_delete(request, id, user_id):
#     if request.user.is_authenticated:
#         user = User.objects.get(id=user_id)
#         chatroom = ChatRoom.objects.get(id=id)
#         user_in_chatroom = UserInChatRoom.objects.get(user=user, chatroom=chatroom)
#         user_in_chatroom.delete()
#         messages.success(request, 'User deleted successfully')
#         return redirect('/chatroom/' + str(id) + '/user')
#     else:
#         return redirect('/login')
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from users.models import Profile
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.text import slugify


@login_required(login_url="login")
def HomePage(request):
    request.user.profile.lastseen = timezone.now()
    return render(request, "home.html")


def SignupPage(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        email = request.POST.get("email")
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")

        if User.objects.filter(username=uname).exists():
            return HttpResponse(f"A user with username '{uname}' already exists!")
        if pass1 != pass2:
            return HttpResponse("Passwords do not match!")

        my_user = User.objects.create_user(uname, email, pass1)
        my_user.save()
        return redirect("login")

    return render(request, "signup.html")


def LoginPage(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        passwd = request.POST.get("pass")
        user = authenticate(request, username=uname, password=passwd)
        request.user.profile.lastseen = timezone.now()
        if user is not None:
            login(request, user)
            print(f"{user.get_username()} is signed")
            return redirect("home")
        else:
            return HttpResponse("Username or Password is incorrect!")
    return render(request, "login.html")


@login_required(login_url="login")
def LogoutPage(request):
    logout(request)
    return redirect("login")


def index(request):
    return render(request, "index.html")


def getHash(s):
    s_norm = s.lower().strip()
    return hashlib.sha256(s_norm.encode("utf-8")).hexdigest()


def getFriendFromHash(hash, current_user, friends):
    for friendId in friends:
        friend = User.objects.get(pk=friendId)
        if (
            getHash(
                min(friend.email, current_user.email)
                + "_"
                + max(friend.email, current_user.email)
            )
            == hash
        ):
            return friend
    return None
def getFriendsRoomNames(current_user, friends):
    friends_roomnames = {}
    for friendId in friends:
        friend = User.objects.get(pk=friendId)
        friends_roomnames[friend.username]=getHash(
                min(friend.email, current_user.email)
                + "_"
                + max(friend.email, current_user.email)
            )
    return friends_roomnames

def getOthersRoomNames(current_user, others):
    others_roomnames = {}
    for otherUser in others:
        others_roomnames[otherUser.username]=getHash(
                min(otherUser.email, current_user.email)
                + "_"
                + max(otherUser.email, current_user.email)
            )
    return others_roomnames


@login_required(login_url="login")
def room(request, room_name):
    request.user.profile.lastseen = timezone.now()
    request.user.profile.save()
    messages = ChatMessage.objects.filter(chatroom_name=room_name).order_by("timestamp")

    for message in messages:
        message.is_expired()
    context = {"room_name": room_name, "messages": messages}
    if request.user.is_authenticated:
        request.user.profile.lastseen = timezone.now()
        request.user.profile.save()
        current_user = request.user
        friends = Friend.objects.filter(user=current_user).values_list(
            "friend", flat=True
        )
        context["friends_roomname"] = getFriendsRoomNames(current_user, friends)

        context["currentChatFriend"] = getFriendFromHash(
            room_name, current_user, friends
        )
        context["isGroup"] = False
        if(context["currentChatFriend"]==None):
            context["currentChatFriend"] = urllib.parse.unquote(base64.b64decode(room_name))

        others = User.objects.exclude(pk=current_user.id).exclude(pk__in=friends)
        groups = Group.objects.filter(
            members=current_user
        )  # Get groups the user is a part of
        context["friends"] = Friend.objects.filter(user=current_user)
        context["others_list"] = others
        context["others_roomname"] = getOthersRoomNames(current_user, others)
        context["groups"] = groups  # Add groups to the context
        friends_lastseen = Profile.objects.filter(
            user__in=friends.values_list("friend", flat=True)
        ).values("user__username", "lastseen")
        context["friends_lastseen"] = friends_lastseen
    return render(request, "chatroom.html", context)


@login_required(login_url="login")
def export_chat(request, room_name):
    messages = ChatMessage.objects.filter(chatroom_name=room_name).order_by("timestamp")
    txt = ""
    for msg in messages:
        txt += f"{msg.sender_username}@{msg.timestamp}: {msg.message_content}\n"
    # print(txt)
    response = HttpResponse(txt, content_type="text/plain")
    response["Content-Disposition"] = f"attachment; filename={slugify(room_name)}.txt"
    return response


@login_required(login_url="login")
def edit_chat(request, msg_id):
    # Check if the current user is the sender of the message
    message = get_object_or_404(ChatMessage, message_id=msg_id)
    request.user.profile.lastseen = timezone.now()
    request.user.profile.save()
    if request.user.username == message.sender_username:
        if request.method == "POST":
            new_content = request.POST.get("editContent")
            delete_duration = request.POST.get("deleteDuration")

            # Update the message content
            message.message_content = new_content

            if delete_duration == "forever":
                message.time = None  # Set to retain forever
            else:
                message.time = int(delete_duration) * 3600
            message.is_expired()
            message.save()

            return redirect("room", room_name=message.chatroom_name)

        else:
            context = {
                "msg_id": message.message_id,
                "chatroom_name": message.chatroom_name,
                "sender_username": message.sender_username,
                "content": message.message_content,
                "time": message.time,
            }

            return render(request, "edit_chat.html", context)

    else:
        return redirect("blog-home")


@login_required(login_url="login")
def delete_chat(request, msg_id):
    message = get_object_or_404(ChatMessage, message_id=msg_id)
    request.user.profile.lastseen = timezone.now()
    request.user.profile.save()
    if request.user.username == message.sender_username:
        chat_room = message.chatroom_name
        message.delete()
        return redirect("room", room_name=chat_room)
    else:
        return redirect("blog-home")


def link(request, msg_id):
    # print("hii")
    message = get_object_or_404(ChatMessage, message_id=msg_id)
    request.user.profile.lastseen = timezone.now()
    request.user.profile.save()
    link = str(message).split("~link~")[-1]
    if not link.startswith("http"):
        link = '<script>window.location="%s";</script>' % (
            "http://127.0.0.1:8000" + link
        )
    else:
        link = '<script>window.location="%s";</script>' % link
    print("link: ", link)
    return HttpResponse(link)


@login_required
def dashboard(request):
    return render(request, "dashboard.html", {"name": request.user.first_name})


@login_required
def videocall(request):
    return render(
        request,
        "videocall.html",
        {"name": request.user.first_name + " " + request.user.last_name},
    )


@login_required
def join_room(request):
    if request.method == "POST":
        roomID = request.POST["roomID"]
        return redirect("/meeting?roomID=" + roomID)
    return render(request, "joinroom.html")

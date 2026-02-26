import secrets

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from core.forms import LoginForm, RegistrationForm
from core.models import Room


def loginView(request):
    if request.user.is_authenticated:
        return redirect("core:chat-list-view")

    if request.method == "POST":
        form = LoginForm(request.POST, request=request)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("core:chat-list-view")
    else:
        form = LoginForm(request=request)

    return render(request, "core/login.html", {"form": form})


def registerView(request):
    if request.user.is_authenticated:
        return redirect("core:chat-list-view")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("core:chat-list-view")
    else:
        form = RegistrationForm()

    return render(request, "core/register.html", {"form": form})


@login_required
def logoutView(request):
    logout(request)
    return redirect("core:login-view")


@login_required
def chatListView(request):
    rooms = Room.objects.filter(user_1=request.user) | Room.objects.filter(user_2=request.user)

    if request.method == "POST":
        other_username = request.POST.get("username", "").strip()
        if other_username and other_username != request.user.username:
            try:
                other_user = User.objects.get(username=other_username)
                user_1, user_2 = sorted([request.user, other_user], key=lambda u: u.id)
                room, created = Room.objects.get_or_create(user_1=user_1, user_2=user_2)
                if created or not room.secret:
                    room.secret = secrets.token_urlsafe(32)
                    room.save(update_fields=["secret"])
                return redirect("core:chat-view", room_id=room.id)
            except User.DoesNotExist:
                messages.error(request, "User not found.")
        else:
            messages.error(request, "Please enter a valid username.")

    return render(request, "core/home.html", {"rooms": rooms})


@login_required
def chatView(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if not room.secret:
        room.secret = secrets.token_urlsafe(32)
        room.save(update_fields=["secret"])
    return render(request, "core/chat.html", {"room": room})


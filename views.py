from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import login
from .forms import UsernamePasswordResetForm

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Movies Store'
    return render(request, 'home/index.html', {'template_data': template_data})

def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html', {'template_data': template_data})

def reset_password_view(request):
    """ Step 1: Enter username to verify identity """
    if request.method == "POST":
        form = UsernamePasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)
            request.session['reset_user_id'] = user.id  # Store user ID in session
            return redirect('set_new_password')  # Redirect to new password form
    else:
        form = UsernamePasswordResetForm()
    return render(request, 'home/reset_password.html', {'form': form})

def set_new_password_view(request):
    """ Step 2: Set new password after verifying username """
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('reset_password')

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            del request.session['reset_user_id']  # Remove user ID from session
            login(request, user)  # Log user in after reset
            return redirect('/')  # Redirect to home page
    else:
        form = SetPasswordForm(user)

    return render(request, 'home/set_new_password.html', {'form': form})

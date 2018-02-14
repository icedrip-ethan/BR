from django.shortcuts import render, redirect
from accounts.forms import (
  RegistrationForm,
  EditProfileForm,
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, authenticate, login
# from django.contrib.auth.decorators import login_required


def index(request):
  return render(request, 'accounts/index.html')

def register(request):
  if request.method=='POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      new_user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password1'])
      login(request, new_user)
      return redirect('accounts:view_profile')
  else:
    form = RegistrationForm()
    args = {'form': form}
    return render(request, 'accounts/reg_form.html', args)


def view_profile(request):
  args = {'user': request.user}
  return render(request, 'accounts/profile.html', args)


def edit_profile(request):
  if request.method == 'POST':
    form = EditProfileForm(data=request.POST, instance=request.user)

    if form.is_valid():
      form.save()
      return redirect('accounts:view_profile')
  else:
    form = EditProfileForm(instance=request.user)
    args = {'form':form}
    return render(request, 'accounts/edit_profile.html', args)


def change_password(request):
  if request.method == 'POST':
    form = PasswordChangeForm(data=request.POST, user=request.user)

    if form.is_valid():
      form.save()
      # to keep user logged in after redirect
      update_session_auth_hash(request, form.user)
      return redirect('accounts:view_profile')
    else:
      return redirect('accounts:change-password')
  else:
    form = PasswordChangeForm(user=request.user)
    args = {'form':form}
    return render(request, 'accounts/change_password.html', args)

from django.shortcuts import render, redirect
from accounts.forms import (
  RegistrationForm,
  EditProfileForm,
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib import messages
# from django.contrib.auth.decorators import login_required


def index(request):
  return render(request, 'accounts/index.html')

def register(request):
  if request.method=='POST':
    form = RegistrationForm(request.POST)
    print(request.POST)
    if form.is_valid():
      form.save()
      new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
      login(request, new_user)
      return redirect('accounts:view_profile')
    else:
      # clean the data (?)
      username = form['username'].value()
      if User.objects.filter(username=username).exists():
        messages.add_message(request, messages.ERROR, 'username exists')
        return render(request, 'accounts/reg_form.html')
  else:
    form = RegistrationForm()
    args = {'form': form}
    return render(request, 'accounts/reg_form.html', args)


def view_profile(request):
  args = {'user': request.user}
  return render(request, 'accounts/profile.html', args)


def edit_profile(request):
  if request.method == 'POST':
    if 'old_password' in request.POST:
      form = PasswordChangeForm(data=request.POST, user=request.user)
      if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        # success msg
        return redirect('accounts:view_profile')
      else:
        # add error
        return redirect('accounts:edit_profile')

    else:  
      form = EditProfileForm(data=request.POST, instance=request.user)
      if form.is_valid():
        form.save()
        #success msg
        return redirect('accounts:view_profile')
      else:
        # add error
        return redirect('accounts:edit_profile')

  else:
    return render(request, 'accounts/edit_profile.html')

def change_password(request):
  if request.method == 'POST':
    form = PasswordChangeForm(data=request.POST, user=request.user)
    print(request.POST)
    print('old_password' in request.POST)
    if form.is_valid():
      form.save()
      # to keep user logged in after redirect
      update_session_auth_hash(request, form.user)
      return redirect('accounts:view_profile')
    else:
      return redirect('accounts:change-password')
  else:
    return render(request, 'accounts/change_password.html')
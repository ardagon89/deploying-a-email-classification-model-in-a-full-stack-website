from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import  messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, FileUploadForm
from .functions.functions import get_results, upload_files

# Create your views here.
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileUpdateForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            email = user_form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                user_form.add_error("email", ValidationError('Another user exists with the same email!', 'duplicate_email'))
            else:
                user = user_form.save()
                profile_form = ProfileUpdateForm(request.POST, instance=user.profile)
                profile_form.save()
                username = user_form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}!. Please log in.')
                return redirect('login')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileUpdateForm()
    return render(request, 'users/register.html', {'user_form':user_form, 'profile_form':profile_form})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'users/profile.html', {'user_form':user_form, 'profile_form':profile_form})

@login_required
def classify(request):
    
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            upload_files(request.FILES.getlist('file'), request.user.id)
            messages.success(request, f'File(s) successfully uploaded!')
            return redirect('result')
    else:
        form = FileUploadForm()
    return render(request, 'users/classify.html', {'form':form})

@login_required
def result(request):
    
    result = get_results(request)

    return render(request, 'users/result.html', {'result': result})
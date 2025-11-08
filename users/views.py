from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib.auth import authenticate, login, logout # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore
from .forms import RegisterUserForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.decorators import login_required  # type: ignore
from django.utils.http import url_has_allowed_host_and_scheme

# Create your views here.

def loginUser(request):
    # Get the 'next' parameter from the GET request, e.g., /login/?next=/some/url/
    next_page = request.GET.get('next')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        # Get 'next' from the form's hidden input on POST
        next_page = request.POST.get('next')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Security check: Ensure the redirect URL is on the same host
            if next_page and url_has_allowed_host_and_scheme(url=next_page, allowed_hosts={request.get_host()}):
                return redirect(next_page)
            else:
                return redirect('forums')  # Default redirect
        else:
            messages.error(request, "Invalid username or password.")
            # Pass next_page back to the template on failed login
            return render(request, 'userPages/login.html', {'next': next_page})

    # Pass the 'next' parameter to the template context on GET request
    return render(request, 'userPages/login.html', {'next': next_page})
    
def logoutUser(request):
    logout(request)
    messages.success(request, ("Logged out successfully."))
    return redirect('forums')

def registerUser(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, ("Registration successful"))
            return redirect('forums')
    else:
        form = RegisterUserForm()
        for field_name in form.fields:
            form.fields[field_name].help_text = None

    return render(request, 'userPages/register.html' ,{'form':form})

@login_required
def showProfile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, ("Updated Succesfully! "))
            return redirect('yourProfile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'u_form': u_form,
        'p_form': p_form  
        }
    return render(request,"profilePages/yourProfile.html", context)

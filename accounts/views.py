#from django.contrib import messages
from django.contrib.auth import login, authenticate
from .form import SignUpForm
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            #messages.info(request, "Successfully logged in!")
            return redirect('login')

        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
            args = {'form': form}
            return render(request, 'registration/signup.html', args)
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form':form})

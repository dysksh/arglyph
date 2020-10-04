from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        # fields = ('email', 'password1', 'password2')
        fields = ('username', 'email', 'password1', 'password2')
        # fields = UserCreationForm.Meta.fields + ('middle_name',)


def signup(request):
    if request.user.is_authenticated:
        return redirect('argument-home')
    else:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = CustomUserCreationForm()
        return render(request, 'account/signup.html', {'form': form})
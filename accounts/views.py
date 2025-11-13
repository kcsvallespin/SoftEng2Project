from .forms import UsernamePasswordResetForm
# Custom password reset view using username
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def password_reset_by_username(request):
    message = None
    show_password_fields = False
    username_value = None
    form = None
    if request.method == 'POST':
        if 'username' in request.POST and 'password1' not in request.POST:
            # Step 1: username submitted
            form = UsernamePasswordResetForm(request.POST)
            if form.is_valid():
                users = form.get_users()
                if users.exists():
                    show_password_fields = True
                    username_value = form.cleaned_data['username']
                else:
                    message = "No user found with that username."
            else:
                message = "Please enter a valid username."
        elif 'username' in request.POST and 'password1' in request.POST:
            # Step 2: new password submitted
            username_value = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if not password1 or not password2 or password1 != password2:
                message = "Passwords do not match."
                show_password_fields = True
            else:
                User = get_user_model()
                users = User.objects.filter(username__iexact=username_value)
                if users.exists():
                    user = users.first()
                    user.set_password(password1)
                    user.save()
                    from django.urls import reverse
                    from django.shortcuts import redirect
                    return redirect(reverse('account_login'))
                else:
                    message = "No user found with that username."
    else:
        form = UsernamePasswordResetForm()
    return render(request, 'account/password_reset_username.html', {
        'form': form if not show_password_fields else None,
        'message': message,
        'show_password_fields': show_password_fields,
        'username_value': username_value,
    })
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_POST

from django import forms

class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            self.add_error('password2', "Passwords do not match.")
        return cleaned_data

@user_passes_test(lambda u: u.is_staff)
def create_user(request):
    message = None
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            User = get_user_model()
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                form.add_error('username', 'Username already exists.')
            else:
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1']
                )
                message = f"User '{user.username}' created successfully."
                form = CreateUserForm()  # reset form
    else:
        form = CreateUserForm()
    return render(request, 'account/create_user.html', {'form': form, 'message': message})

def load_users(request):
    User = get_user_model()
    query = request.GET.get('search', '').strip()
    users = User.objects.all()
    if query:
        users = users.filter(username__icontains=query)
    # Sort staff first, then by username
    users = sorted(users, key=lambda u: (not u.is_staff, u.username.lower()))
    return render(request, 'account/users-list.html', {'users': users, 'search': query})

@user_passes_test(lambda u: u.is_staff)
@require_POST
def delete_user(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    if not user.is_superuser:
        user.delete()
        return redirect('load_users')

# Block/unblock user view
@user_passes_test(lambda u: u.is_staff)
@require_POST
def block_user(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    if not user.is_superuser:
        user.is_blocked = not user.is_blocked
        user.save()
        return redirect('load_users')
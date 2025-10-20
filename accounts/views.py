from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


@login_required
def home(request):
    from django.shortcuts import redirect
    return redirect('curriculum_list')


@login_required
def settings(request):
    return render(request, 'accounts/settings.html')

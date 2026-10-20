from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import RegisterForm
from .services import ApiError, search_games


def home(request):
    return render(request, 'home.html')


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Cuenta creada. Ya puedes iniciar sesión.')
        return redirect('login')
    return render(request, 'register.html', {'form': form})


@login_required
def games(request):
    query = request.GET.get('q', '').strip()[:50]
    error, items = None, []
    try:
        items = search_games(query)
    except ApiError as exc:
        error = str(exc)
    return render(request, 'games.html', {'games': items, 'error': error, 'q': query})

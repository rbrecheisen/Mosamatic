from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest

from ..managers.logmanager import LogManager


def is_auto_refresh(request):
    return True if request.GET.get('auto-refresh', '0') == '1' else False


@login_required
def auth(_) -> HttpResponse:
    return HttpResponse(status=200)


@login_required
def custom_logout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('/')


def help(request):
    return render(request, 'help/index.html')


def go_back(request):
    history = request.session.get('history', None)
    if history:
        history.pop()
        if history:
            request.session['history'] = history
            return redirect(history[-1])
    return redirect('/help/')


def help_page(request, page):
    if page == 'None' or page is None:
        page = 'index'
    return render(request, f'help/{page}.html', context={'previous': request.GET.get('previous', None)})


@login_required
def logs(request: HttpRequest) -> HttpResponse:
    manager = LogManager()
    if request.method == 'POST':
        manager.delete_messages()
    return render(request, 'logs.html', context={'messages': manager.get_messages()})
from django.shortcuts import HttpResponse, render, Http404
from .models import Board
from datetime import datetime


def index(request):
    if request.method == 'GET':
        order_by = request.GET.get('order_by', 'create_date')
        search = request.GET.get('search', '')
        boards = Board.objects.filter(name__icontains=search).order_by('-{}'.format(order_by))
        context = {'boards': boards}
        return render(request, 'dashboard/index.html', context)
    elif request.method == 'POST':
        name = request.POST.get('name', None)
        slug = "{}-{}".format(name.lower().replace(' ','-'), datetime.today())
        new_board = Board.objects.create(name=name, slug=slug)
        context = {'message': 'Created!'}
        return render(request, 'dashboard/index.html', context)
    else:
        return Http404('Not allowed')




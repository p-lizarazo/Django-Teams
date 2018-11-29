import sys
sys.path.append("..")
from django.shortcuts import HttpResponse, render, Http404, redirect
from .models import Board, Column, Task
from datetime import datetime
from team.models import Team
from django.template import RequestContext


def index(request):
    if request.method == 'GET':
        order_by = request.GET.get('order_by', 'create_date')
        search = request.GET.get('search', '')
        boards = Board.objects.filter(team__users__username=request.user.username)
        context = {'boards': boards}
        return render(request, 'dashboard/dashboard.html', context)
    elif request.method == 'POST':
        name = request.POST.get('name', None)
        slug = "{}-{}".format(name.lower().replace(' ','-'), datetime.today())
        new_board = Board.objects.create(name=name, slug=slug)
        context = {'message': 'Created!'}
        return render(request, 'dashboard/dashboard.html', context)
    else:
        return Http404('Not allowed')


def board(request, id):
    if request.method == 'GET':
        my_board = Board.objects.get(id=id)
        columns = Column.objects.filter(board=id)
        context = {'columns': columns, 'id': id}
        return render(request, 'dashboard/columns.html', context)


def board_create(request):
    if request.method == 'GET':
        username = request.user.username
        context = {'teams': Team.objects.filter(users__username=username)}
        return render(request, 'dashboard/create_board.html', context)
    elif request.method == 'POST':
        name = request.POST.get('name')
        team_id = request.POST.get('teams')
        new_board = Board.objects.create(name=name, team=Team.objects.get(id=team_id))
        return redirect('board_index')


def column_create(request, id):
    if request.method == 'GET':
        return render(request, 'dashboard/column_create.html', {})
    elif request.method == 'POST':
        name = request.POST.get('name')
        Column.objects.create(name=name, board=Board.objects.get(id=id))
        return redirect('board', id=id)


def task_create(request,id, column_id):
    if request.method == 'GET':
        return render(request, 'dashboard/task_create.html', {})
    elif request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('comment')
        Task.objects.create(title=title, description=description, column=Column.objects.get(id=column_id))

        return redirect('tasks', id=id, column_id=column_id)


def task_modify(request,id, column_id,task_id):
    if request.method == 'GET':
        pass


def task_delete(request,id,column_id,task_id):
    if request.method == 'GET':
        Task.objects.get(id=task_id).delete()
        return redirect('tasks', id=id, column_id=column_id)


def tasks(request, id, column_id):
    if request.method == 'GET':
        column = Column.objects.get(id=column_id)
        context = {'tasks': column.task_set.all(), 'id': id, 'column_id': column_id}
        return render(request, 'dashboard/tasks.html', context)

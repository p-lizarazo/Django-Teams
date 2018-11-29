from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Team
from django.contrib.auth.models import User


def index(request):
    if request.method == 'GET':
        username = request.user.username
        teams = Team.objects.filter(users__username=username)
        context = {'teams': teams}
        return render(request, 'team/team.html', context)


def create(request):
    if request.method == 'GET':
        users = User.objects.exclude(id=request.user.id)
        context = {'users': users}
        return render(request, 'team/create.html', context)
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        team_users = request.POST.getlist('team_users')
        new_team = Team(name=team_name)
        new_team.save()
        new_team.users.add(request.user.id)
        for i in team_users:
            new_team.users.add(int(i))
        new_team.save()
        return redirect('index')


def modify(request, id):
    team = Team.objects.get(id=id)
    if request.method == 'GET':
        users_id = [x.id for x in team.users.all()]
        users_nselected = User.objects.exclude(id__in=users_id)
        context = {'team': team, 'users_nselected': users_nselected}
        return render(request, 'team/modify.html', context)
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        team_users = request.POST.getlist('team_users')
        team.name = team_name
        team.users.clear()
        team.save()
        team.users.add(request.user.id)
        for i in team_users:
            team.users.add(int(i))
        team.save()
        return redirect('index')

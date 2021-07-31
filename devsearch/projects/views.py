from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project
from .forms import ProjectForm, ReviewForm

from .utils import searchProjects, paginateProjects

def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 2)
    context = {
        'projects' :    projects,
        'search_query': search_query,
        # 'paginator':    paginator,
        'custom_range': custom_range
    }
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()
    tags = projectObj.tags.all()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()
        projectObj.getVoteCount
        messages.success(request, 'Your review was successfully added')
        return redirect('project', pk=projectObj.id)
        
    context = {
        'project' : projectObj,
        'tags' : tags,
        'form' : form
    }
    return render(request, 'projects/single-projects.html', context)

@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')
    context = {
        'form' : form
    }
    return render(request, "projects/project_form.html", context)

@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    projectObj = profile.project_set.get(id=pk)
    form = ProjectForm(instance=projectObj)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=projectObj)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {
        'form' : form
    }
    return render(request, "projects/project_form.html", context)

@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    projectObj = profile.project_set.get(id=pk)
    if request.method == 'POST':
        projectObj.delete()
        return redirect('projects')
    context = {
        'project' : projectObj,
    }
    return render(request, "delete_template.html", context)
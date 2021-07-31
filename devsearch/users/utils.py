from django.db.models import Q
from .models import Profile, Skill
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProfiles(request, profiles, results):
    page = request.GET.get('page')

    paginator = Paginator(profiles, results)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)
    
    
    left_Index = int(page) - results
    if left_Index < 1 :
        left_Index = 1
    
    right_index = int(page) + results +1
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1
    
    custom_range = range(left_Index, right_index)
    return custom_range, profiles

def searchProfiles(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    skills = Skill.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query) | 
                                                 Q(short_intro__icontains=search_query) | 
                                                 Q(skill__in=skills))
    return profiles, search_query
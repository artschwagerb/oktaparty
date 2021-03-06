from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.contrib import messages
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from .okta import OktaTools

from .models import OktaGroup

# Create your views here.
@login_required
def index(request):
    """View function for home page of site."""
    
    context = {

    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'groups/index.html', context=context)

# @vary_on_headers('Cookie')
# @cache_page(60 * 15)
@login_required
def group_yours(request):
    """List Groups."""

    okta = OktaTools()
    if request.user.okta_id:
        user_groups = okta.user_groups(request.user.okta_id)
        user_group_ids = [g['id'] for g in user_groups]
        user_group_list = OktaGroup.objects.filter(okta_id__in=user_group_ids)
    else:
        user_group_list = []
        user_group_ids = []

    group_list = OktaGroup.objects.filter(Q(allow_join=True) | Q(allow_leave=True), ~Q(okta_id__in=user_group_ids))
    
    context = {
        "group_list": group_list,
        "user_group_list": user_group_list,
        "user_group_ids": user_group_ids,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'groups/group_yours.html', context=context)

@login_required
def group_join(request,group_id):
    """Join Group"""
    if request.method == "GET":
        try:
            okta_group = OktaGroup.objects.get(pk=group_id)

        except OktaGroup.DoesNotExist:
            raise Http404("OktaGroup does not exist")
        
        context = {
            'okta_group': okta_group,
        }

        return render(request, 'groups/group_join.html', context)
    
    elif request.method == "POST":
        try:
            okta_group = OktaGroup.objects.get(pk=group_id)
            
            if not okta_group.allow_join:
                raise Http404("Not Allowed to Join.")
            if not request.user.okta_id:
                raise Http404("User missing okta_id.")

            okta_group.join(request.user)
        
        except OktaGroup.DoesNotExist:
            raise Http404("OktaGroup does not exist")
            
        next_url = request.GET.get("next",None)
        if next_url:
            return redirect(next_url)
        else:
            return redirect('okta:group-list')

@login_required
def group_leave(request,group_id):
    """Leave Group"""
    if request.method == "GET":
        try:
            okta_group = OktaGroup.objects.get(pk=group_id)

        except OktaGroup.DoesNotExist:
            raise Http404("OktaGroup does not exist")
        
        context = {
            'okta_group': okta_group,
        }

        return render(request, 'groups/group_leave.html', context)

    elif request.method == "POST":
        try:
            okta_group = OktaGroup.objects.get(pk=group_id)

            if not okta_group.allow_leave:
                raise Http404("Not Allowed to Leave.")
            if not request.user.okta_id:
                raise Http404("User missing okta_id.")

            okta_group.leave(request.user)
        
        except OktaGroup.DoesNotExist:
            raise Http404("OktaGroup does not exist")

        next_url = request.GET.get("next",None)
        if next_url:
            return redirect(next_url)
        else:
            return redirect('okta:group-list')

@login_required
@permission_required('okta.task_sync_okta_groups')
def TaskSyncOktaGroups(request):
    from okta.tasks import okta_group_sync

    t = okta_group_sync.delay()
    messages.success(request, 'Started Okta Group Sync - TaskId: %s' % (t.id))

    next_url = request.GET.get("next",None)
    if next_url:
        return redirect(next_url)
    else:
        return redirect('okta:group-list')

@login_required
def group_list(request):
    """List Groups."""

    okta = OktaTools()

    group_list = OktaGroup.objects.filter(Q(hidden=False))
    
    context = {
        "group_list": group_list,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'groups/group_list.html', context=context)
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.contrib import messages

from .lib.okta import OktaTools

from .models import OktaGroup

# Create your views here.
@login_required
def index(request):
    """View function for home page of site."""
    
    context = {

    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'groups/index.html', context=context)

@login_required
def group_list(request):
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
    return render(request, 'groups/group_list.html', context=context)

@login_required
def group_sync(request):
    """Sync Groups."""

    okta = OktaTools()

    okta_groups = okta.groups()

    for g in okta_groups:
        group_item, group_created = OktaGroup.objects.get_or_create(okta_id=g['id'],
            defaults={
                'name': g['profile']['name'],
                'description': g['profile'].get('description',None),
                'profile': g['profile'],
                'source_type': g['type'],
                'source_system': g['objectClass'][0]
            }
        )
        if group_created:
            print("Group Created: %s" % (group_item))
        else:
            group_item.name = g['profile']['name']
            group_item.description = g['profile'].get('description', None)
            group_item.profile = g['profile']
            group_item.source_type = g['type']
            group_item.source_system = g['objectClass'][0]
            
            group_item.save()

            print("Group Updated: %s" % (group_item))
    
    context = {
        "group_list": group_list,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'groups/group_list.html', context=context)

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
        return redirect('okta:index')
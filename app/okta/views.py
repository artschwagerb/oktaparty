from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count, Q, Sum
from django.contrib import messages
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from .okta import OktaTools

from users.models import User
from .models import OktaGroup, OktaUser
from .forms import GroupEditForm

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
        print(user_groups)
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

# @vary_on_headers('Cookie')
# @cache_page(60 * 15)
@login_required
def group_owned(request):
    """Owned Groups."""

    okta = OktaTools()
    if request.user.email:
        groups_owned_list = OktaGroup.objects.filter(profile__owners__contains=request.user.email)

        group_role_list = groups_owned_list.filter(profile__type="role")
        group_other_list = groups_owned_list.exclude(pk__in=group_role_list.values_list('id'))
    else:
        user_group_list = []
        user_group_ids = []

    group_list = OktaGroup.objects.none()
    
    context = {
        "group_role_list": group_role_list,
        "group_other_list": group_other_list,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'groups/group_owned.html', context=context)

@login_required
def group_roles(request):
    """Role Groups."""

    okta = OktaTools()

    group_role_list = OktaGroup.objects.filter(profile__type="role")
    
    context = {
        "group_role_list": group_role_list,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'groups/group_roles.html', context=context)

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
def group_edit(request,group_id):
    """Edit Group"""
    if request.method == "GET":
        try:
            okta_group = OktaGroup.objects.get(pk=group_id)

        except OktaGroup.DoesNotExist:
            raise Http404("OktaGroup does not exist")
        
        form = GroupEditForm(instance=okta_group)
        
        context = {
            'okta_group': okta_group,
            'form': form,
        }

        return render(request, 'groups/group_edit.html', context)
    
    elif request.method == "POST":
        try:
            okta_group = OktaGroup.objects.get(pk=group_id)

        except OktaGroup.DoesNotExist:
            raise Http404("OktaGroup does not exist")
        
        form = GroupEditForm(request.POST, instance=okta_group)

        if form.is_valid():
            # process
            form.save()
            next_url = request.GET.get("next",None)
            if next_url:
                return redirect(next_url)
            else:
                return redirect('okta:group-list')

@login_required
def group_view(request,group_id):
    """View Group"""
    if request.method == "GET":
        try:
            okta_group = OktaGroup.objects.get(pk=group_id)

        except OktaGroup.DoesNotExist:
            raise Http404("OktaGroup does not exist")
        
        group_members = okta_group.members()
        
        context = {
            'okta_group': okta_group,
            'group_members': group_members,
        }

        return render(request, 'groups/group_view.html', context)

@login_required
def user_view(request,user_id):
    """View User"""
    if request.method == "GET":
        try:
            okta_user = OktaUser.objects.get(pk=user_id)

        except OktaUser.DoesNotExist:
            raise Http404("OktaUser does not exist")
        
        group_membership = okta_user.groups()

        group_membership_types = group_membership.values('profile__type').order_by('profile__type').annotate(count=Count('profile__type'))

        try:
            user_item = User.objects.get(email=okta_user.email)
        except:
            user_item = None
        
        context = {
            'okta_user': okta_user,
            'group_membership': group_membership,
            'group_membership_types': group_membership_types,
            'user_item': user_item,
        }

        return render(request, 'users/user_view.html', context)

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
@permission_required('okta.task_sync_okta_users')
def TaskSyncOktaUsers(request):
    from okta.tasks import okta_user_sync

    t = okta_user_sync.delay()
    messages.success(request, 'Started Okta User Sync - TaskId: %s' % (t.id))

    next_url = request.GET.get("next",None)
    if next_url:
        return redirect(next_url)
    else:
        return redirect('okta:user-list')

@login_required
def group_list(request):
    """List Groups."""

    okta = OktaTools()

    group_list = OktaGroup.objects.filter(Q(hidden=False))

    app_list = OktaGroup.objects.filter(Q(hidden=False) & Q(profile__application__isnull=False)).values_list('profile__application', flat=True)

    app_name = request.GET.get('app', None)
    if app_name:
        group_list = group_list.filter(profile__application=app_name)

    # Just sort the list...
    app_list = sorted(list(set(app_list)), key=str.lower)
    
    context = {
        "group_list": group_list,
        "app_list": app_list,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'groups/group_list.html', context=context)

@login_required
def user_list(request):
    """List Users."""

    okta = OktaTools()

    user_list = OktaUser.objects.all()
    
    context = {
        "user_list": user_list,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'users/user_list.html', context=context)
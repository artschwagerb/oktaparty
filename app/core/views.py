from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    """View function for home page of site."""
    
    context = {

    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'core/index.html', context=context)

def reset_password(request):

    from django.contrib.auth import get_user_model
    from django.conf import settings
    import os

    ALLOW_ADMIN_RESET = int(os.environ.get("ALLOW_ADMIN_RESET", default=0))

    if settings.DEBUG and ALLOW_ADMIN_RESET:
        try:

            user = get_user_model().objects.get(email='admin@example.com')
            user.set_password('brianrocks')
            user.save()

        except:
            get_user_model().objects.create_superuser(email='admin@example.com',password='brianrocks')
            return HttpResponse("User could not be found")

        return HttpResponse("Password has been changed successfully")
    else:
        return HttpResponse("nope")
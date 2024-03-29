from mozilla_django_oidc.auth import OIDCAuthenticationBackend
#from myapp.models import Profile

class MyAuthenticationBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super(MyAuthenticationBackend, self).create_user(claims)
        print(claims)

        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.save()

        return user

    def update_user(self, user, claims):
        print(claims)
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.save()

        return user
from django.contrib.auth.models import User


class EmailAuthBackend:
    """
    1) Authenticate using an email address.
    2) The user credentials will be checked using ModelBackend, and if no user is returned, the credentials
       will be checked using EmailAuthBackend.
    """
    def authenticate(self, request, username=None, password=None):
        try:
            user: User = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

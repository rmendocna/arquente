from django.contrib.auth import get_user_model


class CustomUserModelBackend:

    def authenticate(self, request, username=None, password=None):
        from django.contrib.auth import get_user_model
        _user = get_user_model()
        try:
            user = _user.objects.get(email=username)
            if user.check_password(password):
                return user
        except _user.DoesNotExist:
            return None
        except _user.MultipleObjectsReturned:
            return None

    def get_user(self, user_id):
        _user = get_user_model()
        try:
            return _user.objects.get(pk=user_id)
        except _user.DoesNotExist:
            return None
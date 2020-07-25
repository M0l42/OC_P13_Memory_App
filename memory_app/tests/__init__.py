from django.contrib.auth.models import User


def create_testing_user(username='testuser', password='12345'):
    user = User.objects.create(username=username)
    user.set_password(password)
    user.save()
    return user
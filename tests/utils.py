from django.contrib.auth.models import AnonymousUser


def request_factory_login(factory, user=None):
    """Based on this gist: https://gist.github.com/964472"""
    request = factory.request()
    request.user = user or AnonymousUser()
    return request

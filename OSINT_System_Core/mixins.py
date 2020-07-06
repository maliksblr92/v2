"""
all mixins are defined here
"""
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.models import Group
from django.http import Http404


class RequireLoginMixin:
    """
    Login Required before accessing the view
    """

    def dispatch(self, request, *args, **kwargs):

        # print(request.user.groups.all())
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        return super(RequireLoginMixin, self).dispatch(
            request, *args, **kwargs)


class IsTSO:
    """
    User should belong to the TSO group to access this webpage
    """

    def dispatch(self, request, *args, **kwargs):
        # tso = Group.objects.get(name='tso')
        # print(request.user.groups)
        if not request.user.groups.filter(name='tso').exists():
            raise Http404(
                f'User not allowed to access {request.get_full_path()}')
        return super(IsTSO, self).dispatch(request, *args, **kwargs)


class IsTMO:
    """
    User should belong to the TMO group to access this webpage
    """

    def dispatch(self, request, *args, **kwargs):
        # tmo = Group.objects.get(name='tmo')
        # print(request.user.groups)
        if not request.user.groups.filter(name='tmo').exists():
            raise Http404(
                f'User not allowed to access {request.get_full_path()}')
        return super(IsTMO, self).dispatch(request, *args, **kwargs)


class IsRDO:
    """
    User should belong to the TMO group to access this webpage
    """

    def dispatch(self, request, *args, **kwargs):
        # rdo = Group.objects.get(name='rdo')
        # print(request.user.groups)
        if not request.user.groups.filter(name='rdo').exists():
            raise Http404(
                f'User not allowed to access {request.get_full_path()}')
        return super(IsRDO, self).dispatch(request, *args, **kwargs)


class IsPAO:
    """
    User should belong to the TMO group to access this webpage
    """

    def dispatch(self, request, *args, **kwargs):
        # pao = Group.objects.get(name='pao')
        # print(request.user.groups)
        if not request.user.groups.filter(name='pao').exists():
            raise Http404(
                f'User not allowed to access {request.get_full_path()}')
        return super(IsPAO, self).dispatch(request, *args, **kwargs)

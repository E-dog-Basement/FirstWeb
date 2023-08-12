from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect


class AuthMiddleWare(MiddlewareMixin):

    def process_request(self, request):

        # if request.path_info in ['/login/', '/image/code/', '/sign_up/', '/account/email/', '/ResetPassword/']:
        #     return

        if request.path_info not in []:
            return

        info_dict = request.session.get('info')

        if info_dict:
            return
        else:
            return redirect('/login/')

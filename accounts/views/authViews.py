from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth import logout

from accounts.forms.loginForm import LoginForm
from accounts.forms.userChangePasswordForm import UserChangePasswordForm


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            # Redirige a la página de inicio si el usuario ya está autenticado
            return redirect(reverse('dashboard:index'))

        next = request.GET.get('next', None)
        form = LoginForm()
        context = {
            'form': form,
            'next': next,
        }
        return render(request, 'login.html', context=context)

    def post(self, request):
        if request.user.is_authenticated:
            # Redirige a la página de inicio si el usuario ya está autenticado
            return redirect(reverse('dashboard:index'))

        next = request.GET.get('next', None)
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if next:
                return redirect(next)
            return redirect(reverse('dashboard:index'))
        context = {
            'form': form,
            'next': next,
        }
        return render(request, 'login.html', context=context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')


class UserChangePasswordView(View):
    def get(self, request):
        context = {
            'form': UserChangePasswordForm(user=request.user),
            'title': 'Cambio de Contraseña',
            'subtitle': 'Usuarios',
            'reverse_url': reverse('dashboard:index')
        }

        return render(request, 'core/layout/generic_form.html', context=context)

    def post(self, request):
        user = request.user

        form = UserChangePasswordForm(user=user, data=request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                '¡La contraseña se ha actualizado correctamente, por favor inicie sesión nuevamente!'
            )

            return redirect(reverse('dashboard:index'))

        context = {
            'form': form,
            'title': 'Cambio de Contraseña',
            'subtitle': 'Usuarios',
            'reverse_url': reverse('dashboard:index')
        }

        return render(request, 'core/layout/generic_form.html', context=context)


class PasswordResetCustomView(View):
    def get(self, request):
        context = {
            'form': PasswordResetForm()
        }

        return render(request, 'auth/password_reset_form.html', context=context)

    def post(self, request):
        form = PasswordResetForm(data=request.POST)

        # if form.is_valid():
        #     email = form.cleaned_data['email']

        #     user = User.objects.filter(email=email).first()

        #     if user:
        #         opts = {
        #             'token_generator': default_token_generator,
        #             'use_https': request.is_secure(),
        #             'html_email_template_name': 'auth/password_reset_email.html',
        #             'email_template_name': 'auth/password_reset_email.html',
        #             'subject_template_name': 'auth/email_subject.txt',
        #             'request': request
        #         }

        #         form.save(**opts)

        #         return redirect(reverse('accounts:password_reset_done'))

        #     else:
        #         messages.error(
        #             request, 'No existe un usuario registrado con la dirección de correo indicada.')

        context = {
            'form': form
        }

        return render(request, 'auth/password_reset_form.html', context=context)

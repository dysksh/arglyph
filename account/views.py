from django.shortcuts import redirect, resolve_url
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.views import generic
from django import forms

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)

class Signup(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'account/signup.html'
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            return redirect('argument-home')
        else:
            """仮登録と本登録用メールの発行."""
            # 仮登録と本登録の切り替えは、is_activeで行う
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # アクティベーションURLの送付
            current_site = get_current_site(self.request)
            domain = current_site.domain
            context = {
                'protocol': self.request.scheme,
                'domain': domain,
                'token': dumps(user.pk),
                'user': user,
            }

            subject = render_to_string('mail_templates/signup/subject.txt', context)
            message = render_to_string('mail_templates/signup/message.txt', context)
            from_email = settings.DEFAULT_FROM_EMAIL

            user.email_user(subject, message, from_email)
            return redirect('account:signup-done')


class SignupDone(generic.TemplateView):
    """仮登録"""
    template_name = 'account/signup_done.html'


class SignupComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'account/signup_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # 1日で期限切れ

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 本登録
                    user.is_active = True
                    user.save()
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()

class PasswordReset(PasswordResetView):
    subject_template_name = 'mail_templates/password_reset/subject.txt'
    email_template_name = 'mail_templates/password_reset/message.txt'
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password-reset-done')


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('account:password-reset-complete')
    template_name = 'account/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'

class OnlyCurrentUserMixin(UserPassesTestMixin):
    raise_exception = False

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser

class UserDetail(generic.DetailView):
    model = User
    template_name = 'account/user_detail.html'

class UserUpdate(OnlyCurrentUserMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'account/user_update.html'

    def get_success_url(self):
        return resolve_url('account:user-detail', pk=self.kwargs['pk'])
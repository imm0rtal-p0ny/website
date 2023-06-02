from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import DeleteView, DetailView, ListView
from .forms import LoginForm, EmailVerificationForm, RegistrationUserForm, UpdateUserForm,\
    ResetPasswordInEmailForm, ResetPasswordForm, SearchForm
from .models import ConfirmationCode, CustomUser, CustomUserManager
from .user_exception import NotUserException, NotUserCodeException, TimeOutCodeException, CodeDoNotMatchException,\
    EmailAlreadyRegistered


class HomeView(View):
    def get(self, request):
        return render(request, 'user/home.html')


def logout_view(request):
    logout(request)
    return redirect('home')


class AuthorizedView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'user/authorization.html', {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if not user.is_authorized:
                    return redirect('verification')
                return redirect('home')
            else:
                form.add_error('password', 'Invalid login or password')
        return render(request, 'user/authorization.html', {'form': form})


class VerificationEmailView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_authorized:
                return redirect('home')
            else:
                return render(request, 'user/verification.html', {'button_name': 'Send code'})
        else:
            return redirect('authorization')

    def post(self, request):
        if request.POST.get('code'):
            form = EmailVerificationForm(request.POST)
            if form.is_valid():
                user_email = form.cleaned_data.get('email')
                user_code = form.cleaned_data.get('code')
                try:
                    result = ConfirmationCode.check_valid_code(user_email, user_code)
                    if result:
                        CustomUser.verification(user_email)
                    return redirect('home')
                except (NotUserException, NotUserCodeException, TimeOutCodeException, CodeDoNotMatchException) as message:
                    form.add_error('email', message)
            return render(request, 'user/verification.html', {'button_name': 'Verification', 'form': form})
        else:
            form = EmailVerificationForm(initial={'email': request.user.email})
            try:
                new_code = ConfirmationCode.created_code(request.user.email)
                send_mail(
                    'Code verification',
                    new_code,
                    'imm0rtal-p0ny@ukr.net',
                    [request.user.email],
                    fail_silently=False,
                )
            except NotUserException as message:
                form.add_error('email', message)

            return render(request, 'user/verification.html', {'button_name': 'Verification', 'form': form})


class RegistrationUserView(View):
    def get(self, request):
        form = RegistrationUserForm()
        return render(request, 'user/registration.html', {'form': form})

    def post(self, request):
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            user_data.pop('repeat_password')
            new_user = CustomUserManager()
            new_user.create_user(**user_data)

            return redirect('authorization')

        else:
            return render(request, 'user/registration.html', {'form': form})


class UpdateUserView(View):
    def get(self, request):
        form = UpdateUserForm(instance=request.user)
        return render(request, 'user/update_user.html', {'form': form})

    def post(self, request):
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            request.user.update(**form.cleaned_data)
            return redirect('home')
        else:
            return render(request, 'user/update_user.html', {'form': form})


class MyChangePasswordView(PasswordChangeView):
    template_name = 'user/change_password.html'
    success_url = reverse_lazy('home')


class ResetPasswordView(View):
    def get(self, request):
        form = ResetPasswordInEmailForm()
        return render(request, 'user/reset_password.html', {'button_name': 'Send code', 'form': form})

    def post(self, request):
        if request.POST.get('code'):
            user_email = request.POST.get('email')
            print(1)
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                print(2)

                user_code = form.cleaned_data.get('code')
                new_password = form.cleaned_data.get('new_password')
                print(new_password)
                try:
                    result = ConfirmationCode.check_valid_code(user_email, user_code)
                    print(result)
                    if result:
                        user = CustomUser.get_by_email(user_email)

                        user.set_password(new_password)
                        user.save()
                    return redirect('authorization')
                except (NotUserException, NotUserCodeException, TimeOutCodeException, CodeDoNotMatchException) \
                        as message:
                    form.add_error('code', message)
            return render(request, 'user/reset_password.html', {'button_name': 'Restore password', 'form': form, 'email': user_email})

        else:
            form_email = ResetPasswordInEmailForm(request.POST)
            if form_email.is_valid():
                form = ResetPasswordForm()
                try:
                    new_code = ConfirmationCode.created_code(request.POST.get('email'))
                    send_mail(
                        'Code verification',
                        new_code,
                        'imm0rtal-p0ny@ukr.net',
                        [request.POST.get('email')],
                        fail_silently=False,
                    )
                except NotUserException as message:
                    form.add_error('code', message)

                return render(request, 'user/reset_password.html', {'button_name': 'Restore password',
                                                                      'form': form,
                                                                      'email': form_email.cleaned_data.get('email')})

            return render(request, 'user/reset_password.html', {'button_name': 'Restore password', 'form': form_email})


class ChangeEmailView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('home')
        form = ResetPasswordInEmailForm()
        return render(request, 'user/change_email.html', {'form': form})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('home')
        form = ResetPasswordInEmailForm(request.POST)
        if form.is_valid():
            user = CustomUser.get_by_email(request.user.email)
            try:
                result = user.update_email(form.cleaned_data.get('email'))
                if result:
                    return redirect('home')
            except EmailAlreadyRegistered as ex:
                form.add_error('email', ex)
        return render(request, 'user/change_email.html', {'form': form})


class DeleteUserView(DeleteView):
    model = CustomUser
    template_name = 'user/delete_user.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        if user != request.user:
            print(8)
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        if user != request.user:
            print(8)
            return redirect('home')
        return super().post(request, *args, **kwargs)


class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'user/user_detail.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('authorization')
        return super().get(request, *args, **kwargs)


class UserListView(ListView):
    model = CustomUser
    template_name = 'user/user_list.html'
    paginate_by = 10
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('authorization')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(email__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        print(self.request.GET.get('search'))
        context_data['search_form'] = SearchForm(initial=self.request.GET)
        return context_data



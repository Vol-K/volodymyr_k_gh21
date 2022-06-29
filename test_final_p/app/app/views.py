# Import all necessary moduls:
# 1) from Django package.
# from django.contrib import admin
from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.template.response import TemplateResponse

# 2) from Other packages.
import translators as ts

# 3) Local import.
from .forms import LogInForm, RegisterForm
from .app_support import validate_user_emal, add_user_to_all_tables


#
# class MyAdminSite(admin.AdminSite):
#     def get_app_list(self, request):
#         app_list = super().get_app_list(request)
#         app_list += [
#             {
#                 "name": "App",
#                 "app_label": "my_test_app",
#                 # "app_url": "/admin/test_view",
#                 "models": [
#                     {
#                         "name": "Dummy Model",
#                         "object_name": "Dummy Model",
#                         "admin_url": "/admin/test-custom-copy",
#                         "view_only": True,
#                     }
#                 ],
#             }
#         ]
#         return app_list


# Registering of new user on the website.
def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        # Checking of all data (in a form) from user are valid. When all is ok
        #  - add the new user to the DB and starting "Logon" process for his.
        if form.is_valid():
            form_data = form.cleaned_data

            # New User data
            new_user_login = form_data["username"]
            new_user_password_1 = form_data["password1"]
            new_user_email = form_data["user_email"]

            if validate_user_emal(new_user_email):
                user_data = {"user_login": new_user_login,
                             "user_pass": new_user_password_1,
                             "user_email": new_user_email}
                user = add_user_to_all_tables(user_data)
                login(request, user)
                popup_message = (
                    f"{form_data['username']} - ви успішно зареєструвалися.")
                messages.info(request, popup_message)
                return redirect("../index.html")

            else:
                messages.info(
                    request,
                    "Некоректно введено email.",
                    extra_tags='email'
                )
                return redirect("../register")

        # Check error by form validation procces and
        # show error message for user.
        else:
            form_errors = form.errors.as_data()
            if "username" in form_errors:
                messages.info(
                    request,
                    (ts.google(
                        str(form_errors["username"])[19:-4],
                        from_language='en',
                        to_language='uk'
                    )),
                    extra_tags='username'
                )
            if "password2" in form_errors:
                messages.info(
                    request,
                    (ts.google(
                        str(form_errors["password2"])[19:-4],
                        from_language='en',
                        to_language='uk'
                    )),
                    extra_tags='password'
                )
            new_user_email = form["user_email"].value()
            if not validate_user_emal(new_user_email):
                messages.info(
                    request,
                    "Некоректно введено email.",
                    extra_tags="email"
                )
            return redirect("../register")

    # Showing 'new user registration page' for the first time.
    else:
        form = RegisterForm()
        context = {"form": form}
        return render(request, "user_side/register.html", context)


#
def user_login(request):
    if request.method == "POST":
        form = LogInForm(request.POST)

        # Checking is form valid.
        if form.is_valid():
            form_data = form.cleaned_data

            user = authenticate(
                request,
                username=form_data["username"],
                password=form_data["password"],
            )

            # Checkinng is user has active status now.
            if user is not None:
                if user.is_active:
                    login(request, user)

                    # Create output message.
                    popup_message = (
                        f"Користувач '{form_data['username']}', "
                        "віттаємо з успішиним входом на сайт."
                    )
                    messages.success(request, popup_message)
                    return redirect("../index.html")

                else:
                    return HttpResponse(
                        "Ваш акаунт наразі неактивний, звернітся "
                        "до адміністратора."
                    )

            # Output message if inputed invalid values.
            elif not user:
                popup_message = (
                    "Введено неправильний логін або пароль, спробуйте знову."
                )
                messages.error(request, popup_message)
                return redirect("../login")

            # Message for case if something went wrong.
            else:
                return HttpResponse(
                    "Через технічні проблеми сервер не може обробити ваш "
                    "запит. Спробуйте знову за кілька хвилин."
                )

    # Redirect user to the 'Login' page for the first opened link.
    else:
        form = LogInForm()
        context = {"form": form}
        return render(request, "user_side/login.html", context)


# Exit user from the user account of the website & show message of that.
def log_out(request):
    logout(request)
    popup_message = ("Ви успішно вийшли з акаунта.")
    messages.info(request, popup_message)
    return redirect("../index.html")

from django.shortcuts import render, redirect
# from .admin import DummyModelAdmin


# Create your views here.
def my_custom_view(request):
    if request.method == "POST":
        print("EHUUUUUUU")
        return redirect("/admin")
    else:
        # ccc = DummyModelAdmin.get_app_list()
        context = {"app_list": "ccc"}
        # print
        # return HttpResponse('Admin Custom View')
        return render(request, "admin/test-custom-copy.html", context)

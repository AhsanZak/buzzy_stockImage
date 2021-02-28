from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core.files.base import ContentFile
from .models import *
import base64
# importing Image class from PIL package
from PIL import Image
from UserSide.models import UserDetail


# Create your views here.


def admin_panel(request):
    if request.session.has_key('password'):
        no_total = ImageDetail.objects.all().count()
        no_pending = ImageDetail.objects.filter(approval="pending").count()

        return render(request, 'AdminPanel/index.html', {'no_total': no_total, 'no_pending': no_pending})
    else:
        return redirect(login)


def login(request):
    if request.session.has_key('password'):
        return redirect(admin_panel)
    else:
        if request.method == 'POST':
            admin = request.POST.get('username')
            password = request.POST.get('password')

            if admin == 'admin' and password == '12345':
                request.session['password'] = password
                return redirect(admin_panel)
            else:
                messages.info(request, "Invalid Credentials")
                return render(request, 'AdminPanel/login.html')

        else:
            return render(request, 'AdminPanel/login.html')


def logout(request):
    request.session.flush()
    return redirect(admin_panel)


def manage_user(request):
    if request.session.has_key('password'):
        no_users = UserDetail.objects.all().count()
        no_blocked = UserDetail.objects.filter(is_active=False).count()
        details = UserDetail.objects.all().order_by('id')
        return render(request, 'AdminPanel/manage_user.html',
                      {'user': details, 'no_users': no_users, 'no_blocked': no_blocked})
    else:
        return redirect(admin_panel)


def create_user(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            mobile_number = request.POST['mobile_no']
            email = request.POST['email']
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 == password2:
                if UserDetail.objects.filter(username=username).exists():
                    messages.info(request, "Username Taken")
                    return render(request, 'AdminPanel/register_user.html')
                elif UserDetail.objects.filter(email=email).exists():
                    messages.info(request, "Email Taken")
                    return render(request, 'AdminPanel/register_user.html')
                elif UserDetail.objects.filter(last_name=last_name).exists():
                    messages.info(request, "Mobile Number Taken")
                    return render(request, 'AdminPanel/register_user.html')
                else:
                    user = UserDetail.objects.create_user(username=username, password=password1, email=email,
                                                    first_name=first_name, last_name=last_name, mobile_number=mobile_number)
                    return redirect(admin_panel)
            else:
                messages.info(request, "Passwords not Matching")
        else:
            return render(request, 'AdminPanel/register_user.html')
    else:
        return redirect(admin_panel)


def block_user(request, user_id):
    if request.session.has_key('password'):
        user = UserDetail.objects.get(id=user_id)
        if user.is_active == True:
            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()
        return redirect(manage_user)
    else:
        return redirect(admin_panel)


def block_creator(request, user_id):
    if request.session.has_key('password'):
        user = UserDetail.objects.get(id=user_id)
        if user.is_active == True:
            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()
        return redirect(manage_creator)
    else:
        return redirect(admin_panel)


def update_user(request, id):
    if request.session.has_key('password'):
        user = UserDetail.objects.get(id=id)
        return render(request, 'AdminPanel/update_user.html', {'details': user})
    else:
        return redirect(admin_panel)


def edit_user(request, id):
    if request.session.has_key('password'):
        if request.method == 'POST':
            user = UserDetail.objects.get(id=id)
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.username = request.POST['username']
            user.save()
            return redirect(manage_user)
        else:
            return redirect(update_user)
    else:
        return redirect(admin_panel)


def delete_user(request, id):
    if request.session.has_key('password'):
        user = UserDetail.objects.get(id=id)
        user.delete()
        return redirect(manage_user)
    else:
        return redirect(admin_panel)


def add_creator(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            mobile_number = request.POST['mobile_no']
            email = request.POST['email']
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 == password2:
                if UserDetail.objects.filter(username=username).exists():
                    messages.info(request, "Username Taken")
                    return render(request, 'AdminPanel/register_user.html')
                elif UserDetail.objects.filter(email=email).exists():
                    messages.info(request, "Email Taken")
                    return render(request, 'AdminPanel/register_user.html')
                elif UserDetail.objects.filter(last_name=last_name).exists():
                    messages.info(request, "Mobile Number Taken")
                    return render(request, 'AdminPanel/register_user.html')
                else:
                    user = UserDetail.objects.create_user(username=username, password=password1, email=email,
                                                    first_name=first_name, last_name=last_name, is_staff=True, mobile_number=mobile_number)
                    return redirect(admin_panel)
            else:
                messages.info(request, "Passwords not Matching")
        else:
            return render(request, 'AdminPanel/register_creator.html')


def manage_creator(request):
    if request.session.has_key('password'):
        user = UserDetail.objects.filter(is_staff=True)
        no_blocked = UserDetail.objects.filter(is_staff=True, is_active=False).count()
        no_creators = UserDetail.objects.filter(is_staff=True).count()
        return render(request, 'AdminPanel/manage_creator.html', {'user': user, 'no_blocked': no_blocked, 'no_creators': no_creators})
    else:
        return redirect(admin_panel)


def category(request):
    if request.session.has_key('password'):
        categories = Category.objects.all()

        return render(request, 'AdminPanel/manage_category.html', {'categories': categories})
    else:
        return redirect(login)


def add_category(request):
    if request.session.has_key('password'):
        name = request.POST['name']
        Category.objects.create(name=name)
        return redirect(category)
    else:
        return redirect(login)


def delete_category(request, id):
    if request.session.has_key('password'):
        category = Category.objects.get(id=id)
        category.delete()
        return redirect(category)
    else:
        return redirect(login)


def contents(request):
    if request.session.has_key('password'):
        contents = ImageDetail.objects.all()
        no_contents = ImageDetail.objects.all().count()
        no_pending = ImageDetail.objects.filter(approval="pending").count()

        return render(request, 'AdminPanel/contents.html',
                      {'contents': contents, 'no_pending': no_pending,
                       'no_contents': no_contents})
    else:
        return redirect(admin_panel)


def add_contents(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            name = request.POST['wallpaper_name']
            price = request.POST['price']
            category = Category.objects.get(name=request.POST['category'])
            i = request.FILES.get("image")

            ImageDetail.objects.create(name=name, category=category, description="This is Image description",
                                       price=price, image=i, approval="approved")
            return redirect(contents)
        else:
            categories = Category.objects.all()
            return render(request, 'AdminPanel/AddContent.html', {'categories': categories})
    else:
        return redirect(admin_panel)


def approve_contents(request):
    if request.session.has_key('password'):
        contents = ImageDetail.objects.filter(approval="pending")
        no_contents = ImageDetail.objects.all().count()
        no_pending = ImageDetail.objects.filter(approval="pending").count()

        return render(request, 'AdminPanel/approve_contents.html',
                      {'contents': contents, 'no_pending': no_pending,
                       'no_contents': no_contents})
    else:
        return redirect(login)


def disapprove_contents(request):
    if request.session.has_key('password'):
        contents = ImageDetail.objects.filter(approval="approved")
        no_contents = ImageDetail.objects.all().count()
        no_pending = ImageDetail.objects.filter(approval="pending").count()
        return render(request, 'AdminPanel/disapprove_contents.html',
                      {'contents': contents, 'no_pending': no_pending,
                       'no_contents': no_contents})
    else:
        return redirect(login)


def approved_contents(request, id):
    if request.session.has_key('password'):
        content = ImageDetail.objects.get(id=id)
        content.approval = "approved"
        content.save()
        return redirect(approve_contents)
    else:
        return redirect(login)


def disapproved_contents(request, id):
    if request.session.has_key('password'):
        content = ImageDetail.objects.get(id=id)
        content.approval = "pending"
        content.save()
        return redirect(disapprove_contents)
    else:
        return redirect(login)


def admin_delete_content(request, id):
    if request.session.has_key('password'):
        content = ImageDetail.objects.get(id=id)
        content.delete()
        return redirect(contents)
    else:
        return redirect(admin_panel)

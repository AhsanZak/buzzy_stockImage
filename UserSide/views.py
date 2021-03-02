from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
from AdminPanel.models import *
from django.http import JsonResponse
import uuid
import json
import mimetypes
from wsgiref.util import FileWrapper
from django.core.files.base import ContentFile
import base64
from PIL import Image
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse


def send_file(response):
    img = open('C:/Users/ahsan/Downloads/pexels-harrison-candlin-2441454.jpg', 'rb')
    response = FileResponse(img)
    print("sdfsf")
    return response

def home(request):
    contents = ImageDetail.objects.filter(approval="approved", user__is_staff=True)
    paginator = Paginator(contents, 10)
    print(paginator)
    page = request.GET.get('page')
    try:
        contents = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        contents = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range
            # return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        contents = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return render(request,
                    'UserSide/home.html',
                    {'section': 'contents', 'contents': contents})
    return render(request,
                    'UserSide/home.html',
                        {'section': 'images', 'contents': contents})
                

def load_more(request):
    offset = int(request.GET['offset'])
    filter = request.GET['filter']
    limit = 2
    if filter == 'all':
        posts = ImageDetail.objects.all()
        totalData = len(posts)
        posts = posts[offset:limit+offset]
    elif filter == 'free':
        posts = ImageDetail.objects.filter(price=False)
        totalData = len(posts)
        posts = posts[offset:limit+offset]
    elif filter == 'paid':
        posts = ImageDetail.objects.filter(price=True)
        totalData = len(posts)
        posts = posts[offset:limit+offset]
    elif filter == 'top':
        posts = ImageDetail.objects.filter(rate__range=(3,5))
        totalData = len(posts)
        posts = posts[offset:limit+offset]

    data={}
    posts_json = serializers.serialize('json', posts)

    print("Serialized post", posts_json)
    
    return JsonResponse(data={
        'posts':posts_json,
        'totalResult':totalData
    })


def about(request):
    return render(request, 'UserSide/about1.html')


def contact(request):
    return render(request, 'UserSide/contact.html')


def login(request):
    if request.user.is_authenticated:
        return redirect(home)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(home)
        else:
            messages.info(request, "Invalid credentials")
            return redirect(login)
    else:
        return render(request, 'UserSide/login.html')


def register(request):
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
                return render(request, 'UserSide/signup.html')
            elif UserDetail.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return render(request, 'UserSide/signup.html')
            elif UserDetail.objects.filter(last_name=last_name).exists():
                messages.info(request, "Mobile Number Taken")
                return render(request, 'UserSide/signup.html')
            else:
                user = UserDetail.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name, mobile_number=mobile_number, )
                return redirect('login')
        else:
            messages.info(request, "Passwords Not Matching")
            return render(request, 'UserSide/signup.html')

    else:
        return render(request, 'UserSide/signup.html')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect(home)
    else:
        return redirect(home)


def view_single(request, image_id):
    content = ImageDetail.objects.filter(id=image_id).first()
    contents = ImageDetail.objects.filter(approval="approved", user__is_staff=True)
    return render(request, 'UserSide/view_single.html', {'content': content, 'contents': contents })


def view_creator(request, user):
    user = UserDetail.objects.get(username=user)
    contents = ImageDetail.objects.filter(user=user)

    return render(request, 'UserSide/view_creator.html', {'user': user, 'contents': contents})



def rate(request, image_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            value = int(request.POST['rate'])

            image_detail = ImageDetail.objects.get(id=image_id)
            image_detail.rate = (image_detail.rate + value) / 2

            image_detail.save()
            return redirect(view_single, image_id)
        else:
            return redirect(view_single, image_id)
    else:
        return redirect(login)


def activate_creator(request):
    if request.user.is_authenticated:
        user = UserDetail.objects.get(username=request.user)
        if user.is_staff == False:
            user.is_staff = True
            user.save()
        return redirect(profile_settings)
    else:
        return redirect(login)


def Deactivate_creator(request, user_id):
    if request.user.is_authenticated:
        user = UserDetail.objects.get(id=user_id)
        if user.is_staff == True:
            user.is_staff = False
            user.save()
        return redirect(home)
    else:
        return redirect(login)


def creator(request):
    if request.user.is_authenticated:
        no_pending = ImageDetail.objects.filter(user=request.user, approval="pending").count()
        return render(request, 'UserSide/creator.html', {'no_pending': no_pending})
    else:
        return redirect(login)


def creator_contents(request):
    if request.user.is_authenticated:
        contents = ImageDetail.objects.filter(user=request.user)
        return render(request, 'UserSide/creator_contents.html', {'contents': contents})
    else:
        return redirect(login)


def delete_content(request, id):
    if request.user.is_authenticated:
        content = ImageDetail.objects.filter(id=id)
        content.delete()
        return redirect(creator_contents)
    else:
        return redirect(login)


def creator_upload(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST['wallpaper_name']
            category = request.POST['category']
            image = request.FILES['image']
            description = request.POST['description']
            price = request.POST['price'] 

            if price == 'free':
                price = False
            else: 
                price = True

            try:
                Category.objects.get(name=category)
            except ObjectDoesNotExist:
                Category.objects.create(name=category)
            
            print(price)
            ImageDetail.objects.create(name=name, category=Category.objects.get(name=category), price=price, image=image, user=request.user,
                                    approval="pending", description=description)
            return redirect(creator_upload)
        else:
            categories = Category.objects.all()
            return render(request, 'UserSide/creator_upload.html', {'categories': categories})
    else:
        return redirect(login)


def creator_settings(request):
    pass


def profile_settings(request):
    if request.user.is_authenticated:
        username = request.user
        profile = UserDetail.objects.filter(username=username)
        return render(request, 'UserSide/UserProfile.html', {'profile': profile})
    else:
        return redirect(login)


def edit_userProfile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            username = request.user
            user_image = request.FILES.get('imageInput')

            if user_image is not None:
                user_profile = UserDetail.objects.filter(username=username)
                if not user_profile:
                    UserDetail.objects.create(user_image=user_image, user=user)
                else:
                    user_profile = UserDetail.objects.get(username=username)
                    user_profile.user_image = user_image
                    user_profile.save()

            return redirect(profile_settings)

        else:
            return redirect(profile_settings)
    else:
        return redirect(login)


def download_image(request):
    if request.user.is_authenticated:
        image = ImageDetail.objects.get(id=request.POST['id'])
        if Downloads.objects.filter(image=image):
            result = "ALreadry Downloaded"
            print("already downloaded")
        else:
            Downloads.objects.create(image=image, transaction_id=uuid.uuid4(), status='success', payment_mode='free',
                             user=request.user)
            result = "success"
            print("success")
        return JsonResponse({'result': result}, safe=False)
    else:
        return redirect(login)


def payment_page(request):
    if request.user.is_authenticated:
        return render(request, 'UserSide/payment.html')
    else:
        redirect(login)


def downloads(request):
    if request.user.is_authenticated:
        contents = ImageDetail.objects.all()
        return render(request, 'UserSide/image_library.html', {'contents': contents})
    else:
        return redirect(login)

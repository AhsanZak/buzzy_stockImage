from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core.files.base import ContentFile
from .models import *
import base64
# importing Image class from PIL package
from PIL import Image
from UserSide.models import UserDetail
from django.contrib.auth.models import User, auth
import cv2
from django.http import JsonResponse
from UserSide.models import *

# Create your views here.


def admin_panel(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        no_total = ImageDetail.objects.all().count()
        no_pending = ImageDetail.objects.filter(approval="pending").count()
        try:
            credits_available = Wallet.objects.get(user=request.user)
        except:
            credits_available = Wallet.objects.create(user=request.user)
        order = Order.objects.all()
        no_orders = Order.objects.all().count()
        no_downloads = Downloads.objects.all().count()
        downloads = Downloads.objects.all()  

        order_amounts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for download in downloads:
            print(download.date_downloaded.month)
            order_amounts[download.date_downloaded.month - 1] += 1
        
        print("Order amount in march", order_amounts[2])
        print(order_amounts)

        print("Total Orders : ", no_orders)
        print("Total Downloads : ", no_downloads)   

        context = { 
                    'no_total': no_total, 
                    'no_pending': no_pending,
                    'no_downloads': no_downloads,
                    'no_orders': no_orders,
                    'credits_available': credits_available,
                    'order_amounts': order_amounts
                }

        return render(request, 'AdminPanel/index.html', context)
    else:
        return redirect(login)


def login(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        return redirect(admin_panel)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(admin_panel)
        else:
            messages.info(request, "Invalid credentials")
            return render(request, 'AdminPanel/login.html')
    else:
        return render(request, 'AdminPanel/login.html')


def logout(request):
    auth.logout(request)
    return redirect(admin_panel)


def manage_watermark(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        
        watermarks = WaterMark.objects.all()
        return render(request, 'AdminPanel/manage_watermark.html', {'watermarks':watermarks})

    else:
        return redirect(admin_panel)


def add_watermark(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method == 'POST':
            WaterMark.objects.all().delete()
            name = request.POST['name']
            image = request.FILES['image']

            WaterMark.objects.create(image=image, name=name)

            return JsonResponse('success', safe=False)
    else:
        return redirect(login)


def manage_user(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        no_users = UserDetail.objects.filter(is_superuser=False).count()
        no_blocked = UserDetail.objects.filter(is_active=False).count()
        details = UserDetail.objects.filter(is_superuser=False).order_by('id')

        context = {
                'user': details, 
                'no_users': no_users, 
                'no_blocked': no_blocked
        }
        return render(request, 'AdminPanel/manage_user.html', context)
    else:
        return redirect(admin_panel)


def create_user(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
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
                    wallet = Wallet.objects.create(user=user)
                    return redirect(manage_user)
            else:
                messages.info(request, "Passwords not Matching")
        else:
            return render(request, 'AdminPanel/register_user.html')
    else:
        return redirect(admin_panel)


def block_user(request, user_id):
    if request.user.is_authenticated and request.user.is_superuser == True:
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
    if request.user.is_authenticated and request.user.is_superuser == True:
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
    if request.user.is_authenticated and request.user.is_superuser == True:
        user = UserDetail.objects.get(id=id)
        return render(request, 'AdminPanel/update_user.html', {'details': user})
    else:
        return redirect(admin_panel)


def edit_user(request, id):
    if request.user.is_authenticated and request.user.is_superuser == True:
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
    if request.user.is_authenticated and request.user.is_superuser == True:
        user = UserDetail.objects.get(id=id)
        user.delete()
        return redirect(manage_user)
    else:
        return redirect(admin_panel)


def add_creator(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
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
                    wallet = Wallet.objects.create(user=user)

                    return redirect(manage_creator)
            else:
                messages.info(request, "Passwords not Matching")
        else:
            return render(request, 'AdminPanel/register_creator.html')


def manage_creator(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        user = UserDetail.objects.filter(is_staff=True, is_superuser=False)
        no_blocked = UserDetail.objects.filter(is_staff=True, is_active=False).count()
        no_creators = UserDetail.objects.filter(is_staff=True, is_superuser=False).count()
        
        top_creators = 0
        top_images = ImageDetail.objects.filter(rate=4).distinct('user')
        print("lalalal")
        for images in top_images:
            print("Top Images : ", images)
            print(images.user)
            top_creators += 1

        context = {'user': user, 
                    'no_blocked': no_blocked, 
                    'no_creators': no_creators,
                    'top_creators': top_creators
                }

        return render(request, 'AdminPanel/manage_creator.html', context)
    else:
        return redirect(admin_panel)


def delete_category(request, id):
    if request.user.is_authenticated and request.user.is_superuser == True:
        category = Category.objects.get(id=id)
        category.delete()
        return redirect(category)
    else:
        return redirect(login)


def contents(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        contents = ImageDetail.objects.all()
        no_paid_contents = ImageDetail.objects.filter(price=True).count()
        no_contents = ImageDetail.objects.all().count()
        no_creators = UserDetail.objects.filter(is_active=True).count()
        no_pending = ImageDetail.objects.filter(approval="pending").count()

        return render(request, 'AdminPanel/contents.html',
                      {'contents': contents, 'no_pending': no_pending,
                       'no_contents': no_contents, 'no_paid_contents': no_paid_contents, 'no_creators': no_creators})
    else:
        return redirect(admin_panel)


def add_contents(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method == 'POST':
            name = request.POST['name']
            tags = request.POST['tags'].upper()
            image = request.FILES['image']
            description = request.POST['description']
            price = request.POST['price']
            print(price)


            
            # printing original string
            print("The original string is : " + tags)
            
            # initializing punctuations string 
            punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
            
            # Removing punctuations in string
            # Using loop + punctuation string
            for ele in tags: 
                if ele in punc: 
                    tags = tags.replace(ele, "") 
            
            # printing result 
            print("The string after punctuation filter : " + tags) 

            tag_list = tags.split()
            print(tag_list)

            tag_list = tags.split()
            print(tag_list)


            if price == 'free':
                print("price is false")
                price = False
            else:
                print("price is true")
                price = True

            if price == True :
                print("Price is True")
                image_detail = ImageDetail.objects.create(name=name, price=price,
                                           image=image, user=request.user,
                                           approval="approved", description=description)
                
                for tags in tag_list:
                    Tags.objects.create(tag=tags, image=image_detail)


                img = cv2.imread('static/'+image_detail.ImageURL)
                h_img, w_img, _ = img.shape

                watermark = WaterMark.objects.all().first()
                logo = cv2.imread('static/'+watermark.ImageURL)

                h_logo, w_logo, _ = logo.shape
                # Get the center of the original. It's the location where we will place the watermark
                center_y = int(h_img / 2)
                center_x = int(w_img / 2)

                top_y = center_y - int(h_logo / 2)
                left_x = center_x - int(w_logo / 2)
                bottom_y = top_y + h_logo
                right_x = left_x + w_logo

                roi = img[top_y: bottom_y, left_x: right_x]
                result = cv2.addWeighted(roi, 1, logo, 0.3, 0)
                img[top_y: bottom_y, left_x: right_x] = result

                cv2.imwrite("static/image/watermarks/"+image_detail.image.name, img)
                result = "created"
                print(result)
                return JsonResponse({'data': result}, safe=False)
            else:
                print("price is false")
                image_detail = ImageDetail.objects.create(name=name, price=price,
                                           image=image, user=request.user,
                                           approval="approved", description=description)
                                           
                for tags in tag_list:
                    Tags.objects.create(tag=tags, image=image_detail)

                result = "created"
                print(result)
                return JsonResponse({'data': result}, safe=False)

        else:
            return render(request, 'AdminPanel/AddContent.html')
    else:
        return redirect(login)


def approve_contents(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        contents = ImageDetail.objects.filter(approval="pending")
        no_contents = ImageDetail.objects.all().count()
        no_pending = ImageDetail.objects.filter(approval="pending").count()
        no_creators = UserDetail.objects.filter(is_staff=True).count()
        no_paid_contents = ImageDetail.objects.filter(price=True).count()

        context = {
                    'contents': contents, 
                    'no_pending': no_pending,
                    'no_contents': no_contents, 
                    'no_creators': no_creators, 
                    'no_paid_contents': no_paid_contents
        }


        return render(request, 'AdminPanel/approve_contents.html', context)
    else:
        return redirect(login)


def disapprove_contents(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        contents = ImageDetail.objects.filter(approval="approved")
        no_contents = ImageDetail.objects.all().count()
        no_pending = ImageDetail.objects.filter(approval="pending").count()
        no_approved = ImageDetail.objects.filter(approval="approved").count()

        context = {'contents': contents, 
                    'no_pending': no_pending,
                    'no_contents': no_contents,
                    'no_approved': no_approved
                }
        return render(request, 'AdminPanel/disapprove_contents.html', context)
    else:
        return redirect(login)


def approved_contents(request, id):
    if request.user.is_authenticated and request.user.is_superuser == True:
        content = ImageDetail.objects.get(id=id)
        content.approval = "approved"
        content.save()
        return redirect(approve_contents)
    else:
        return redirect(login)


def disapproved_contents(request, id):
    if request.user.is_authenticated and request.user.is_superuser == True:
        content = ImageDetail.objects.get(id=id)
        content.approval = "pending"
        content.save()
        return redirect(disapprove_contents)
    else:
        return redirect(login)


def admin_delete_content(request, id):
    if request.user.is_authenticated and request.user.is_superuser == True:
        content = ImageDetail.objects.get(id=id)
        content.delete()
        return redirect(contents)
    else:
        return redirect(admin_panel)


def orders(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        orders = Order.objects.all()
        return render(request, 'AdminPanel/orders.html', {'orders':orders})
    else:
        return redirect(login)

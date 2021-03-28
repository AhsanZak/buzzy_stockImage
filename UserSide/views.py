from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
from AdminPanel.models import *
from django.http import JsonResponse
import uuid
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse
import cv2
import datetime
from django.db.models import Q
from django.contrib.auth.hashers import check_password



def home(request):
    contents = ImageDetail.objects.filter(approval="approved", user__is_staff=True).order_by('-id')
    paginator = Paginator(contents, 20)
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

    tags = Tags.objects.all().distinct('tag')

    if request.is_ajax():
        return render(request,
                      'UserSide/home.html',
                      {'section': 'contents', 'contents': contents, 'tags':tags})
    return render(request,
                  'UserSide/home.html',
                  {'section': 'images', 'contents': contents, 'tags':tags})


def load_more(request):
    offset = int(request.GET['offset'])
    filter = request.GET['filter']
    limit = 20
    if filter == 'all':
        posts = ImageDetail.objects.filter(approval="approved", user__is_staff=True)
        totalData = len(posts)
        posts = posts[offset:limit + offset]
    elif filter == 'free':
        posts = ImageDetail.objects.filter(price=False, approval="approved", user__is_staff=True)
        totalData = len(posts)
        posts = posts[offset:limit + offset]
    elif filter == 'paid':
        posts = ImageDetail.objects.filter(price=True, approval="approved", user__is_staff=True)
        totalData = len(posts)
        posts = posts[offset:limit + offset]
    elif filter == 'top':
        posts = ImageDetail.objects.filter(rate__range=(3, 5), approval="approved", user__is_staff=True)
        totalData = len(posts)
        posts = posts[offset:limit + offset]

    data = {}
    posts_json = serializers.serialize('json', posts)

    print("Serialized post", posts_json)

    return JsonResponse(data={
        'posts': posts_json,
        'totalResult': totalData
    })


def about(request):
    return render(request, 'UserSide/about1.html')


def contact(request):
    return render(request, 'UserSide/contact.html')


def login(request, backend='django.contrib.auth.backends.ModelBackend'):
    if request.user.is_authenticated:
        print("USer Is Authenticated")
        return redirect(home)
    if request.method == 'POST':
        print("Request Mehthod is post")
        username = request.POST['username']
        password = request.POST['password']

        
        user = UserDetail.objects.filter(username=username).first()

        if user is not None and check_password(password, user.password):
            if user.is_active == False:
                messages.info(request, 'User is Blocked')
                return render(request, 'UserSide/login.html')
            else:
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect(home)
        else:
            value = {"username": username}
            messages.info(request, "Invalid Credentials")
            return render(request, 'UserSide/login.html')


        # user = auth.authenticate(username=username, password=password)
        # if user is not None:
        #     print("User is not none")
        #     if user.is_active == 'false':
        #         print("user is not avtive ")
        #         return render(request, 'UserSide/login.html')
        #     else:
        #         auth.login(request, user)
        #         return redirect(home)
        # else:
        #     messages.info(request, "Invalid Credentials")
        #     return render(request, 'UserSide/login.html')
    else:
        print("User is not authentcautered")
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
            elif UserDetail.objects.filter(mobile_number=mobile_number).exists():
                messages.info(request, "Mobile Number Taken")
                return render(request, 'UserSide/signup.html')
            else:
                user = UserDetail.objects.create_user(username=username, password=password1, email=email,
                                                      first_name=first_name, last_name=last_name, mobile_number=mobile_number)
                wallet = Wallet.objects.create(user=user)
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


def search(request):
    if request.method == 'GET':
        search_name = request.GET['search']
        print(type(search_name))
        contents = ImageDetail.objects.filter(Q(tag_image__tag__icontains=search_name) | Q(name__icontains=search_name)).distinct('image')
        print(contents)
        context = {
            'contents': contents,
            'search_content': search_name
        }
        return render(request, 'UserSide/searchContent.html', context)


def tag_filter(request, tag_name):
    print(tag_name)
    contents = Tags.objects.filter(tag=tag_name).distinct('image')
    context = {
        'contents': contents,
        'tag_name': tag_name
    }
    return render(request, 'UserSide/tagContent.html', context)


def view_single(request, image_id):
    content = ImageDetail.objects.get(id=image_id)
    contents = ImageDetail.objects.filter(approval="approved", user__is_staff=True, user=content.user)
    comments = Comments.objects.filter(image=image_id).order_by('-id')
    # credits = Wallet.objects.get(user=request.user)
    tags = Tags.objects.filter(image_id=content)

    #similar_images
    tag_list = []
    for tag in tags:
        tag_list.append(tag.tag)
    similar_images = Tags.objects.filter(~Q(image_id=image_id), tag__in=tag_list).distinct('image')

    if request.user.is_authenticated:
        try:
            Favourites.objects.get(user=request.user, image=content)
            favourite = 1
        except ObjectDoesNotExist or Object:
            favourite = 0
    
        if Downloads.objects.filter(user=request.user, image_id=image_id).exists():
            downloads = Downloads.objects.get(user=request.user, image_id=image_id)
            if downloads.image_id == image_id:
                option_available = 1
                print(option_available)
            else:
                option_available = 0
                print("not paid")
                print(option_available)
        else:
            option_available = 0
        print(option_available)
    else:
        favourite = 0
        option_available = 0
        print("user not regstered")
        print(option_available)

    print(option_available)

    context = {
        'content' : content,
        'contents' : contents,
        'comments' : comments,
        'similar' : similar_images,
        # 'credits' : credits,
        'tags': tags,
        'option_available' : option_available, 
        'favourite' : favourite
    }
    return render(request, 'UserSide/view_single.html', context)


def view_creator(request, user):
    creator = UserDetail.objects.get(username=user)
    contents = ImageDetail.objects.filter(user=creator)
    no_of_contents = ImageDetail.objects.filter(user=creator).count()
    creator_bio = Creator.objects.get(user=creator)
    context = {
        'user': creator, 
        'contents': contents, 
        'creator_bio': creator_bio,
        'no_of_contents': no_of_contents
    }
    return render(request, 'UserSide/view_creator.html', context)


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
            Creator.objects.create(user=request.user)
        return redirect(profile_settings)
    else:
        return redirect(login)


def Deactivate_creator(request, user_id):
    if request.user.is_authenticated:
        user = UserDetail.objects.get(id=user_id)
        if user.is_staff == True:
            user.is_staff = False
            creator = Creator.objects.get(user=request.user)
            creator.delete()
            user.save()
        return redirect(profile_settings)
    else:
        return redirect(login)


def creator(request):
    if request.user.is_authenticated and request.user.is_staff == True:
        no_pending = ImageDetail.objects.filter(user=request.user, approval="pending").count()
        wallet_orders = WalletTransactions.objects.filter(to_user=request.user, transaction_name=WalletTransactions.SADHA)
        creator_images = ImageDetail.objects.filter(user=request.user)
        no_downloads = Downloads.objects.filter(image__in=creator_images).count()

        #Total Earning
        total_earnings = 0
        for order in wallet_orders:
            total_earnings += order.amount

        #Earnings per month
        order_amounts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for order in wallet_orders:
            order_amounts[order.date.month - 1] += order.amount

        context = {
                    'no_pending': no_pending,
                    'order_amounts': order_amounts,
                    'no_downloads': no_downloads,
                    'total_earnings': total_earnings
                }

        return render(request, 'UserSide/creator.html', context)
    else:
        return redirect(login)


def creator_contents(request):
    if request.user.is_authenticated and request.user.is_staff == True:
        contents = ImageDetail.objects.filter(user=request.user)
        return render(request, 'UserSide/creator_contents.html', {'contents': contents})
    else:
        return redirect(login)


def delete_content(request, id):
    if request.user.is_authenticated and request.user.is_staff == True:
        content = ImageDetail.objects.get(id=id)
        content.delete()
        return redirect(creator_contents)
    else:
        return redirect(login)


def creator_upload(request):
    if request.user.is_authenticated and request.user.is_staff == True:
        if request.method == 'POST':
            name = request.POST['wallpaper_name']
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
                                           approval="pending", description=description)
                
                for tags in tag_list:
                    Tags.objects.create(tag=tags, image=image_detail)


                img = cv2.imread('static/'+image_detail.ImageURL)
                h_img, w_img, _ = img.shape

                print("Height and Width of the Image are : ", h_img, w_img)

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
                                           approval="pending", description=description)
                                           
                for tags in tag_list:
                    Tags.objects.create(tag=tags, image=image_detail)

                result = "created"
                print(result)
                return JsonResponse({'data': result}, safe=False)

        else:
            return render(request, 'UserSide/creator_upload.html')
    else:
        return redirect(login)


def otp_login(request):
    if request.user.is_authenticated:
        return redirect(home)
    otp = 1
    if request.method == 'POST':
        number = request.POST['mobile']
        request.session['number'] = number
        if UserDetail.objects.filter(mobile_no=number).exists():
            otp = 0
            url = "https://d7networks.com/api/verifier/send"
            number = str(91) + number
            payload = {
                'mobile': number,
                'sender_id': 'SMSINFO',
                'message': 'Your otp code is {code}',
                'expiry': '900'}
            files = [
            ]
            headers = {
                'Authorization': 'Token b76a52adeb253e2dbb98dd2378d542f8d53fbe6b'
            }
            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            data = response.text.encode('utf8')
            datadict = json.loads(data)
            id = datadict['otp_id']
            request.session['id'] = id

            return render(request, 'User/otplogin.html', {'otp': otp})
        else:
            messages.info(request, "Please enter registered Number")
            return render(request, 'User/otplogin.html', {'otp': otp})
    else:
        return render(request, 'User/otplogin.html', {'otp': otp})


def verify_otp(request):
    if request.user.is_authenticated:
        return redirect(home)
    else:
        if request.method == 'POST':
            otp = request.POST['otp']
            id_otp = request.session['id']
            url = "https://d7networks.com/api/verifier/verify"
            payload = {'otp_id': id_otp,
                       'otp_code': otp}
            files = [

            ]
            headers = {
                'Authorization': 'Token b76a52adeb253e2dbb98dd2378d542f8d53fbe6b'
            }

            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            data = response.text.encode('utf8')
            datadict = json.loads(data)
            status = datadict['status']

            if status == 'success':
                number = request.session['number']
                user_detail = UserDetail.objects.filter(mobile_no=number).first()
                user = user_detail.user
                print(user)
                if user_detail is not None:
                    if user_detail.user.is_active == False:
                        messages.info(request, 'User is blocked')
                        return redirect(login)

                    else:
                        auth.login(request, user)
                        return redirect(home)
                else:
                    return redirect(login)

            else:
                messages.error(request, 'User not Exist')
                return redirect(login)

        else:
            return HttpResponse("Oops")


def creator_settings(request):
    pass


def profile_settings(request):
    if request.user.is_authenticated:
        username = request.user
        profile = UserDetail.objects.filter(username=username)

        try:
            credits_available = Wallet.objects.get(user=request.user)
        except:
            credits_available = Wallet.objects.create(user=request.user)

        try:
            creator_bio = Creator.objects.get(user=request.user)
        except ObjectDoesNotExist:
            creator_bio = 0

        context = {
            'profile' : profile,
            'credits_available' : credits_available, 
            'creator_bio' : creator_bio 
        }
        return render(request, 'UserSide/UserProfile.html', context)
    else:
        return redirect(login)


def edit_userProfile(request):
    if request.user.is_authenticated:
        print(request.user)
        if request.method == 'POST':
            user = request.user
            user_image = request.FILES.get('imageInput')

            if request.user.is_staff == True:
                try:
                    bio = Creator.objects.get(user=user)
                    
                except ObjectDoesNotExist:
                    Creator.objects.create(user=user)
                    bio = Creator.objects.get(user=user)
                bio.bio = request.POST['bio']
                bio.save()   

            if user_image is not None:
                user_profile = UserDetail.objects.filter(username=user)
                if not user_profile:
                    UserDetail.objects.create(user_image=user_image, user=user)
                else:
                    user_profile = UserDetail.objects.get(username=user)
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
        plans = Plan.objects.all()
        return render(request, 'UserSide/payment.html', {'plans': plans})
    else:
        return redirect(login)


def add_comment(request):
    if request.user.is_authenticated:
        image = ImageDetail.objects.get(id=request.POST['id'])
        comment = request.POST['comment']
        user = request.user
        Comments.objects.create(user=user, comment=comment, image=image)
        result = "success"
        return JsonResponse({'result': result}, safe=False)
    else:
        result = "failed"
        return JsonResponse({'result': result}, safe=False)


def orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
        walletTransactions = WalletTransactions.objects.filter(from_user=request.user, transaction_name=WalletTransactions.SADHA).distinct('transaction_id')
        credits_available = Wallet.objects.get(user=request.user)
        no_downloads = Downloads.objects.filter(user=request.user).count()
        context = {
            'orders': orders,
            'walletTransactions': walletTransactions,
            'credits_available': credits_available.credits_available,
            'no_downloads': no_downloads
        }
        return render(request, 'UserSide/orders.html', context)
    else:
        return redirect(login)


def library(request):
    if request.user.is_authenticated:
        downloads = Downloads.objects.filter(user=request.user)
        favourites = Favourites.objects.filter(user=request.user)
        context = {
            'downloads' : downloads,
            'favourites' : favourites
        }
        return render(request, 'UserSide/image_library.html', context)
    else:
        return redirect(login)


def apply_credit(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            image_id = request.POST['id']
            print(request.user)
            wallet = Wallet.objects.get(user=request.user)
            print(wallet.credits_available)
            if wallet.credits_available >= 1:

                transaction_id = uuid.uuid4()

                image = ImageDetail.objects.get(id=image_id)

                #Deducting the amount from the user
                wallet.credits_available -= 2
                wallet.save()
                
                print("This is the user : ", request.user)

                creator = image.user
                print("This is creator : ", creator)

                

                #Adding 50% payment to admin               
                WalletTransactions.objects.create(from_user=request.user, to_user=UserDetail.objects.get(is_superuser=True), transaction_name=WalletTransactions.SADHA, amount=1, transaction_id=transaction_id)
                admin = UserDetail.objects.get(username="admin")
                admin_wallet = Wallet.objects.get(user=admin)
                admin_wallet.credits_available += 1
                admin_wallet.save()
                print("Admin Wallet : ", admin_wallet.credits_available)

                creator_wallet = Wallet.objects.get(user=creator)   
                #Adding 50% of the payment to creator
                WalletTransactions.objects.create(from_user=request.user, to_user=creator, transaction_name=WalletTransactions.SADHA, amount=1, transaction_id=transaction_id)
                creator_wallet.credits_available += 1
                creator_wallet.save()
                print("Creator Wallet : ", creator_wallet.credits_available)

                Downloads.objects.create(user=request.user, image=image)
                print("success")
                return JsonResponse("success", safe=False)
            else:
                print("failed")
                return JsonResponse("failed", safe=False)
    else:
        return JsonResponse("guest", safe=False)
        

def add_favourite(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            image_id = request.POST['id']
            image = ImageDetail.objects.get(id=image_id)
            Favourites.objects.create(user=user, image=image)
            print("success added to favourites --------------------------------------------------------------------- ")
            return JsonResponse("success", safe=False)
        else:
            print("failed")
            return JsonResponse("failed", safe=False)
    else:
        return JsonResponse("guest", safe=False)


def remove_favourite(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            image_id = request.POST['id']
            image = ImageDetail.objects.get(id=image_id)
            favourite = Favourites.objects.get(user=user, image=image)
            favourite.delete()
            print("success Remove from favourites --------------------------------------------------------------------- ")
            return JsonResponse("success", safe=False)
        else:
            print("failed")
            return JsonResponse("failed", safe=False)


def user_payment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            mode = request.POST['mode']
            plan = request.POST['plan']

            option = Plan.objects.get(name=plan)
            amount = option.price

            transaction_id = uuid.uuid4()
            if mode == 'Paypal':
                return JsonResponse({'mode': mode, 'tid': transaction_id, 'amount': amount}, safe=False)
            elif mode == 'Razorpay':
                return JsonResponse({'mode': mode, 'tid': transaction_id, 'amount': amount}, safe=False)
    else:
        return redirect(login)


def success_razorpay(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            date = datetime.datetime.now()
            user = request.user
            mode = 'Razorpay'
            tid = request.POST['tid']
            plan = request.POST['plan']

            try:
                Wallet.objects.get(user=request.user)
            except ObjectDoesNotExist:
                Wallet.objects.create(user=request.user)
                
            wallet = Wallet.objects.get(user=request.user)
            print(request,'gerrrrr')
            user = request.user

            print("Plan _________________", plan)

            if plan == "Personal":
                price = 10
            elif plan == "Professional":
                price = 30
            elif plan == "Business":
                price = 60
            elif plan == "Single Image":
                price = 2

            Order.objects.create(user=request.user, transaction_id=tid, total_price=price, payment_mode=mode, plan=plan)
            WalletTransactions.objects.create(from_user=request.user, to_user=request.user, transaction_name=WalletTransactions.SWANTHAM, amount=price, transaction_id=uuid.uuid4())
            wallet.credits_available = wallet.credits_available + price

            wallet.save()
            
            print("Success")
            return JsonResponse('success', safe=False)
    else:
        return redirect(login)


def success_paypal(request):
    if request.user.is_authenticated:
        date = datetime.datetime.now()
        user = request.user
        mode = 'Paypal'
        id = request.POST['id']
        tid = request.POST['tid']
        total_amount = 5
        image = ImageDetail.objects.get(id=id)
        Order.objects.create(user=user, total_price=total_amount, transaction_id=tid, date_ordered=date, payment_mode=mode, image=image)
        print("Order Successfull")
        return JsonResponse('success', safe=False)
    else:
        return redirect(login)




from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.home, name="home"),
    path('load-more', views.load_more, name="load_more"),
    path('login', views.login, name="login"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('register', views.register, name="register"),
    path('logout', views.logout, name="logout"),

    path('search/', views.search, name="search"),
    path('tag-filter/<str:tag_name>/', views.tag_filter, name="tag_filter"),
    path('view-creator/<str:user>/', views.view_creator, name="view_creator"),

    path('activate-creator/', views.activate_creator, name="activate_creator"),
    path('deactivate-creator/<int:user_id>', views.Deactivate_creator, name="deactivate_creator"),

    path('creator/', views.creator, name="creator"),
    path('creator-contents/', views.creator_contents, name="creator_contents"),
    path('creator-upload/', views.creator_upload, name="creator_upload"),
    path('delete-content/<int:id>', views.delete_content, name="delete_content"),

    path('profile-settings', views.profile_settings, name="profile_settings"),
    path('edit-profile', views.edit_userProfile, name="edit_userProfile"),
    path('creator-settings', views.creator_settings, name="creator_settings"),

    path('view-single/<int:image_id>', views.view_single, name="view_single"),
    path('rate/<int:image_id>', views.rate, name="rate"),
    path('add-comment/', views.add_comment, name="add_comment"),

    path('download-image/', views.download_image, name="download_image"),

    path('add-favourite/', views.add_favourite, name="add_favourite"),
    path('remove-favourite/', views.remove_favourite, name="remove_favourite"),

    path('orders/', views.orders, name="orders"),
    path('library', views.library, name="library"),
    path('payment-page', views.payment_page, name="payment_page"),
    # path('payment/', views.payment, name="payment"),

    path('apply-credit/', views.apply_credit, name="apply_credit"),
    path('user-payment/', views.user_payment, name="user_payment"),
    path('success-razorpay/', views.success_razorpay, name="success_razorpay"),
    path('success-paypal/', views.success_paypal, name="success_paypal"),
]

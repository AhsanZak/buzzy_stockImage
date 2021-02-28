from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('load-more', views.load_more, name="load_more"),
    path('login', views.login, name="login"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('register', views.register, name="register"),
    path('logout', views.logout, name="logout"),

    path('view-creator/<str:user>/', views.view_creator, name="view_creator"),

    path('activate-creator/', views.activate_creator, name="activate_creator"),
    path('deactivate-creator/<int:user_id>', views.Deactivate_creator, name="deactivate_creator"),

    path('creator', views.creator, name="creator"),
    path('creator-contents', views.creator_contents, name="creator_contents"),
    path('creator-upload', views.creator_upload, name="creator_upload"),
    path('delete-content/<int:id>', views.delete_content, name="delete_content"),

    path('profile-settings', views.profile_settings, name="profile_settings"),
    path('edit-profile', views.edit_userProfile, name="edit_userProfile"),
    path('creator-settings', views.creator_settings, name="creator_settings"),

    path('view-single/<int:image_id>', views.view_single, name="view_single"),
    path('rate/<int:image_id>', views.rate, name="rate"),
    path('download-image/', views.download_image, name="download_image"),
    path('downloads', views.downloads, name="downloads"),
    path('payment-page', views.payment_page, name="payment_page")
]
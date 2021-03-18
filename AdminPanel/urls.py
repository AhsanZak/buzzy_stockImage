from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_panel, name="admin_panel"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="admin_logout"),

    path('manage-user', views.manage_user, name="manage-user"),
    path('create-user', views.create_user, name="create_user"),
    path('update-user/<int:id>', views.update_user, name="update_user"),
    path('edit-user/<int:id>', views.edit_user, name="edit_user"),
    path('block-user/<int:user_id>', views.block_user, name="block_user"),
    path('delete-user/<int:id>', views.delete_user, name="delete_user"),

    path('manage-creator', views.manage_creator, name="manage_creator"),
    path('add-creator', views.add_creator, name="add_creator"),
    path('block-creator/<int:user_id>', views.block_creator, name="block_creator"),

    path('contents', views.contents, name="contents"),
    path('add-contents', views.add_contents, name="add_contents"),
    path('approve-contents', views.approve_contents, name="approve_contents"),
    path('disapprove-contents', views.disapprove_contents, name="disapprove_contents"),
    path('approved-contents/<int:id>', views.approved_contents, name="approved_contents"),
    path('disapproved-contents/<int:id>', views.disapproved_contents, name="disapproved_contents"),
    path('admin-delete-content/<int:id>', views.admin_delete_content, name="admin_delete_content"),

    path('category/', views.category, name="category"),
    path('add-category/', views.add_category, name="add_category"),
    path('delete-category/', views.delete_category, name="delete_category"),
]

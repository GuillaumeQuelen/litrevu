from django.urls import path
from . import views

urlpatterns = [
    path('flux/', views.flux, name='flux'),
    path('ticket/create/', views.create_ticket, name='create_ticket'),
    path('ticket/<int:ticket_id>/update/', views.update_ticket, name='update_ticket'),
    path('ticket/<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),
    path('ticket/<int:ticket_id>/review/', views.create_review, name='create_review'),
    path('review/<int:review_id>/update/', views.update_review, name='update_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('follow/', views.follow_users, name='follow_users'),
    path('follow/<int:follow_id>/unfollow/', views.unfollow_user, name='unfollow_user'),
    path('review/create/', views.create_ticket_and_review, name='create_ticket_and_review'),
    path('posts/', views.my_posts, name='my_posts'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='argument-home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name='post-delete'),
    path('comment/<int:post_pk>/', views.comment_create, name='comment-create'),
    path('reply/<int:comment_pk>/', views.reply_create, name='reply-create'),
]

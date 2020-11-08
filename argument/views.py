from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment
from django import forms
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic


class PostListView(ListView):
    model = Post
    template_name = 'argument/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post
    def get_context_data(self, **kwargs):
        # detailページを訪れたタイミングで閲覧数をカウント
        self.object.views += 1
        self.object.save()
        
        context = super().get_context_data(**kwargs)
        # どのコメントにも紐つかないコメント(記事へのコメント)を取得
        context["comment_list"] = self.object.comment_set.filter(parent__isnull=True) 
        return context
    

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    success_url = ('/')

    def form_valid(self, form):
        form.instance.advocate = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.advocate = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.advocate:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.advocate:
            return True
        return False

class PostRankingView(ListView):
    model = Post
    template_name = 'argument/ranking.html'
    context_object_name = 'posts'
    ordering = ['-views']

# コメントフォーム
CommentForm = forms.modelform_factory(Comment, fields=('content', ))

@login_required
def comment_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    author = request.user
    form = CommentForm(request.POST or None)

    if request.method == 'POST':
        comment = form.save(commit=False)
        comment.post = post
        comment.author = author
        comment.save()
        return redirect('post-detail', pk=post.pk)
    context = {
        'form': form,
        'post': post,
        'author': author,
    }
    return render(request, 'argument/comment_form.html', context)

@login_required
def reply_create(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    post = comment.post
    author = request.user
    form = CommentForm(request.POST or None)
    
    if request.method == 'POST':
        reply = form.save(commit=False)
        reply.parent = comment
        reply.post = post
        reply.author = author
        reply.save()
        return redirect('post-detail', pk=post.pk)
    context = {
        'form': form,
        'post': post,
        'comment': comment,
        'author': author,
    }
    return render(request, 'argument/comment_form.html', context)
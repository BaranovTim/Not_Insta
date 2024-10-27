from django.contrib.auth.decorators import login_required
from.forms import PostForm
from rest_framework.viewsets import ModelViewSet
from .serializers import PostSerializer
from .models import Post, Like, Comment
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import LoginForm, CommentForm
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from .serializers import CommentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response



class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("You are not allowed to edit this post.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You are not allowed to delete this post.")
        instance.delete()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            post.likes -= 1
        else:
            post.likes += 1
        post.save()
        return Response({'likes_count': post.like_set.count()})

def index(request):
    posts = Post.objects.all()
    liked_posts = []

    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            # Create a new comment instance without saving it yet
            comment = comment_form.save(commit=False)
            comment.author = request.user
            post_id = request.POST.get('post_id')  # Get the post ID from the form
            comment.post_id = post_id
            comment.save()
            return redirect('index')
    else:
        comment_form = CommentForm()


    return render(request, 'main/index.html', {
        'Posts': posts,
        'liked_posts': liked_posts,
        'comment_form': comment_form,
        'comments': Comment.objects.all()
    })



@login_required
def post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'main/post.html', {"form": form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('index')  # Only the author can edit

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PostForm(instance=post)

    return render(request, 'main/post_edit.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Check if the user has already liked the post
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if created:
        post.likes += 1
    else:
        post.likes -= 1
        like.delete()

    post.save()
    return redirect('index')
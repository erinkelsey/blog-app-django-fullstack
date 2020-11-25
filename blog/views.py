from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse_lazy

from blog.models import Post, Comment
from blog.forms import CommentForm, PostForm


################## CLASS-BASED VIEWS #####################
class AboutView(TemplateView):
    """
    View for rendering the About page

    Template for this view is about.html. 
    """
    template_name = 'about.html'


class PostListView(ListView):
    """
    View for rendering the list of Posts.

    Template for this view is post_list.html.
    """
    model = Post

    def get_queryset(self):
        """
        Gets the Post objects to show on the main Post list page. 

        Only returns published posts. 

        Returns:
            QuerySet<Post>: the posts to display
        """
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    """
    View for rendering a specific Post's details. 

    Template for this view is post_detail.html.

    PK for Post is passed in URL. 
    """
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    """
    View for creating a new Post. 

    Template for this view is post_form.html.

    User must be logged in to access.

    Redirects to the new Post's details page on success. 
    """
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    model = Post
    form_class = PostForm


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for update a specific Post. 

    Template for this view is post_detail.html.

    PK for Post is passed in URL.

    User must be logged in to access.

    Redirects to the updated Post's details page on success. 
    """
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    model = Post
    form_class = PostForm


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting a specific Post. 

    Template for this view is post_confirm_delete.html.

    PK for Post is passed in URL.

    User must be logged in to access.

    Redirects to the Post list page, on success. 
    """
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    model = Post
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin, ListView):
    """
    View for rendering a the list of unpublished (draft) Posts. 

    Template for this view is post_draft_list.html.

    PK for Post is passed in URL.

    User must be logged in to access.

    Redirects to the updated Post list. 
    """
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        """
        Gets the Post objects to show on the draft list page. 

        Only returns unpublished posts. 

        Returns:
            QuerySet<Post>: the posts to display
        """
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


################## FUNCTION-BASED VIEWS #####################
@login_required
def add_comment_to_post(request, pk):
    """
    View for adding a comment to a post.

    If method is POST, add the comment from CommentForm to Post. 
    Redirects to the Post's detail page, on success. 

    Else show comment_form.html template. 

    Redirects to 404, if the Post cannot be found. 

    Args:
        pk (int): PK for Post to add comment to
    """

    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect('post_detail', pk=post.pk)

    else:
        form = CommentForm()

    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    """
    View for approving a comment on a post.

    Redirects to the Post's detail page, on success. 

    Redirects to 404, if the Post cannot be found. 

    Args:
        pk (int): PK for Post to add comment to
    """

    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    """
    View for deleting a comment from a post.

    Redirects to the Post's detail page, on success. 

    Redirects to 404, if the Post cannot be found. 

    Args:
        pk (int): PK for Post to delete comment from
    """

    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


@login_required
def post_publish(request, pk):
    """
    Publish a Post with a specific PK.

    Redirects to the Post's detail page, on success. 

    Redirects to 404, if the Post cannot be found. 

    Args:
        pk (int): the PK for the Post to publish
    """
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

from django.db import models
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        """
        Publish this post, by setting published_date to current timestamp.
        """
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        """
        Get the approved comments for this Post.

        Returns:
            QuerySet<Comment>: the approved comments for this Post
        """
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        """
        Redirects to this Post's details page. 
        """
        return reverse("post_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        'blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        """
        Approve this comment.
        """
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        """
        Redirect to the Post list page.  
        """
        return reverse("post_list")

    def __str__(self):
        return self.text

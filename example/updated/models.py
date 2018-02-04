from django.db import models
from .behaviors import Authorable, Permalinkable, Timestampable, Publishable
from .querysets import AuthorableQuerySet, PublishableQuerySet

#from model_utils.managers import QueryManager # PassThroughManager


class BlogPostQuerySet(AuthorableQuerySet, PublishableQuerySet):
    pass

class BlogPostManager(models.Manager):
    def get_queryset(self):
        return BlogPostQuerySet(self.model, using=self._db)  # Important!
    
    def published(self):
        return self.get_queryset().published()

    def authored_by(self, author):
        return self.get_queryset().authored_by(author)


class BlogPost(Authorable, Permalinkable, Timestampable, Publishable, models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    
    url_name = "blog-post"#

    @property
    def slug_source(self):
        return self.title
    
    objects = BlogPostManager()
    #QueryManager.get_queryset(BlogPostQuerySet)()
    #objects = PassThroughManager.for_queryset_class(BlogPostQuerySet)()


class BlogComment(Authorable, Permalinkable, Timestampable, models.Model):
    post = models.ForeignKey(BlogPost, on_delete='PROTECT', related_name='comments')
    subject = models.CharField(max_length=255)
    body = models.TextField()

    url_name = 'blog-comment'
    
    def get_url_kwargs(self, **kwargs):
        return super(BlogComment, self).get_url_kwargs(post_slug=self.post.name, **kwargs) #post.slug, **kwargs)
    
    @property
    def slug_source(self):
        return self.subject

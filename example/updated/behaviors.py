from django.db import models
from django.contrib.auth.models import User

#from model_utils.managers import QueryManager #  PassThroughManager

from .querysets import PublishableQuerySet, AuthorableQuerySet


class Permalinkable(models.Model):
    slug = models.SlugField()
    
    class Meta:
        abstract = True
    
    def get_url_kwargs(self, **kwargs):
        kwargs.update(getattr(self, 'url_kwargs', {}))
        return kwargs
    

    #@models.permalink
    def get_absolute_url(self):
        url_kwargs = self.get_url_kwargs(slug=self.slug)
        return (url_kwargs)
        #return (self.url_name, (), url_kwargs)
    
    #def pre_save(self, instance, a  dd):
    def pre_save(self, instance):        
        from django.utils.text import slugify
        if not instance.slug:
            instance.slug = slugify(self.slug.name) # .slug_source)

class PublishManger(models.Manager):
    def get_queryset(self):
        return PublishableQuerySet(self.model, using=self._db)  # Important!

class Publishable(models.Model):
    publish_date = models.DateTimeField(null=True)
    
    class Meta:
        abstract = True
    
    objects = PublishManger()
    #QueryManager.get_queryset(PublishableQuerySet)() 
    #objects = PassThroughManager.for_queryset_class(PublishableQuerySet)()

    def publish_on(self, date=None):
        from django.utils import timezone
        if not date:
            date = timezone.now()
        self.publish_date = date
        self.save()

    @property
    def is_published(self):
        from django.utils import timezone
        return self.publish_date and self.publish_date < timezone.now()


class AuthorManager(models.Manager):
    def get_queryset(self):
        return AuthorableQuerySet(self.model, using=self._db)  # Important!

class Authorable(models.Model):
    author = models.ForeignKey(User,on_delete='PROTECT', null=True)
    
    class Meta:
        abstract = True
    
    objects = AuthorManager()
    #QueryManager.get_queryset(AuthorableQuerySet)()
    #objects = PassThroughManager.for_queryset_class(AuthorableQuerySet)()


class Timestampable(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

from django.test import TestCase
from django.utils import timezone
from .models import BlogPost


class BlogPostTestCase(TestCase):
    
    def test_published_blogpost(self):
        print('start 1...')        
        blogpost = BlogPost.objects.create(publish_date=timezone.now())
        print(f'blogpost.publish_date {blogpost.publish_date}')
        self.assertTrue(blogpost.is_published)
        self.assertIn(blogpost, BlogPost.objects.published())
        print('end 1...')        

    def test_unpublished_blogpost(self):
        print('start 2...')      
        blogpost = BlogPost.objects.create(publish_date=None)
        print(f'blogpost.publish_date {blogpost.publish_date}')
        self.assertFalse(blogpost.is_published)
        self.assertNotIn(blogpost, BlogPost.objects.published())
        print('end 2...')              

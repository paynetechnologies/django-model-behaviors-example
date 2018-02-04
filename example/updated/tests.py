#from django.test import TestCase
import unittest
from django.utils import timezone
from .models import BlogPost

class BehaviorTestCaseMixin(object):
    def get_model(self):
        return getattr(self, 'model')
    
    def create_instance(self, **kwargs):
        print('**kwargs {**kwargs}')
        return BlogPost.objects.create(**kwargs)


class PublishableTests(BehaviorTestCaseMixin):
    def test_published(self):
        obj = self.create_instance(publish_date=timezone.now())
        return obj

    
    def test_unpublished(self):
        obj = self.create_instance(publish_date=None)
        return obj


class BehaviorTest(unittest.TestCase):
    def setUp(self):
        print('setUp...')
        self.test1 = PublishableTests()
        self.test2 = PublishableTests()
       
    def testA(self):
        print("Test1.test_published")
        obj = self.test1.test_published()
        self.assertTrue(obj.is_published)
        self.assertIn(obj, BlogPost.objects.published())
    
    def testB(self):
        print("Test2.test_unpublished")
        obj = self.test2.test_unpublished()
        self.assertNotIn(obj, BlogPost.objects.published())

    def tearDown(self):
        print('tearDown...')


    # class BlogPostTestCase(PublishableTests):
    #     model = BlogPost
        
    #     def create_instance(self, **kwargs):
    #         return BlogPost.objects.create(**kwargs)

"""
class BlogPostTestCase(PublishableTests, AuthorableTests, PermalinkableTests, TimestampableTests, TestCase):
    model = BlogPost
    
    def create_instance(self, **kwargs):
        return BlogPost.objects.create(**kwargs)

    def test_blog_specific_functionality(self):
        ...
"""
if __name__ == '__main__':  
    unittest.main(warnings='ignore') 
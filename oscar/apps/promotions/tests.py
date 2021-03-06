import httplib

from django.utils import unittest
from django.core.exceptions import ValidationError
from django.core.urlresolvers import resolve
from django.test import Client

from oscar.apps.promotions.models import * 

class HomepageTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_homepage(self):
        response = self.client.get("/")
        self.assertEquals(httplib.OK, response.status_code)



class PromotionTest(unittest.TestCase):

    def test_promotion_cannot_be_saved_without_content(self):
        with self.assertRaises(ValidationError):
            p = Promotion(name='Dummy')
            p.full_clean() 
            
    def test_html_is_returned_for_pod_html(self):
        p = Promotion(name='Dummy', pod_image='/dummy-image.jpg')
        self.assertTrue(len(p.get_pod_html()) > 0)
        
    def test_html_is_returned_for_pod_with_link_html(self):
        p = Promotion(name='Dummy', pod_image='/dummy-image.jpg', link_url="http://www.example.com")
        self.assertTrue(len(p.get_pod_html()) > 0)


class PagePromotionTest(unittest.TestCase):
    
    def setUp(self):
        self.promotion = Promotion.objects.create(name='Dummy', link_url='http://www.example.com')
        self.page_prom = PagePromotion.objects.create(promotion=self.promotion,
                                                      position=RAW_HTML,
                                                      page_url='/')
    
    def test_clicks_start_at_zero(self):
        self.assertEquals(0, self.page_prom.clicks)
    
    def test_click_is_recorded(self):
        self.page_prom.record_click()
        self.assertEquals(1, self.page_prom.clicks)

    def test_get_link(self):
        link = self.page_prom.get_link()
        match = resolve(link)
        self.assertEquals('oscar-page-promotion-click', match.url_name)


class KeywordPromotionTest(unittest.TestCase):
    
    def setUp(self):
        self.promotion = Promotion.objects.create(name='Dummy', link_url='http://www.example.com')
        self.kw_prom = KeywordPromotion.objects.create(promotion=self.promotion,
                                                       position=RAW_HTML,
                                                       keyword='cheese')
    
    def test_clicks_start_at_zero(self):
        self.assertEquals(0, self.kw_prom.clicks)
    
    def test_click_is_recorded(self):
        self.kw_prom.record_click()
        self.assertEquals(1, self.kw_prom.clicks)
        
    def test_get_link(self):
        link = self.kw_prom.get_link()
        match = resolve(link)
        self.assertEquals('oscar-keyword-promotion-click', match.url_name)
        

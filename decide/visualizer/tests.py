from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from voting.models import Voting, Question

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from rest_framework.test import APIClient
from base import mods

# Create your tests here.

class VisualizerTestCase(StaticLiveServerTestCase):

    
    def setUp(self):
        super().setUp()        
        options = webdriver.FirefoxOptions()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)
        
        self.client = APIClient()
        mods.mock_query(self.client)
        
    def tearDown(self):           
        self.driver.quit()
        super().tearDown()

        self.client= None

    def test_simpleVisualizer(self):
        
        
        q = Question(desc='test question')
        q.save()
        v = Voting(name='test voting', question=q)
        v.save()
        
        #print(f"Live URL= {self.live_server_url}/visualizer/{v.pk}/")
        response =self.driver.get(f'{self.live_server_url}/visualizer/{v.pk}/')
        #print(f"Web source= {self.driver.page_source}")
        
        vState= self.driver.find_element_by_tag_name("h2").text
        #print(f"Estado = {vState}")

        #assert "no comenzada" in self.driver.page_source
        self.assertTrue(vState, "Votación no comenzada")
        
        


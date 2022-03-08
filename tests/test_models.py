"""
Test cases for Promotion Model

"""
import logging
import unittest
import os
from service.models import Promotion, DataValidationError, db

######################################################################
#  <your resource name>   M O D E L   T E S T   C A S E S
######################################################################
class TestPromotion(unittest.TestCase):
    """ Test Cases for Promotion Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        pass

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        db.drop_all()
        db.create_all()

    def tearDown(self):
        """ This runs after each test """
        pass

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_created(self):
        """ Test Promotion.create """
        allPromotions = Promotion.query.all()
        self.assertEquals(len(allPromotions), 0)

        promo = Promotion()
        promo.name = "30 days free"
        promo.create()

        self.assertEquals(len(Promotion.query.all()), 1)
        self.assertEquals(Promotion.query.filter_by(id=1).first().name, "30 days free")

        #misc
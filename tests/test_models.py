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
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.drop_all()
        db.create_all()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_promotion(self):
        """Create a promotion and assert that it exists"""
        promotion = Promotion(name="first_month_free")
        self.assertTrue(promotion is not None)
        self.assertEqual(promotion.id, None)
        self.assertEqual(promotion.name, "first_month_free")

    def test_add_a_promotion(self):
        """Create a promotion and add it to the database"""
        promotions = Promotion.all()
        self.assertEqual(promotions, [])
        promotion = Promotion(name="first_month_free")
        self.assertTrue(promotion is not None)
        self.assertEqual(promotion.id, None)
        promotion.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(promotion.id, 1)
        promotions = Promotion.all()
        self.assertEqual(len(promotions), 1)

    def test_update_a_promotion(self):
        """Update a Promotion"""
        promotion = Promotion(name="first_month_free")
        logging.debug(promotion)
        promotion.create()
        logging.debug(promotion)
        self.assertEqual(promotion.id, 1)
        # Change it an save it
        original_id = promotion.id
        promotion.save()
        self.assertEqual(promotion.id, original_id)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        promotions = Promotion.all()
        self.assertEqual(len(promotions), 1)
        self.assertEqual(promotions[0].id, 1)

    def test_delete_a_promotion(self):
        """Delete a Promotion"""
        promotion = Promotion(name="first_month_free")
        promotion.create()
        self.assertEqual(len(Promotion.all()), 1)
        # delete the promotion and make sure it isn't in the database
        promotion.delete()
        self.assertEqual(len(Promotion.all()), 0)

    def test_serialize_a_promotion(self):
        """Test serialization of a Promotion"""
        promotion = Promotion(name="first_month_free")
        data = promotion.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], promotion.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], promotion.name)
        
    def test_deserialize_a_promotion(self):
        """Test deserialization of a Promotion"""
        data = {
            "id": 1,
            "name": "first_month_free",
        }
        promotion = Promotion()
        promotion.deserialize(data)
        self.assertNotEqual(promotion, None)
        self.assertEqual(promotion.id, None)
        self.assertEqual(promotion.name, "first_month_free")

    def test_deserialize_missing_data(self):
        """Test deserialization of a Promotion with missing data"""
        data = {"id": 1}
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_deserialize_bad_data(self):
        """Test deserialization of bad data"""
        data = "this is not a dictionary"
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_find_promotion(self):
        """Find a Promotion by ID"""
        promotions = [
            Promotion(name="ten_percent_discount"),
            Promotion(name="five_dollars_off"),
            Promotion(name="two_week_trial"),
        ]
        for promotion in promotions:
            promotion.create()
        logging.debug(promotions)
        # make sure they got saved
        self.assertEqual(len(Promotion.all()), 3)
        # find the 2nd promotion in the list
        promotion = Promotion.find(promotions[1].id)
        self.assertIsNot(promotion, None)
        self.assertEqual(promotion.id, promotions[1].id)
        self.assertEqual(promotion.name, promotions[1].name)

    def test_find_by_name(self):
        """Find a Promotion by Name"""
        Promotion(name="first_month_free").create()
        promotions = Promotion.find_by_name("first_month_free")
        self.assertEqual(promotions[0].name, "first_month_free")

    def test_find_or_404_found(self):
        """Find or return 404 found"""
        promotions = [
            Promotion(name="ten_percent_discount"),
            Promotion(name="five_dollars_off"),
            Promotion(name="two_week_trial"),
        ]
        for promotion in promotions:
            promotion.create()

        promotion = Promotion.find_or_404(promotions[1].id)
        self.assertIsNot(promotion, None)
        self.assertEqual(promotion.id, promotions[1].id)
        self.assertEqual(promotion.name, promotions[1].name)
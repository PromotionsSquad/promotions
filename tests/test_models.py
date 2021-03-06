# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Promotion Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_promotions.py:TestPetModel

"""
import os
import logging
import unittest
from datetime import datetime
from werkzeug.exceptions import NotFound
from factories import PromotionFactory
from service.models import Promotion, DataValidationError, db
from service import app
from sqlalchemy.sql import func

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  P R O M O T I O N   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestPromotionModel(unittest.TestCase):
    """Test Cases for Promotion Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Promotion.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_promotion(self):
        """Create a promotion and assert that it exists"""
        promotion = Promotion(name="first_month_free", starts_at="2022-04-01", ends_at="2022-06-01", active=False)
        self.assertTrue(promotion is not None)
        self.assertEqual(promotion.id, None)
        self.assertEqual(promotion.name, "first_month_free")
        self.assertEqual(promotion.starts_at, "2022-04-01")
        self.assertEqual(promotion.ends_at, "2022-06-01")
        self.assertEqual(promotion.active, False)

    def test_add_a_promotion(self):
        """Create a promotion and add it to the database"""
        promotions = Promotion.all()
        self.assertEqual(promotions, [])
        promotion = Promotion(name="first_month_free", starts_at="2022-04-01", ends_at="2022-06-01", active=False)
        self.assertTrue(promotion is not None)
        self.assertEqual(promotion.id, None)
        promotion.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(promotion.id, 1)
        promotions = Promotion.all()
        self.assertEqual(len(promotions), 1)

    def test_read_a_promotion(self):
        """Read a Promotion"""
        promotion = PromotionFactory()
        logging.debug(promotion)
        promotion.create()
        self.assertEqual(promotion.id, 1)
        # Fetch it back
        found_promotion = Promotion.find(promotion.id)
        self.assertEqual(found_promotion.id, promotion.id)
        self.assertEqual(found_promotion.name, promotion.name)
        self.assertEqual(found_promotion.starts_at, promotion.starts_at)
        self.assertEqual(found_promotion.ends_at, promotion.ends_at)
        self.assertEqual(found_promotion.active, promotion.active)

    def test_list_all_promotions(self):
        """List Promotions in the database"""
        promotions = Promotion.all()
        self.assertEqual(promotions, [])
        # Create 5 Promotions
        for _ in range(5):
            promotion = PromotionFactory()
            promotion.create()
        # See if we get back 5 promotions
        promotions = Promotion.all()
        self.assertEqual(len(promotions), 5)

    def test_update_a_promotion(self):
        """Update a Promotion"""
        promotion = PromotionFactory()
        logging.debug(promotion)
        promotion.create()
        logging.debug(promotion)
        self.assertEqual(promotion.id, 1)
        # Change it an save it
        promotion.starts_at = "2022-04-02"
        original_id = promotion.id
        promotion.update()
        self.assertEqual(promotion.id, original_id)
        self.assertEqual(promotion.starts_at, datetime(2022, 4, 2))
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        promotions = Promotion.all()
        self.assertEqual(len(promotions), 1)
        self.assertEqual(promotions[0].id, 1)
        self.assertEqual(promotions[0].starts_at, datetime(2022, 4, 2))

    def test_delete_a_promotion(self):
        """Delete a Promotion"""
        promotion = PromotionFactory()
        promotion.create()
        self.assertEqual(len(Promotion.all()), 1)
        # delete the promotion and make sure it isn't in the database
        promotion.delete()
        self.assertEqual(len(Promotion.all()), 0)

    def test_serialize_a_promotion(self):
        """Test serialization of a Promotion"""
        promotion = PromotionFactory()
        data = promotion.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], promotion.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], promotion.name)
        self.assertIn("starts_at", data)
        self.assertEqual(data["starts_at"], "2022-04-01")
        self.assertIn("ends_at", data)
        self.assertEqual(data["ends_at"], "2022-06-30")
        self.assertIn("active", data)
        self.assertEqual(data["active"], promotion.active)

    def test_deserialize_a_promotion(self):
        """Test deserialization of a Promotion"""
        data = {
            "id": 1,
            "name": "30_days_free",
            "starts_at": "2022-04-03",
            "ends_at": "2022-06-30",
            "active": True,
        }
        promotion = Promotion()
        promotion.deserialize(data)
        self.assertNotEqual(promotion, None)
        self.assertEqual(promotion.id, None)
        self.assertEqual(promotion.name, "30_days_free")
        self.assertEqual(promotion.starts_at, datetime(2022, 4, 3))
        self.assertEqual(promotion.ends_at, datetime(2022, 6, 30))
        self.assertEqual(promotion.active, True)

    def test_deserialize_missing_data(self):
        """Test deserialization of a Promotion with missing data"""
        data = {"id": 1, "name": "30_days_free"}
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_deserialize_bad_data(self):
        """Test deserialization of bad data"""
        data = "this is not a dictionary"
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_deserialize_bad_active(self):
        """Test deserialization of bad active attribute"""
        test_promotion = PromotionFactory()
        data = test_promotion.serialize()
        data["active"] = "true"
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_find_promotion(self):
        """Find a Promotion by ID"""
        promotions = PromotionFactory.create_batch(3)
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
        self.assertEqual(promotion.starts_at, promotions[1].starts_at)
        self.assertEqual(promotion.ends_at, promotions[1].ends_at)
        self.assertEqual(promotion.active, promotions[1].active)

    def test_find_by_name(self):
        """Find a Promotion by Name"""
        Promotion(name="first_month_free", starts_at="2022-04-01", ends_at="2022-06-01", active=False).create()
        Promotion(name="ten_percent_discount", starts_at="2022-05-01", ends_at="2022-07-01", active=True).create()
        promotions = Promotion.find_by_name("first_month_free")
        self.assertEqual(promotions[0].name, "first_month_free")
        self.assertEqual(promotions[0].starts_at, datetime(2022,4,1))
        self.assertEqual(promotions[0].ends_at, datetime(2022,6,1))
        self.assertEqual(promotions[0].active, False)

    def test_find_by_active(self):
        """Find Promotions by Active"""
        Promotion(name="first_month_free", starts_at="2022-04-01", ends_at="2022-06-01", active=False).create()
        Promotion(name="ten_percent_discount", starts_at="2022-05-01", ends_at="2022-07-01", active=True).create()
        promotions = Promotion.find_by_active(True)
        promotion_list = list(promotions)
        self.assertEqual(len(promotion_list), 1)
        self.assertEqual(promotions[0].name, "ten_percent_discount")
        self.assertEqual(promotions[0].starts_at, datetime(2022,5,1))
        self.assertEqual(promotions[0].ends_at, datetime(2022,7,1))
        self.assertEqual(promotions[0].active, True)

    def test_find_or_404_found(self):
        """Find or return 404 found"""
        promotions = PromotionFactory.create_batch(3)
        for promotion in promotions:
            promotion.create()

        promotion = Promotion.find_or_404(promotions[1].id)
        self.assertIsNot(promotion, None)
        self.assertEqual(promotion.id, promotions[1].id)
        self.assertEqual(promotion.name, promotions[1].name)
        self.assertEqual(promotion.active, promotions[1].active)

    def test_find_or_404_not_found(self):
        """Find or return 404 NOT found"""
        self.assertRaises(NotFound, Promotion.find_or_404, 0)

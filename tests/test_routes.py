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
Promotion API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN

  While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_service.py:TestPromotionServer
"""

import os
import logging
import unittest

# from unittest.mock import MagicMock, patch
from urllib.parse import quote_plus
from service import app, status
from service.models import db, init_db
from factories import PromotionFactory

# Disable all but critical errors during normal test run
# uncomment for debugging failing tests
logging.disable(logging.CRITICAL)

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/promotions"
CONTENT_TYPE_JSON = "application/json"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestPromotionServer(unittest.TestCase):
    """Promotion Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_promotions(self, count):
        """Factory method to create promotions in bulk"""
        promotions = []
        for _ in range(count):
            test_promotion = PromotionFactory()
            resp = self.app.post(
                BASE_URL, json=test_promotion.serialize(), content_type=CONTENT_TYPE_JSON
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test promotion"
            )
            new_promotion = resp.get_json()
            test_promotion.id = new_promotion["id"]
            promotions.append(test_promotion)
        return promotions

    def test_index(self):
        """Test the Home Page"""
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Promotion Demo REST API Service")

    def test_get_promotion_list(self):
        """Get a list of Promotions"""
        self._create_promotions(5)
        resp = self.app.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_get_promotion(self):
        """Get a single Promotion"""
        # get the id of a promotion
        test_promotion = self._create_promotions(1)[0]
        resp = self.app.get(
            "/promotions/{}".format(test_promotion.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_promotion.name)

    def test_get_promotion_not_found(self):
        """Get a Promotion thats not found"""
        resp = self.app.get("/promotions/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_promotion(self):
        """Create a new Promotion"""
        test_promotion = PromotionFactory()
        logging.debug(test_promotion)
        resp = self.app.post(
            BASE_URL, json=test_promotion.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_promotion = resp.get_json()
        self.assertEqual(new_promotion["name"], test_promotion.name, "Names do not match")
        self.assertEqual(
            new_promotion["category"], test_promotion.category, "Categories do not match"
        )
        self.assertEqual(
            new_promotion["available"], test_promotion.available, "Availability does not match"
        )
        # Check that the location header was correct
        resp = self.app.get(location, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_promotion = resp.get_json()
        self.assertEqual(new_promotion["name"], test_promotion.name, "Names do not match")
        self.assertEqual(
            new_promotion["category"], test_promotion.category, "Categories do not match"
        )
        self.assertEqual(
            new_promotion["available"], test_promotion.available, "Availability does not match"
        )

    def test_create_promotion_no_data(self):
        """Create a Promotion with missing data"""
        resp = self.app.post(BASE_URL, json={}, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_promotion_no_content_type(self):
        """Create a Promotion with no content type"""
        resp = self.app.post(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_promotion_bad_available(self):
        """ Create a Promotion with bad available data """
        test_promotion = PromotionFactory()
        logging.debug(test_promotion)
        # change available to a string
        test_promotion.available = "true"
        resp = self.app.post(
            BASE_URL, json=test_promotion.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_promotion(self):
        """Delete a Promotion"""
        test_promotion = self._create_promotions(1)[0]
        resp = self.app.delete(
            "{0}/{1}".format(BASE_URL, test_promotion.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get(
            "{0}/{1}".format(BASE_URL, test_promotion.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_promotion_list_by_category(self):
        """Query Promotions by Category"""
        promotions = self._create_promotions(10)
        test_category = promotions[0].category
        category_promotions = [promotion for promotion in promotions if promotion.category == test_category]
        resp = self.app.get(
            BASE_URL, query_string="category={}".format(quote_plus(test_category))
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(category_promotions))
        # check the data just to be sure
        for promotion in data:
            self.assertEqual(promotion["category"], test_category)
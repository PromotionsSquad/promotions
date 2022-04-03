# Copyright 2016, 2021 John Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Models for Promotion Demo Service

All of the models are stored in this module

Models
------
Promotion - A Promotion used in the Promotion Store

Attributes:
-----------
name (string) - the name of the promotion

"""
import logging
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


def init_db(app):
    """Initialize the SQLAlchemy app"""
    Promotion.init_db(app)


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Promotion(db.Model):
    """
    Class that represents a Promotion

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    starts_at = db.Column(db.DateTime)
    ends_at = db.Column(db.DateTime)
    active = db.Column(db.Boolean())

    ##################################################
    # INSTANCE METHODS
    ##################################################

    def __repr__(self):
        return "<Promotion %r id=[%s]>" % (self.name, self.id)

    def create(self):
        """
        Creates a Promotion to the database
        """
        logger.info("Creating %s", self.name)
        # id must be none to generate next primary key
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Promotion to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """Removes a Promotion from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self) -> dict:
        """Serializes a Promotion into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "starts_at": self.starts_at.strftime("%Y-%m-%d"),
            "ends_at": self.ends_at.strftime("%Y-%m-%d"),
            "active": self.active,
        }

    def deserialize(self, data: dict):
        """
        Deserializes a Promotion from a dictionary
        Args:
            data (dict): A dictionary containing the Promotion data
        """
        try:
            self.name = data["name"]
            self.starts_at = datetime.strptime(data["starts_at"], "%Y-%m-%d")
            self.ends_at = datetime.strptime(data["ends_at"], "%Y-%m-%d")
            if isinstance(data["active"], bool):
                self.active = data["active"]
            else:
                raise DataValidationError(
                    "Invalid type for boolean [active]: "
                    + str(type(data["active"]))
                )
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0])
        except KeyError as error:
            raise DataValidationError("Invalid promotion: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid promotion: body of request contained bad or no data " + str(error)
            )
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def init_db(cls, app: Flask):
        """Initializes the database session

        :param app: the Flask app
        :type data: Flask

        """
        logger.info("Initializing database")
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls) -> list:
        """Returns all of the Promotions in the database"""
        logger.info("Processing all Promotions")
        return cls.query.all()

    @classmethod
    def find(cls, promotion_id: int):
        """Finds a Promotion by it's ID

        :param promotion_id: the id of the Promotion to find
        :type promotion_id: int

        :return: an instance with the promotion_id, or None if not found
        :rtype: Promotion

        """
        logger.info("Processing lookup for id %s ...", promotion_id)
        return cls.query.get(promotion_id)

    @classmethod
    def find_or_404(cls, promotion_id: int):
        """Find a Promotion by it's id

        :param promotion_id: the id of the Promotion to find
        :type promotion_id: int

        :return: an instance with the promotion_id, or 404_NOT_FOUND if not found
        :rtype: Promotion

        """
        logger.info("Processing lookup or 404 for id %s ...", promotion_id)
        return cls.query.get_or_404(promotion_id)

    @classmethod
    def find_by_name(cls, name: str) -> list:
        """Returns all Promotions with the given name

        :param name: the name of the Promotions you want to match
        :type name: str

        :return: a collection of Promotions with that name
        :rtype: list

        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_category(cls, category: str) -> list:
        """Returns all of the Promotions in a category

        :param category: the category of the Promotions you want to match
        :type category: str

        :return: a collection of Promotions in that category
        :rtype: list

        """
        logger.info("Processing category query for %s ...", category)
        return cls.query.filter(cls.category == category)

    @classmethod
    def find_by_active(cls, active: bool = True) -> list:
        """Returns all Promotions by their active

        :param active: True for promotions that are active
        :type active: bool

        :return: a collection of Promotions that are active
        :rtype: list

        """
        logger.info("Processing active query for %s ...", active)
        return cls.query.filter(cls.active == active)

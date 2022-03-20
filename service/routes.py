# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
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
Promotion Store Service

Paths:
------
GET /promotions - Returns a list all of the Promotions
GET /promotions/{id} - Returns the Promotion with a given id number
POST /promotions - creates a new Promotion record in the database
PUT /promotions/{id} - updates a Promotion record in the database
DELETE /promotions/{id} - deletes a Promotion record in the database
"""

from flask import jsonify, request, url_for, make_response, abort
from werkzeug.exceptions import NotFound
from service.models import Promotion
from . import status  # HTTP Status Codes
from . import app  # Import Flask application

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Promotion Demo REST API Service",
            version="1.0",
            paths=url_for("list_promotions", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# LIST ALL promotions
######################################################################
@app.route("/promotions", methods=["GET"])
def list_promotions():
    """Returns all of the promotions"""
    app.logger.info("Request for promotion list")
    promotions = []
    category = request.args.get("category")
    name = request.args.get("name")
    if category:
        promotions = Promotion.find_by_category(category)
    elif name:
        promotions = Promotion.find_by_name(name)
    else:
        promotions = Promotion.all()

    results = [promotion.serialize() for promotion in promotions]
    app.logger.info("Returning %d promotions", len(results))
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# RETRIEVE A promotion
######################################################################
@app.route("/promotions/<int:promotion_id>", methods=["GET"])
def get_promotions(promotion_id):
    """
    Retrieve a single Promotion

    This endpoint will return a Promotion based on it's id
    """
    app.logger.info("Request for promotion with id: %s", promotion_id)
    promotion = Promotion.find(promotion_id)
    if not promotion:
        raise NotFound("Promotion with id '{}' was not found.".format(promotion_id))

    app.logger.info("Returning promotion: %s", promotion.name)
    return make_response(jsonify(promotion.serialize()), status.HTTP_200_OK)


######################################################################
# ADD A NEW promotion
######################################################################
@app.route("/promotions", methods=["POST"])
def create_promotions():
    """
    Creates a Promotion
    This endpoint will create a Promotion based the data in the body that is posted
    """
    app.logger.info("Request to create a promotion")
    check_content_type("application/json")
    promotion = Promotion()
    promotion.deserialize(request.get_json())
    promotion.create()
    message = promotion.serialize()
    location_url = url_for("get_promotions", promotion_id=promotion.id, _external=True)

    app.logger.info("Promotion with ID [%s] created.", promotion.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


######################################################################
# UPDATE AN EXISTING promotion
######################################################################
@app.route("/promotions/<int:promotion_id>", methods=["PUT"])
def update_promotions(promotion_id):
    """
    Update a Promotions

    This endpoint will update a Promotions based the body that is posted
    """
    app.logger.info("Request to update promotion with id: %s", promotion_id)
    check_content_type("application/json")
    promotion = Promotion.find(promotion_id)
    if not promotion:
        raise NotFound("Promotion with id '{}' was not found.".format(promotion_id))
    promotion.deserialize(request.get_json())
    promotion.id = promotion_id
    promotion.update()

    app.logger.info("Promotion with ID [%s] updated.", promotion.id)
    return make_response(jsonify(promotion.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A promotion
######################################################################
@app.route("/promotions/<int:promotion_id>", methods=["DELETE"])
def delete_promotions(promotion_id):
    """
    Delete a Promotion

    This endpoint will delete a Promotion based the id specified in the path
    """
    app.logger.info("Request to delete promotion with id: %s", promotion_id)
    promotion = Promotion.find(promotion_id)
    if promotion:
        promotion.delete()

    app.logger.info("Promotion with ID [%s] delete complete.", promotion_id)
    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )
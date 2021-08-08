from app.udalocate.models import Location
from app.udalocate.schemas import (
    LocationSchema
)
from app.udalocate.services import LocationService
from flask import request, Response
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaLocate", description="Service to Create and Get Locations")  # noqa


# TODO: This needs better exception handling

#
# @api.before_request
# def before_request():
#     # Set up a Kafka producer
#     TOPIC_NAME = 'locations'
#     KAFKA_SERVER = 'localhost:9092'
#     producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
#     # Setting Kafka to g enables us to use this
#     # in other parts of our application
#     g.topic = TOPIC_NAME
#     g.kafka_producer = producer
#     print(g.kafka_producer)


@api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    def post(self) -> Response:
        request.get_json()
        if LocationService.create(request.get_json()):
            return Response("{'message' : 'accepted'}", status=202, mimetype='application/json')
        else:
            return Response(status=408)

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location

import logging
from typing import Dict

from flask_restful.representations import json
from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError

from app import db
from app.udalocate.models import Location
from app.udalocate.schemas import LocationSchema
from geoalchemy2.functions import ST_AsText, ST_Point



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("location-api")


class LocationService:
    # TOPIC_NAME = 'locations'
    # KAFKA_SERVER = 'localhost:9092'
    # producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def create(location: Dict):
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        db.session.add(new_location)
        db.session.commit()

        return new_location

        # TODO: Uncomment if Kafka Consumer works
        # logger.info('Location Received', location)
        # location_bytes = json.dumps(location).encode()
        # try:
        #     LocationService.producer.send(LocationService.TOPIC_NAME, location_bytes)
        #     LocationService.producer.flush(timeout=60)
        #     return True
        # except Exception as e:
        #     logger.error("Producer Timed Out")
        #     return False




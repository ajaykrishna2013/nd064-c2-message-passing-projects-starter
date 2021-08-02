from app.udalocate.models import Connection, Location, Person  # noqa
from app.udalocate.schemas import LocationSchema  # noqa


def register_routes(api, app, root="api"):
    from app.udalocate.controllers import api as location_api

    api.add_namespace(location_api, path=f"/{root}")

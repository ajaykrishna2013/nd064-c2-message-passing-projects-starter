def register_routes(api, app, root="api"):
    from app.udalocate import register_routes as attach_location_serivce

    # Add routes
    attach_location_serivce(api, app)

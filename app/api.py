"""Flask REST API for the BI migration engine."""

from flask import Flask, jsonify, request

try:
    from flask_cors import CORS
except ModuleNotFoundError:  
    class CORS:  
        def __init__(self, *args, **kwargs):
            pass

from .engine import migrate


def create_app():
    """Create and configure the Flask application."""

    application = Flask(__name__)

    CORS(application)

    @application.route(
        "/api/health",
        methods=["GET"],
    )
    def health():
        """Return the API health status."""

        return jsonify(
            {
                "status": "ok",
                "service": (
                    "Office Soln AI BI Migration Engine"
                ),
            }
        )

    @application.route(
        "/api/migrate",
        methods=["POST"],
    )
    def migration():
        """Run the BI migration engine."""

        data = request.get_json(
            silent=True
        )

        if not data:
            return jsonify(
                {
                    "success": False,
                    "error": (
                        "Request body must contain "
                        "valid JSON data."
                    ),
                }
            ), 400

        required_fields = [
            "calculations",
            "target_calculation",
            "existing_dax",
            "visual",
        ]

        missing_fields = [
            field
            for field in required_fields
            if field not in data
        ]

        if missing_fields:
            return jsonify(
                {
                    "success": False,
                    "error": (
                        "Missing required fields."
                    ),
                    "missing_fields": missing_fields,
                }
            ), 400

        try:
            result = migrate(data)

        except (
            KeyError,
            TypeError,
            ValueError,
        ) as error:
            return jsonify(
                {
                    "success": False,
                    "error": str(error),
                }
            ), 400

        return jsonify(
            {
                "success": True,
                "result": result,
            }
        ), 200

    return application


app = create_app()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )
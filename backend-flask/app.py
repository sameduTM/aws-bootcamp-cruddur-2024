from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import os

from services.home_activities import *
from services.notifications_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *
from services.users_short import *

# Honeycomb ---------
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter

# X-RAY -------------
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# CloudWatch Logs
import watchtower
import logging
from time import strftime

# ROLLBAR
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception

# Flask Cognito Token Verify
from jwt.exceptions import JWTException
from lib.cognito_jwt_token import TokenVerify


"""
# Configuring Logger to Use CloudWatch
LOGGER = logging.getLogger("CloudWatch")
LOGGER.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
cw_handler = watchtower.CloudWatchLogHandler(log_group_name='cruddur')
LOGGER.addHandler(console_handler)
LOGGER.addHandler(cw_handler)
"""

# Honeycomb ----------
# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)


# Show this in the logs within the backedd-flask app STDOUT
simple_processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(simple_processor)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = Flask(__name__)


# Ensure your SECRET_KEY is bytes for the Fernet encryption used by this lib
# app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")


frontend = os.getenv("FRONTEND_URL")
backend = os.getenv("BACKEND_URL")
origins = [frontend, backend]

cors = CORS(
    app,
    resources={r"/api/*": {"origins": origins}},
    allow_headers=["Content-Type", "Authorization", "Accept"],
    methods=["OPTIONS", "GET", "HEAD", "POST"],
    supports_credentials=True,
)

# Rollbar:- real-time error tracking & debugging tool
rollbar_access_token = os.getenv("ROLLBAR_ACCESS_TOKEN")
with app.app_context():
    rollbar.init(rollbar_access_token, environment="production")
    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)


# X-RAY -------------
xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service="backend-flask", dynamic_naming=xray_url)
XRayMiddleware(app, xray_recorder)

# Initialize automatic instrumentation with Flask
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()


@app.route('/api/health-check')
def health_check():
    return {'success': True}, 200


"""@app.route("/rollbar/test")
def rollbar_test():
    rollbar.report_message("Hello World!", "warning")
    return "Hello World!"""


@app.route("/api/message_groups", methods=["GET"])
def data_message_groups():
    access_token = request.headers.get("Authorization")
    try:
        claims = TokenVerify.cognito_jwt_verify(access_token)
        app.logger.debug("authenticated")
        app.logger.debug(claims)

        cognito_user_id = claims.get("sub")
        model = MessageGroups.run(cognito_user_id=cognito_user_id)
        if model["errors"] is not None:
            return model["errors"], 422
        else:
            return model["data"], 200
    except Exception as e:
        app.logger.debug("un-authenticated:", e)
        return {}, 401


@app.route("/api/messages/<string:message_group_uuid>", methods=["GET"])
def data_messages(message_group_uuid):
    access_token = request.headers.get("Authorization")
    try:
        claims = TokenVerify.cognito_jwt_verify(access_token)
        app.logger.debug("authenticated")
        app.logger.debug(claims)

        cognito_user_id = claims.get("sub")
        model = Messages.run(
            cognito_user_id=cognito_user_id, message_group_uuid=message_group_uuid
        )
        if model["errors"] is not None:
            return model["errors"], 422
        else:
            return model["data"], 200

    except JWTException as e:
        app.logger.debug("un-authenticated")
        app.logger.debug(e)
        return {}, 401


@app.route("/api/messages", methods=["POST", "OPTIONS"])
@cross_origin()
def data_create_message():
    message = request.json.get("message")
    access_token = request.headers.get("Authorization")
    try:
        claims = TokenVerify.cognito_jwt_verify(access_token)
        app.logger.debug("authenticated")

        cognito_user_id = claims.get("sub")
        message_group_uuid = request.json.get("message_group_uuid", None)
        user_receiver_handle = request.json.get("user_receiver_handle", None)
        print("message:", message, "message_group_uuid:",
              message_group_uuid, "user_receiver_handle:", user_receiver_handle)

        if message_group_uuid == None:
            # create for the first time
            model = CreateMessage.run(
                mode="create",
                message=message,
                cognito_user_id=cognito_user_id,
                user_receiver_handle=user_receiver_handle,
            )
        else:
            model = CreateMessage.run(
                mode="update",
                message=message,
                message_group_uuid=message_group_uuid,
                cognito_user_id=cognito_user_id,
            )
        if model["errors"] is not None:
            return model["errors"], 422
        else:
            return model["data"], 200

    except Exception as e:
        app.logger.debug("un-authenticated")
        return {}, 401


@app.route("/api/activities/home", methods=["GET", "POST"])
def data_home():
    access_token = request.headers.get("Authorization")
    try:
        TokenVerify.cognito_jwt_verify(access_token)
        app.logger.debug("authenticated")
        data = HomeActivities.run()
    except Exception as e:
        app.logger.debug("un-authenticated")
        data = HomeActivities.run()
    print(data)
    return data, 200


@app.route("/api/activities/notifications", methods=["GET"])
def data_notifications():
    data = NotificationsActivities.run()
    return data, 200


@app.route("/api/users/@<string:handle>/short", methods=["GET"])
def data_users_short(handle):
    data = UsersShort.run(handle)
    return data, 200


@app.route("/api/activities/@<string:handle>", methods=["GET"])
def data_handle(handle):
    model = UserActivities.run(handle)
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200


@app.route("/api/activities/search", methods=["GET"])
def data_search():
    term = request.args.get("term")
    model = SearchActivities.run(term)
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200
    return


@app.route("/api/activities", methods=["POST", "OPTIONS"])
@cross_origin()
def data_activities():
    user_handle = request.headers.get("Username")
    message = request.json["message"]
    ttl = request.json["ttl"]
    model = CreateActivity.run(message, user_handle, ttl)
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200
    return


@app.route("/api/activities/<string:activity_uuid>", methods=["GET"])
def data_show_activity(activity_uuid):
    data = ShowActivity.run(activity_uuid=activity_uuid)
    return data, 200


@app.route("/api/activities/<string:activity_uuid>/reply", methods=["POST", "OPTIONS"])
@cross_origin()
def data_activities_reply(activity_uuid):
    user_handle = "andrewbrown"
    message = request.json["message"]
    model = CreateReply.run(message, user_handle, activity_uuid)
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200
    return


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4567)

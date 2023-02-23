from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.metrics import MetricUnit

import db

logger = Logger(service="APP")
tracer = Tracer(service="APP")
metrics = Metrics(namespace="MyApp", service="APP")
app = ApiGatewayResolver()


@app.post("/connect")
@tracer.capture_method
def connect():
    source = app.current_event.json_body['source']
    dest = app.current_event.json_body['dest']
    id = db.log_connect_request('main', source, dest)
    return id

@app.get("/connected/<source>/<dest>")
@tracer.capture_method
def connected(source, dest):
    return db.get_connected('main', source, dest)

@tracer.capture_lambda_handler
@logger.inject_lambda_context(
    correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True
)
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event, context):
    try:
        return app.resolve(event, context)
    except Exception as e:
        logger.exception(e)
        raise

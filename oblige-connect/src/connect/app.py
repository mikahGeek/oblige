from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.metrics import MetricUnit

logger = Logger(service="APP")
tracer = Tracer(service="APP")
metrics = Metrics(namespace="MyApp", service="APP")
app = ApiGatewayResolver()


@app.post("/connect")
@tracer.capture_method
def connect():
    return app.current_event.json_body

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

from fastapi import APIRouter

from apis.api_v1.payment_process_api.api import payment_process_api

v1_routing = APIRouter(prefix="/api/v1", tags=["v1"])
v1_routing.add_api_route(
    "/process-payment",
    endpoint=payment_process_api,
    methods=["POST"],
    tags=["payment-process"],
    status_code=200
)

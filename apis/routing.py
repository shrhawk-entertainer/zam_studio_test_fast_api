from fastapi import Depends

from apis.api_v1.routing import v1_routing
from common.dependencies import basic_auth


def setup_routing(app):
    app.include_router(v1_routing, dependencies=[Depends(basic_auth)])

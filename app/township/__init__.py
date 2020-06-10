from flask import Blueprint

township = Blueprint("township", __name__)

from . import views
from ..models.township import Source
from ..models.township import tm_dict

@township.app_context_processor
def inject_objects():
    return dict(Source=Source)

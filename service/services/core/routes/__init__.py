# pylint: disable=C0413

from services.api import Api

api: Api = Api()

# Import routes here
# from .module import *  # isort:skip
from .region import top_categories_by_region  # isort:skip

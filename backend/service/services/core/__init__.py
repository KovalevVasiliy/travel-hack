from services.app import make_app

app = make_app()

from .routes import api  # pylint: disable=C0413  # isort:skip

app.include_router(api, tags=['api'], prefix='/api')

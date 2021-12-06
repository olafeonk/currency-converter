from aiohttp.web import Application, run_app
from app.api import converted, database


if __name__ == '__main__':
    app = Application()
    app.router.add_get('/convert', converted)
    app.router.add_post('/database', database)
    run_app(app)

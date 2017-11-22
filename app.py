from apistar import Include, Route, hooks, http, types
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
import pymongo


def AcceptOrigin(method: http.Method, response: types.ReturnValue):
    response.headers.append("Access-Control-Allow-Origin", "*")
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS,HEADERS"
    response.headers["Access-Control-Allow-Headers"] = "Authorization"
    response.headers["Access-Control-Expose-Headers"] = "*"
    if method.lower() == "options":
        response.status = 200
    return response


def welcome(name=None):
    if name is None:
        return {'message': 'Welcome to API Star!'}
    return {'message': 'Welcome to API Star, %s!' % name}

settings = {
    "AFTER_REQUEST": [
        hooks.render_response,
        AcceptOrigin,
    ]
}

__mongo = None
def connect_db():
    global __mongo
    if __mongo is None:
        __mongo = pymongo.MongoClient()
    db = __mongo['mck']
    collection = db['yunniao']
    return collection


def show_task(task_id: int):
    collection = connect_db()
    record = collection.find_one({'task_id': task_id}, {"_id": 0})
    return record


routes = [
    Route('/', 'GET', welcome),
    Route('/task', 'GET', show_task),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]

app = App(routes=routes, settings=settings)


if __name__ == '__main__':
    app.main()

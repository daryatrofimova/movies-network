import logging

from sanic import Sanic, response
from sanic.request import Request
from sanic.response import HTTPResponse, redirect
from sanic_cors import CORS

import config
from network.graph import ShortestPath

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

from statsd import StatsClient
api = Sanic(__name__)
CORS(api, automatic_options=True)


@api.listener('before_server_start')
async def init(app, _):
    logging.info("Initializing")
    app.graph = ShortestPath()
    logging.info('Initialization completed')


@api.route('/swagger')
@api.route('/')
def swagger_ui(request: Request):
    return redirect(f'http://petstore.swagger.io/?url=http://{request.host}/spec')


@api.route('/spec')
async def definition(request: Request):
    host = request.headers.get('Host') or 'localhost'
    swagger_path = './swagger.yml'
    with open(swagger_path) as f:
        return HTTPResponse(body=f.read().replace('%host%', host))


@api.route('/bacon', methods=['GET'])
async def bacon(request: Request):
    try:
        bacon_number, shortest_path = await api.graph.shortest_path(target=request.args.get('actor'),
                                                                    source='Kevin Bacon')
        return response.json({'bacon_number': bacon_number,
                              'connection': shortest_path})
    except Exception as error:
        logging.error('Error while processing: %s', error, exc_info=True)
        return HTTPResponse('Error: %s' % error, status=500)


@api.route('/any_actor_connection_number', methods=['GET'])
async def any_actor_connection_number(request: Request):
    try:
        actor_connection_number, shortest_path = await api.graph.shortest_path(
            target=request.args.get('actor'),
            source=request.args.get('actor2'))

        return response.json({'actor_connection_number': actor_connection_number,
                              'connection': shortest_path})
    except Exception as error:
        logging.error('Error while processing: %s', error, exc_info=True)
        return HTTPResponse('Error %s' % error, status=500)


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=config.API_PORT)


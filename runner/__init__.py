from configparser import ConfigParser
from http import HTTPStatus

from internal.adapters.api import API
from internal.adapters.pg_storage import PgStorage
from internal.adapters.uwsgi import UWSGI
from internal.domain.resources_worker import ResourcesWorker


def get_uwsgi_app():

    config = read_config()
    
    app = UWSGI(config['api_prefix'])
    
    storage = PgStorage(
        host=config['db_host'], port=config['db_port'], dbname=config['db_name'], user=config['db_user'], password=config['db_pass']
        )

    handler = ResourcesWorker(storage)
    api = API(handler)
    
    @app.route('OPTIONS', '*')
    def options(request, response):
        response.set_status(HTTPStatus.OK)

    @app.route('POST', '/resource_types')
    def create_type(request, response):
        api.create_type(request, response)

    @app.route('GET', '/resource_types/{id}')
    def get_type(request, response, id):
        api.get_type(request, response, id)

    @app.route('GET', '/resource_types')
    def list_types(request, response):
        api.list_types (request, response)

    @app.route('PUT', '/resource_types/{id}')
    def update_type(request, response, id):
        api.update_type(request, response, id)

    @app.route('DELETE', '/resource_types/{id}')
    def delete_type(request, response, id):
        api.delete_type(request, response, id)

    @app.route('DELETE', '/resource_types')
    def delete_types(request, response):
        api.delete_types(request, response)
        
    @app.route('POST', '/resources')
    def create_resource(request, response):
        api.create_resource(request, response)

    @app.route('GET', '/resources/{id}')
    def get_resource(request, response, id):
        api.get_resource(request, response, id)

    @app.route('GET', '/resources')
    def list_resources(request, response):
        api.list_resources(request, response)

    @app.route('PUT', '/resources/{id}')
    def update_resource(request, response, id):
        api.update_resource(request, response, id)

    @app.route('DELETE', '/resources/{id}')
    def delete_resource(request, response, id):
        api.delete_resource(request, response, id)

    @app.route('DELETE', '/resources')
    def delete_resources(request, response):
        api.delete_resources(request, response)
        
    return app


def read_config() -> dict:

    config = ConfigParser()
    config.read('config.ini')
    
    data = {}
    
    if 'server' not in config.sections():
        raise KeyError("config section server not found")
    
    data['api_prefix'] = config['server'].get('api_prefix')
    
    if 'database' not in config.sections():
        raise KeyError("database section server not found")
    
    db_type = config['database'].get('type', '')
    if db_type != 'pgsql':
        raise NotImplementedError('database type ' + db_type + ' is not supported')
    
    data['db_host'] = config['database'].get('host', '')
    data['db_port'] = str(config['database'].get('port', ''))
    data['db_name'] = config['database'].get('database', '')
    data['db_user'] = config['database'].get('user', '')
    data['db_pass'] = config['database'].get('password', '')
    
    return data

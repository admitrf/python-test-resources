import json
import re

from http import HTTPStatus
from urllib.parse import urlparse

class Request:
    
    method: str = ''
    path: str = ''
    query_params: dict = {}
    body: dict = {}
    
    def __init__(self, environ):

        def separate_param(param: str):
            vals = param.split('=')
            return {
                'key': vals[0],
                'value': vals[1] if len(vals) > 1 else True
                }
            
        res = urlparse(environ['RAW_URI'])
        self.method = environ['REQUEST_METHOD']
        self.path = res.path
        params = list(map(separate_param, res.query.split('&')))
        self.query_params = {}
        for param in params:
            self.query_params[param['key']] = param['value']
        if environ.get('CONTENT_TYPE', '') == 'application/json':
            try:
                request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            except (ValueError):
                request_body_size = 0
            request_body = environ['wsgi.input'].read(request_body_size)
            self.body = json.loads(request_body)


class Response:
    status_code: int = HTTPStatus.OK.value
    status_text: str = HTTPStatus.OK.phrase
    response_body: str = ''
    
    def __call__(self, start_response):
        headers = [
            ('Content-Type','application/json'),
            ('Access-Control-Allow-Origin','*'),
            ('Access-Control-Allow-Methods','POST, GET, OPTIONS, PUT, DELETE'),
            ('Access-Control-Allow-Headers','*'),
            ('Access-Control-Max-Age','86400')
        ]
        start_response(str(self.status_code) + ' ' + self.status_text, headers)
        if len(self.response_body) > 0:
            return iter([bytes(self.response_body, 'utf-8')])
        else:
            return iter([])
    
    def set_status(self, status):
        self.status_code = status.value
        self.status_text = status.phrase


__PARAM_RE__ = re.compile("^(.*)\{([a-z]*)\}$")


class UWSGI:
    
    routes: dict
    api_prefix: str = ''
    api_prefix_len: int = 0
    
    def __init__(self, api_prefix):
        self.routes = {}
        self.api_prefix = api_prefix
        self.api_prefix_len = len(api_prefix)


    def __call__(self, environ, start_response):
        request = Request(environ)
        
        response = self.handle_request(request)
        
        return response(start_response)


    def __remove_api_prefix(self, path):
        if self.api_prefix_len == 0:
            return path
        if path[0:self.api_prefix_len] == self.api_prefix:
            return path[self.api_prefix_len:]
        else:
            return path


    def route(self, method: str, path: str):
        def wrapper(handler):
            if method not in self.routes:
                self.routes[method] = {}
            self.routes[method][path] = handler
            return handler
        
        return wrapper


    def handle_request(self, request):
        response = Response()
        
        handler, kwargs = self.find_handler(request.method, request.path)
        if handler is not None:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)
        
        return response


    def find_page_handler(self, pages, request_path):
        requested_path = self.__remove_api_prefix(request_path)
        for path, handler in pages.items():
            if path == '*':
                return handler, {}
            if path == requested_path:
                return handler, {}
            
            matches = __PARAM_RE__.match(path)
            if matches is not None:
                prefix = matches.group(1)
                prefix_len = len(prefix)
                param_name = matches.group(2)
                if requested_path[0:prefix_len] == prefix:
                    try:
                        param_val = int(requested_path[prefix_len:])
                        return  handler, {param_name: param_val}
                    except Exception as _e:
                        continue
        
        return None, {}


    def find_handler(self, request_method, request_path):
        for method, pages in self.routes.items():
            if request_method != method:
                continue
            
            handler, kwargs = self.find_page_handler(pages, request_path)
            if handler is not None:
                return handler, kwargs
                    
        return None, {}


    def default_response(self, response):
        response.set_status(HTTPStatus.NOT_FOUND)


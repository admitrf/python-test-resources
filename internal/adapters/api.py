import json

from http import HTTPStatus

from internal import constants
from internal.adapters.uwsgi import Request, Response
from internal.models import ResourcesEncoder
from internal.ports.resources_handler import ResourcesHandler

class API():
    
    __handler: ResourcesHandler
    
    def __init__(self, handler: ResourcesHandler) -> None:
        self.__handler = handler


    def create_type(self, request: Request, response: Response):
        raw_name = request.body.get('name', '')
        raw_max_speed = request.body.get('max_speed', '')
        if raw_name == '' or raw_max_speed == '':
            response.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            response.response_body = json.dumps({'result': 'error', 'error': constants.ERR_WRONG_DATA})
            return
            
        data = {'name': raw_name}
        try:
            data['max_speed'] = int(raw_max_speed)
        except Exception as _e:
            response.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            response.response_body = json.dumps({'result': 'error', 'error': constants.ERR_WRONG_DATA})
            return
        
        res, item = self.__handler.create_type(data)
        if res['result'] != constants.OK:
            response.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            response.response_body = json.dumps(res)
        else:
            response.set_status(HTTPStatus.CREATED)
            response.response_body = json.dumps(item, cls=ResourcesEncoder)


    def get_type(self, _request: Request, response: Response, id: int):
        res, item = self.__handler.get_type(id)
        if res['result'] == constants.OK:
            response.set_status(HTTPStatus.OK)
            response.response_body = json.dumps(item, cls=ResourcesEncoder)
        elif res['error'] == constants.ERR_NOT_FOUND:
            response.set_status(HTTPStatus.NOT_FOUND)
            response.response_body = json.dumps(res)
        else:
            response.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            response.response_body = json.dumps(res)


    def list_types(self, _request: Request, response: Response):
        res, items = self.__handler.list_types()
        if res['result'] != constants.OK:
            response.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            response.response_body = json.dumps(res)
        else:
            response.set_status(HTTPStatus.OK)
            response.response_body = json.dumps(items, cls=ResourcesEncoder)


    def update_type(self, request: Request, response: Response, id: int):
        raw_name = request.body.get('name', '')
        raw_max_speed = request.body.get('max_speed', '')
        if raw_name == '' or raw_max_speed == '':
            response.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            response.response_body = json.dumps({'result': 'error', 'error': constants.ERR_WRONG_DATA})
            return
            
        data = {'id': id, 'name': raw_name}
        try:
            data['max_speed'] = int(raw_max_speed)
        except Exception as _e:
            response.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            response.response_body = json.dumps({'result': 'error', 'error': constants.ERR_WRONG_DATA})
            return
        
        res, item = self.__handler.update_type(data)
        if res['result'] == constants.OK:
            response.set_status(HTTPStatus.OK)
            response.response_body = json.dumps(item, cls=ResourcesEncoder)
        elif res['error'] == constants.ERR_NOT_FOUND:
            response.set_status(HTTPStatus.NOT_FOUND)
            response.response_body = json.dumps(res)
        else:
            response.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            response.response_body = json.dumps(res)


    def delete_type(self, _request: Request, response: Response, id: int):
        res, count = self.__handler.delete_types([id])
        if res['result'] != constants.OK:
            response.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            response.response_body = json.dumps(res)
        else:
            response.set_status(HTTPStatus.ACCEPTED)
            response.response_body = json.dumps({'deleted': count})


    def delete_types(self, request: Request, response: Response):
        ids = []
        raw_ids = request.query_params.get('ids', '')
        if raw_ids != '':
            try:
                ids = list(map(lambda x: int(x), raw_ids.split(',')))
            except Exception as _e:
                ids = []
                
        res, count = self.__handler.delete_types(ids)
        if res['result'] != constants.OK:
            response.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            response.response_body = json.dumps(res)
        else:
            response.set_status(HTTPStatus.ACCEPTED)
            response.response_body = json.dumps({'deleted': count})


    def create_resource(self, request: Request, response: Response):
        raw_name = request.body.get('name', '')
        raw_cur_speed = request.body.get('cur_speed', '')
        raw_resource_type = request.body.get('resource_type', '')
        if raw_name == '' or raw_cur_speed == '' or raw_resource_type == '':
            response.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            response.response_body = json.dumps({'result': 'error', 'error': constants.ERR_WRONG_DATA})
            return
            
        data = {'name': raw_name}
        try:
            data['cur_speed'] = int(raw_cur_speed)
            data['resource_type'] = int(raw_resource_type)
        except Exception as _e:
            response.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            response.response_body = json.dumps({'result': 'error', 'error': constants.ERR_WRONG_DATA})
            return
        
        res, item = self.__handler.create_resource(data)
        if res['result'] != constants.OK:
            response.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            response.response_body = json.dumps(res)
        else:
            response.set_status(HTTPStatus.CREATED)
            response.response_body = json.dumps(item, cls=ResourcesEncoder)


    def get_resource(self, _request: Request, response: Response, id: int):
        res, item = self.__handler.get_resource(id)
        if res['result'] == constants.OK:
            response.set_status(HTTPStatus.OK)
            response.response_body = json.dumps(item, cls=ResourcesEncoder)
        elif res['error'] == constants.ERR_NOT_FOUND:
            response.set_status(HTTPStatus.NOT_FOUND)
            response.response_body = json.dumps(res)
        else:
            response.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            response.response_body = json.dumps(res)


    def list_resources(self, request: Request, response: Response):
        resource_type = 0
        raw_resource_type = request.query_params.get('resource_type', '')
        if raw_resource_type != '':
            try:
                resource_type = int(raw_resource_type)
            except Exception as _e:
                resource_type = 0
        res, items = self.__handler.list_resources(resource_type=resource_type)
        if res['result'] != constants.OK:
            response.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            response.response_body = json.dumps(res)
        else:
            response.set_status(HTTPStatus.OK)
            response.response_body = json.dumps(items, cls=ResourcesEncoder)


    def update_resource(self, request: Request, response: Response, id: int):
        raw_name = request.body.get('name', '')
        raw_cur_speed = request.body.get('cur_speed', '')
        raw_resource_type = request.body.get('resource_type', '')
        if raw_name == '' or raw_cur_speed == '' or raw_resource_type == '':
            response.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            response.response_body = json.dumps({'result': 'error', 'error': constants.ERR_WRONG_DATA})
            return
            
        data = {'id': id, 'name': raw_name}
        try:
            data['cur_speed'] = int(raw_cur_speed)
            data['resource_type'] = int(raw_resource_type)
        except Exception as _e:
            response.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            response.response_body = json.dumps({'result': 'error', 'error': constants.ERR_WRONG_DATA})
            return
            
        res, item = self.__handler.update_resource(data)
        if res['result'] == constants.OK:
            response.set_status(HTTPStatus.OK)
            response.response_body = json.dumps(item, cls=ResourcesEncoder)
        elif res['error'] == constants.ERR_NOT_FOUND:
            response.set_status(HTTPStatus.NOT_FOUND)
            response.response_body = json.dumps(res)
        else:
            response.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            response.response_body = json.dumps(res)


    def delete_resource(self, _request: Request, response: Response, id: int):
        res, count = self.__handler.delete_resources([id])
        if res['result'] != constants.OK:
            response.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            response.response_body = json.dumps(res)
        else:
            response.set_status(HTTPStatus.ACCEPTED)
            response.response_body = json.dumps({'deleted': count})


    def delete_resources(self, request: Request, response: Response):
        ids = []
        raw_ids = request.query_params.get('ids', '')
        if raw_ids != '':
            try:
                ids = list(map(lambda x: int(x), raw_ids.split(',')))
            except Exception as _e:
                ids = []
                
        res, count = self.__handler.delete_resources(ids)
        if res['result'] != constants.OK:
            response.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            response.response_body = json.dumps(res)
        else:
            response.set_status(HTTPStatus.ACCEPTED)
            response.response_body = json.dumps({'deleted': count})

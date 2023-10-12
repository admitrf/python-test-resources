from typing import Optional

from internal import constants
from internal.models import Resource, ResourceType
from internal.ports.resources_handler import ResourcesHandler
from internal.ports.storage import Storage


class ResourcesWorker(ResourcesHandler):

    __strg: Storage

    def __init__(self, strg: Storage) -> None:
        self.__strg = strg


    def __result(self, error: str = '') -> dict:
        return {
            'result': constants.ERROR if error != '' else constants.OK,
            'error': error
        }


    def create_type(self, data: dict) -> (dict, Optional[ResourceType]):
        if 'name' not in data or 'max_speed' not in data:
            return self.__result(constants.ERR_WRONG_DATA), None
        
        item = ResourceType(data['name'], data['max_speed'])
        
        success, item = self.__strg.create_type(item)
        if not success:
            return self.__result(constants.ERROR_UNKNOWN), None
        
        return self.__result(), item


    def get_type(self, id: int) -> (dict, Optional[ResourceType]):
        if id <= 0:
            return self.__result(constants.ERR_WRONG_DATA), None
        
        success, items = self.__strg.read_types(id=id)
        if not success:
            return self.__result(constants.ERR_UNKNOWN), []
        
        if len(items) == 0:
            return self.__result(constants.ERR_NOT_FOUND), None
        else:
            return self.__result(), items[0]


    def list_types(self) -> (dict, list[ResourceType]):
        success, items = self.__strg.read_types()
        if not success:
            return self.__result(constants.ERR_UNKNOWN), []
        else:
            return self.__result(), items


    def update_type(self, data: dict) -> (dict, Optional[ResourceType]):
        if 'name' not in data or 'max_speed' not in data or 'id' not in data:
            return self.__result(constants.ERR_WRONG_DATA), None
        
        success, item = self.get_type(data['id'])
        if not success:
            return self.__result(constants.ERR_UNKNOWN), None
        if item is None:
            return self.__result(constants.ERR_NOT_FOUND), None
        
        item.name = data['name']
        item.max_speed = data['max_speed']
        success, item = self.__strg.update_type(item)
        if not success:
            return self.__result(constants.ERR_UNKNOWN), None
        else:
            return self.__result(), item


    def delete_types(self, ids: list[int]) -> (dict, int):
        success, count = self.__strg.delete_types(ids)
        if not success:
            return self.__result(constants.ERR_UNKNOWN), 0
        else:
            return self.__result(), count


    def create_resource(self, data: dict) -> (dict, Optional[Resource]):
        if 'name' not in data or 'cur_speed' not in data or 'resource_type' not in data:
            return self.__result(constants.ERR_WRONG_DATA), None
        
        (success, resource_type) = self.get_type(data['resource_type'])
        if not success:
            return self.__result(constants.ERR_UNKNOWN), None
        if resource_type is None:
            return self.__result(constants.ERR_WRONG_DATA), None
        
        item = Resource(resource_type, data['name'], data['cur_speed'])
        success, item = self.__strg.create_resource(item)
        if not success:
            return self.__result(constants.ERR_UNKNOWN), None
        else:
            return self.__result(), item


    def get_resource(self, id: int) -> (dict, Optional[Resource]):
        res, items = self.list_resources(id=id)
        if res['result'] == 'error':
            return res, items
        if len(items) == 0:
            return self.__result(constants.ERR_NOT_FOUND), None
        else:
            return res, items[0]


    def list_resources(self, id: int = 0, resource_type: int = 0) -> (dict, list[Resource]):
        if resource_type > 0:
            success, type_item = self.get_type(resource_type)
            if not success:
                return self.__result(constants.ERR_UNKNOWN), []
            if type_item is None:
                resource_type = 0
        
        success, items = self.__strg.read_resources(id=id, type_id=resource_type)
        if not success:
            return self.__result(constants.ERR_UNKNOWN), []
        else:
            return self.__result(), items


    def update_resource(self, data: dict) -> (dict, Optional[Resource]):
        if 'resource_type' not in data or 'name' not in data or 'cur_speed' not in data or 'id' not in data:
            return self.__result(constants.ERR_WRONG_DATA), None
        
        success, item = self.get_resource(data['id'])
        if not success:
            return self.__result(constants.ERR_UNKNOWN), None
        if item is None:
            return self.__result(constants.ERR_NOT_FOUND), None
        
        success, resource_type = self.get_type(data['resource_type'])
        if not success:
            return self.__result(constants.ERR_UNKNOWN), None
        if resource_type is None:
            return self.__result(constants.ERR_WRONG_DATA), None
        
        item.resorurce_type = resource_type
        item.name = data['name']
        item.cur_speed = data['cur_speed']
        success, item = self.__strg.update_resource(item)
        if not success:
            return self.__result(constants.ERR_UNKNOWN), None
        else:
            return self.__result(), item


    def delete_resources(self, ids: list[int]) -> (dict, int):
        success, count = self.__strg.delete_resources(ids)
        if not success:
            return self.__result(constants.ERR_UNKNOWN), 0
        else:
            return self.__result(), count

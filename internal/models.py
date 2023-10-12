import json

class ResourceType:

    __id = 0
    name = ''
    max_speed = 0


    def __init__(self, name: str, max_speed: int, id: int = 0) -> None:
        self.__id = id
        self.name = name
        self.max_speed = max_speed


    @property
    def id(self):
        return self.__id


class Resource:

    __id = 0
    name = ''
    cur_speed = 0
    resource_type: ResourceType


    def __init__(self, resource_type: ResourceType, name: str, cur_speed: int, id: int = 0) -> None:
        if resource_type is None:
            raise ValueError("empty resource type is not permitted")
        if not isinstance(resource_type, ResourceType):
            raise ValueError("wrong resource type value")
        self.__id = id
        self.resource_type = resource_type
        self.name = name
        self.cur_speed = cur_speed


    @property
    def id(self):
        return self.__id


    @property
    def speed_excess(self):
        val = 0
        if self.resource_type and self.resource_type.max_speed != 0:
            val = round(self.cur_speed / self.resource_type.max_speed * 100) - 100
        return val


class ResourcesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Resource):
            return {
                'id': obj.id,
                'name': obj.name,
                'cur_speed': obj.cur_speed,
                'resource_type': obj.resource_type,
                'speed_excess': obj.speed_excess
            }
        if isinstance(obj, ResourceType):
            return {
                'id': obj.id,
                'name': obj.name,
                'max_speed': obj.max_speed
            }
        return json.JSONEncoder.default(self, obj)
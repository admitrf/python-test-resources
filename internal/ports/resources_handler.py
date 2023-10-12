from abc import ABC, abstractmethod
from typing import Optional

from internal.models import ResourceType, Resource

class ResourcesHandler(ABC):

    @abstractmethod
    def create_type(self, data: dict) -> (dict, Optional[ResourceType]):
        # 
        pass    

    @abstractmethod
    def get_type(self, id: int) -> (dict, Optional[ResourceType]):
        # 
        pass    

    @abstractmethod
    def list_types(self) -> (dict, list[ResourceType]):
        # 
        pass

    @abstractmethod
    def update_type(self, data: dict) -> (dict, Optional[ResourceType]):
        # 
        pass

    @abstractmethod
    def delete_types(self, ids: list[int]) -> (dict, int):
        # 
        pass

    @abstractmethod
    def create_resource(self, data: dict) -> (dict, Optional[Resource]):
        # 
        pass    
    
    @abstractmethod
    def get_resource(self, id: int) -> (dict, Optional[Resource]):
        # 
        pass    
    
    @abstractmethod
    def list_resources(self, resource_type: int = 0) -> (dict, list[Resource]):
        # 
        pass
    
    @abstractmethod
    def update_resource(self, data: dict) -> (dict, Optional[Resource]):
        # 
        pass
    
    @abstractmethod
    def delete_resources(self, ids: list[int]) -> (dict, int):
        # 
        pass

from abc import ABC, abstractmethod
from typing import Optional

from internal.models import ResourceType, Resource

class Storage(ABC):
    
    @abstractmethod
    def create_type(self, item: ResourceType) -> (bool, Optional[ResourceType]):
        # 
        pass    
    
    @abstractmethod
    def read_types(self, id: int = 0) -> (bool, list[ResourceType]):
        # 
        pass
    
    @abstractmethod
    def update_type(self, item: ResourceType) -> (bool, Optional[ResourceType]):
        # 
        pass    
    
    @abstractmethod
    def delete_types(self, ids: list[int]) -> (bool, int):
        # 
        pass
    
    @abstractmethod
    def create_resource(self, item: Resource) -> (bool, Optional[Resource]):
        # 
        pass
    
    @abstractmethod
    def read_resources(self, ids: list[int] = [], type_id: int = 0) -> (bool, list[Resource]):
        # 
        pass
    
    @abstractmethod
    def update_resource(self, item: Resource) -> (bool, Optional[Resource]):
        # 
        pass
    
    @abstractmethod
    def delete_resources(self, ids: list[int]) -> (bool, int):
        # 
        pass

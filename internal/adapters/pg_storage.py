import psycopg2
import sys

from typing import Optional

from internal import constants
from internal.models import Resource, ResourceType
from internal.ports.storage import Storage


class PgStorage(Storage):
    
    __conn = None
    
    def __init__(self, host: str, port: int, dbname: str, user: str, password: str) -> None:
        self.__conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
        cur = self.__conn.cursor()
        cur.execute('SELECT 1')


    def create_type(self, item: ResourceType) -> (bool, Optional[ResourceType]):
        if item is None:
            print(constants.ERR_RESOURCE_TYPE_IS_EMPTY, sys.stderr)
            return False, None
        if item.id != 0:
            print('resource type is already created', sys.stderr)
            return False, None
        
        try:
            cur = self.__conn.cursor()
            cur.execute('INSERT INTO resource_types (name, max_speed) VALUES (%s, %s) RETURNING id', 
                        (item.name, item.max_speed)
                        )
            [item_id] = cur.fetchone()
            self.__conn.commit()
            cur.close()
        except Exception as e:
            print(e, sys.stderr)
            return False, None
        
        return True, ResourceType(item.name, item.max_speed, item_id)


    def read_types(self, id: int = 0) -> (bool, list[ResourceType]):
        result = []
        conditions = []
        cond_values = []
        
        if id > 0:
            conditions.append("id = %s")
            cond_values.append(id)
        
        query = """
            SELECT id, name, max_speed FROM resource_types
            """
        if len(conditions) > 0:
            query += ' WHERE ' + " AND ".join(str(e) for e in conditions)
        query += ' ORDER BY id'
        
        try:
            cur = self.__conn.cursor()
            cur.execute(query, tuple(cond_values))
            for (item_id, name, max_speed) in cur.fetchall():
                result.append(ResourceType(name, max_speed, item_id))
            self.__conn.commit()
            cur.close()
        except Exception as e:
            print(e, sys.stderr)
            return False, result
        
        return True, result


    def update_type(self, item: ResourceType) -> (bool, Optional[ResourceType]):
        if item is None:
            print(constants.ERR_RESOURCE_TYPE_IS_EMPTY, sys.stderr)
            return False, None
        if item.id == 0:
            print(constants.ERR_RESOURCE_TYPE_IS_UNKNOWN, sys.stderr)
            return False, None
        
        try:
            cur = self.__conn.cursor()
            cur.execute('UPDATE resource_types SET name=%s, max_speed=%s WHERE id=%s', (item.name, item.max_speed, item.id))
            self.__conn.commit()
            cur.close()
        except Exception as e:
            print(e, sys.stderr)
            return False, None
        
        return True, item


    def delete_types(self, ids: list[int]) -> (bool, int):
        count = 0
        if len(ids) == 0:
            return True, count
        
        try:
            cur = self.__conn.cursor()
            cur.execute("""
                        DELETE FROM resource_types
                        WHERE id IN %(ids)s AND id NOT IN (SELECT DISTINCT resource_type FROM resources)
                        RETURNING *
                        """, {'ids': tuple(ids)})
            for _record in cur.fetchall():
                count += 1
            self.__conn.commit()
            cur.close()
        except Exception as e:
            print(e, sys.stderr)
            return False, 0
        
        return True, count


    def create_resource(self, item: Resource) -> (bool, Optional[Resource]):
        if item is None:
            print('resource is empty', sys.stderr)
            return False, None
        if item.id != 0:
            print('resource is already created', sys.stderr)
            return False, None
        if item.resource_type is None:
            print(constants.ERR_RESOURCE_TYPE_IS_EMPTY, sys.stderr)
            return False, None
        if item.resource_type.id == 0:
            print(constants.ERR_RESOURCE_TYPE_IS_UNKNOWN, sys.stderr)
            return False, None
        
        try:
            cur = self.__conn.cursor()
            cur.execute('INSERT INTO resources (name, resource_type, cur_speed) VALUES (%s, %s, %s) RETURNING id', 
                        (item.name, item.resource_type.id, item.cur_speed)
                        )
            [item_id] = cur.fetchone()
            self.__conn.commit()
            cur.close()
        except Exception as e:
            print(e, sys.stderr)
            return False, None
        
        return True, Resource(item.resource_type, item.name, item.cur_speed, item_id)


    def read_resources(self, id: int = 0, type_id: int = 0) -> (bool, list[Resource]):
        result = []
        conditions = []
        cond_values = []
        
        if id > 0:
            conditions.append("r.id = %s")
            cond_values.append(id)
        if type_id > 0:
            conditions.append("r.resource_type = %s")
            cond_values.append(type_id)
        
        query = """
            SELECT r.id, r.name, r.cur_speed, t.id AS type_id, t.name AS type_name, t.max_speed
            FROM resources r
            INNER JOIN resource_types t ON t.id = r.resource_type
            """
        if len(conditions) > 0:
            query += ' WHERE ' + " AND ".join(conditions)
        query += ' ORDER BY r.id'
        
        try:
            cur = self.__conn.cursor()
            cur.execute(query, tuple(cond_values))
            cache = {}
            for (item_id, name, cur_speed, type_id, type_name, max_speed) in cur.fetchall():
                if str(type_id) in cache:
                    resource_type = cache[str(type_id)]
                else:
                    resource_type = ResourceType(type_name, max_speed, type_id)
                    cache[str(type_id)] = resource_type
                result.append(Resource(resource_type, name, cur_speed, item_id))
            self.__conn.commit()
            cur.close()
        except Exception as e:
            print(e, sys.stderr)
            return False, result
        
        return True, result


    def update_resource(self, item: Resource) -> (bool, Optional[Resource]):
        if item is None:
            print('resource is empty', sys.stderr)
            return False, None
        if item.id == 0:
            print('resource is unknown', sys.stderr)
            return False, None
        if item.resource_type is None:
            print(constants.ERR_RESOURCE_TYPE_IS_EMPTY, sys.stderr)
            return False, None
        if item.resource_type.id == 0:
            print(constants.ERR_RESOURCE_TYPE_IS_UNKNOWN, sys.stderr)
            return False, None
        
        try:
            cur = self.__conn.cursor()
            cur.execute('UPDATE resources SET name=%s, resource_type=%s, cur_speed=%s WHERE id=%s', 
                        (item.name, item.resource_type.id, item.cur_speed, item.id)
                        )
            self.__conn.commit()
            cur.close()
        except Exception as e:
            print(e, sys.stderr)
            return False, None
        
        return True, item


    def delete_resources(self, ids: list[int]) -> (bool, int):
        count = 0
        if len(ids) == 0:
            return True, count
        
        try:
            cur = self.__conn.cursor()
            cur.execute('DELETE FROM resources WHERE id IN %(ids)s RETURNING *', {'ids': tuple(ids)})
            for _record in cur.fetchall():
                count += 1
            self.__conn.commit()
            cur.close()
        except Exception as e:
            print(e, sys.stderr)
            return False, 0
        
        return True, count

from models import Nugu

class Comp():
    MODES = ["exact", "contain", "except"]

    def comp(self, value1, value2, mode: str = "exact") -> bool:
        if type(value1) == type(value2):
            if type(value1) == str:
                return self.comp_str(value1, value2, mode)
            elif type(value1) == int:
                return self.comp_int(value1, value2, mode)
            elif type(value1) == bool:
                return self.comp_bool(value1, value2, mode)
            else:
                return False
        else:
            return False

    def comp_str(self, value1: str, value2: str, mode: str = "exact") -> bool:
        if mode == "exact":
            return self.comp_str_exact(value1, value2)
        elif mode == "contain":
            return self.comp_str_contain(value1, value2)
        elif mode == "except":
            return self.comp_str_except(value1, value2)
        else:
            return False
        
    def comp_int(self, value1: int, value2: int, mode: str = "exact") -> bool:
        if mode == "exact":
            return self.comp_int_exact(value1, value2)
        elif mode == "contain":
            return self.comp_int_contain(value1, value2)
        elif mode == "except":
            return self.comp_int_except(value1, value2)
        else:
            return False
        
    def comp_bool(self, value1: bool, value2: bool, mode: str = "exaxt") -> bool:
        return value1 == value2
    
    def comp_str_exact(self, value1: str, value2: str) -> bool:
        return value1 == value2

    def comp_str_contain(self, value1: str, value2: str) -> bool:
        return (value2 in value1) | (value1 in value2)

    def comp_str_except(self, value1: str, value2: str) -> bool: # 여집합
        return not self.comp_str_contain(value1, value2)

    def comp_int_exact(self, value1: int, value2: int) -> bool:
        return value1 == value2

    def comp_int_contain(self, value1: int, value2: int) -> bool:
        return (str(value2) in str(value1)) | (str(value1) in str(value2))

    def comp_int_except(self, value1: int, value2: int) -> bool: # 여집합
        return not self.comp_int_contain(value1, value2)
    
class Validate():
    PK = Nugu.nickname.__str__().split('.')[-1]

    def __init__(self, PK: str = None):
        self.PK = PK if PK is not None else self.PK

    def duplicate(self, db_list: list, key: str = Nugu.nickname.__str__().split('.')[-1]) -> bool:
        hash_set = set()
        new_db_list = []
        
        for db_nugu in db_list:
            if db_nugu[key] not in hash_set:
                hash_set.add(db_nugu[key])
                new_db_list.append(db_nugu)

        return new_db_list
                
            
        
            
        
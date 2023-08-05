import json
from requests import Session
import pandas as pd
from pydeen.utils import CryptUtil, CryptEngine

class Base:
    """
        Abstract base class
    """

    BASE_PROP_TYPE = "type"
    BASE_PROP_PROP = "properties"
    BASE_PROP_KEY  = "key"
    BASE_PROP_DESCRIPTION = "description" 

    def __init__(self) -> None:
        self.type = "pydeen.Base"
        self._properties = {}
        self.debug = False

    def __repr__(self) -> str:
        return self.type

    def trace(self, msg):
        if self.debug == True:
            print("DEBUG:", msg)

    def info(self, msg):
        if self.debug == True:
            print("INFO:", msg)

    def error(self, msg):
        if self.debug == True:
            print("ERROR:", msg)

    def warning(self, msg):
        if self.debug == True:
            print("WARNING:", msg)

    def get_properties(self):
        return self._properties

    def set_property(self, name, value):
        if value == None or value == "":
            self._properties.pop(name, None)
        else:        
            self._properties[name] = value

    def get_property(self, name, default=None):
        if name in self._properties.keys():
            value = self._properties[name]
            value_type = type(value)
            if value_type == dict:
                engine_key = value[CryptEngine.PROP_ENGINE]
                engine = CryptUtil.get_engine(engine_key)        
                return engine.decode(value) 
            else:
                return value 
        else:
            return default

    def get_type(self) -> str:
        return self.type

    def get_key(self) -> str:
        return self.get_property(Base.BASE_PROP_KEY)

    def get_description(self) -> str:
        return self.get_property(Base.BASE_PROP_DESCRIPTION)

    def set_key(self, desc:str):
        self.set_property(Base.BASE_PROP_DESCRIPTION, desc)    

    def get_config(self):
        return self._properties

    def get_config_file_name(self, filename) -> str:
        if filename.find(".") > 0:
            return filename
        else:
            return filename + "." + self.type + ".cfg"   

    def set_config(self, config):
        self._properties = config    

    def save_config(self, filename) -> bool:
        try:
            config = self.get_config()
            if config == None:
                return False

            with open(self.get_config_file_name(filename), "w") as file:
                file.write(json.dumps(config))
            return True         
        except Exception as exc:
            self.error(f"Error while saving config: {type(exc)} - {exc}")
            return False
        

    def load_config(self, filename) -> bool:    
        try:    
            json_string = ""
            with open(self.get_config_file_name(filename),"r") as file:
                for line in file:
                    if json_string == "":
                        json_string = line
                    else:    
                        json_string += "\n" + line
            
            json_obj = json.loads(json_string)
            return self.set_config(json_obj)
        except Exception as exc:
            self.error(f"Error while loading config: {type(exc)} - {exc}")
            return False


    def menu(self):
        print("This object has no menu")    

class Auth(Base):
    """
        abstract authentification
    """

    AUTH_TYPE_NONE  = "None"
    AUTH_TYPE_BASIC = "Basic"

    AUTH_PROP_TYPE = "type"
    AUTH_PROP_USER = "user"
    AUTH_PROP_PASS = "password"


    def __init__(self) -> None:
        Base.__init__(self)
        self.type = "pydeen.Auth"

    def get_config(self):
        return self._properties

    def init_from_config(self, type, config:dict) -> bool:
        # have to be redefined
        self._properties = {}
        return False

    def set_config(self, config:dict) -> bool:
        
        self._properties = {}
        if Auth.AUTH_PROP_TYPE in config.keys():
            type = config[Auth.AUTH_PROP_TYPE]
        else:
            type = Auth.AUTH_TYPE_NONE     
        
        return self.init_from_config(type, config)

    def get_auth_type(self) -> str:
        type = self.get_property(Auth.AUTH_PROP_TYPE)
        if type == None:
            type = Auth.AUTH_TYPE_NONE

    def get_auth_headers(self) -> dict:
        return None      

    def get_auth_for_request(self):
        return None

    def get_auth_for_requests_session(self) -> Session:
        return None


class Backend(Base):
    """
        abstract enterprise backend with properties
    """
    # static constants
    BACKEND_PROP_NAME       = "name"
    BACKEND_PROP_AUTH       = "auth"
    BACKEND_PROP_HOST       = "host"
    BACKEND_PROP_PROTOCOL   = "protocol"
    BACKEND_PROP_TENANT     = "tenant"
    BACKEND_PROP_PORT       = "port"
    BACKEND_PROP_PATH       = "path"
    BACKEND_PROP_URL        = "url"
    BACKEND_PROP_LANGUAGE   = "language"


    def __init__(self, name, auth:Auth=None) -> None:
        Base.__init__(self)
        self.name = name
        self.type = "pydeen.Backend"
        self.params = {}

        if auth == None:
            self._auth = Auth()
        else:
            self._auth = auth

    def get_name(self):
        return self.name
        
    def set_auth_info(self, auth:Auth):
        self._auth = auth

    def set_auth_basic(self, user, password):
        self._auth = Auth()
        self._auth.set_basic_auth(user, password)

    def get_auth_info(self) -> Auth:
        return self._auth

    def get_params(self):
        return self.params

    def is_auth_info_available(self) -> bool:
        """
            checks if an authorization information is given
        """
        if self._auth == None or self._auth.get_auth_type() == Auth.AUTH_TYPE_NONE:
            return False
        else:
            return True    

    def get_auth_for_request(self):
        return None    

    def set_connection(self, host, port="", protocol="", tenant="", path="", language=""):
        self.set_property(Backend.BACKEND_PROP_HOST, host)
        self.set_property(Backend.BACKEND_PROP_PORT, port)
        self.set_property(Backend.BACKEND_PROP_PROTOCOL, protocol)
        self.set_property(Backend.BACKEND_PROP_TENANT, tenant)
        self.set_property(Backend.BACKEND_PROP_PATH, path)
        self.set_property(Backend.BACKEND_PROP_LANGUAGE, language)

    def get_config(self):
        json_obj = {}
        json_obj[Backend.BASE_PROP_TYPE] = self.type
        json_obj[Backend.BASE_PROP_PROP] = self._properties
        json_obj[Backend.BACKEND_PROP_NAME] = self.name
        json_obj[Backend.BACKEND_PROP_AUTH] = self._auth.get_config()
        return json_obj

    def set_config(self, config) -> bool:

        # set main fields
        self.name = config[Backend.BACKEND_PROP_NAME]
        self.type = config[Backend.BASE_PROP_TYPE]
        self._properties = config[Backend.BASE_PROP_PROP]

        # check auth info
        self._auth = Auth()
        auth_config = config[Backend.BACKEND_PROP_AUTH]
        #print("Read AuthConfig", auth_config)
        if self._auth.set_config(auth_config) == False:
            print("no auth information available for backend")

        # result
        return True
        
class Connector(Base):
    """
        abstract connector to an backend system
    """
    def __init__(self, backend) -> None:
        Base.__init__(self)
        self.type = "pydeen.Connector"
        self.backend = backend
        self.params = {}

    def __repr__(self) ->str:
        return f"{self.type} to {self.backend}"

    def get_backend(self) -> Backend:
        return self.backend

class EntityMetaInfo(Base):
    def __init__(self) -> None:
        super().__init__()
        self.type = "EntityMetaInfo"

    def get_columns(self) -> list:
        return None
class Result(Base):

    def __init__(self, result) -> None:
        super().__init__()
        self.result = result    
        self.type = "pydeen.Result"
        self.columns = None
        self.entityMetaInfo:EntityMetaInfo=None

    def set_entity_metainfo(self, metainfo):
        self.entityMetaInfo = metainfo

    def get_result_raw(self):
        return self.result

    def is_list(self) -> bool:
        if self.result == None:
            return False

        if type(self.result) == "<class 'list'>":
            return True

    def is_list_of_dict(self) -> bool:
        if self.is_list() == False or self.is_empty() == True:
            return False

        if type(self.result[0]) == "<class 'dict'>":
            return True

    def is_empty(self) -> bool:
        if self.result == None:
            return True

        if self.is_list() == True:
            if self.result.len() == 0:
                return True                    
        
        return False

    def get_columns(self) -> list:
        # check metainfo
        result = None
        if self.entityMetaInfo != None:
            result = self.entityMetaInfo.get_columns()

        if result != None:
            return result
        
        # cols from data cached?
        if self.columns != None:
            return self.columns
        
        # check workaround
        if self.is_list_of_dict() == False:
            return None
        else:
            result = []
            for name in self.result[0].keys():
                result.append(name)
        # workaround active
        self.columns = result
        return result             

    def get_count(self) -> int:        
        if self.result == None:
            return 0

        try:
            return len(self.result)
        except:
            print("ERROR COUNT")
            return 0    

    def get_result_as_pandas_df(self, type_mapping:bool=True) -> pd.DataFrame:
        # check result
        if self.is_list_of_dict() == False:
            self.error("invalid result type to convert to pandas dataframe")
            return None
        
        # get result
        raw  = self.get_result_raw()
        cols = self.get_columns()
        if cols == None or len(cols) == 0 or raw == None or len(raw) == 0:
            self.error("invalid result data to convert to pandas dataframe")
            return None

        # prepare pandas
        data = []
        for record in raw:
            entry = []
            for col in cols:
                raw_value = record[col]
                value = self.convert_raw_value(col, raw_value)
                entry.append(value)
            data.append(entry)    

        # create dataframe
        df = pd.DataFrame(data,columns=cols)
        return df

    def convert_raw_value(self, column, value):
        return value   

class Request(Base):

    def __init__(self) -> None:
        super().__init__()
        self.result = None
        self.type = "pydeen.Request"

    def get_result(self) -> Result:
        return self.result



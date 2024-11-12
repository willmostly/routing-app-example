from dataclasses import dataclass
from typing import List, Optional, Set, Dict, cast, Any
import marshmallow_dataclass
from json import dumps


class JsonDataClass:
    @classmethod
    def from_json(cls, json_string: str):
        schema = marshmallow_dataclass.class_schema(cls)()
        return cast(cls, schema.loads(json_string))

    @classmethod
    def from_dict(cls, class_dict: {}):
        schema = marshmallow_dataclass.class_schema(cls)()
        return cast(cls, schema.load(class_dict))


@dataclass
class TrinoQueryProperties(JsonDataClass):
    isQueryParsingSuccessful: bool
    body: str
    queryType: str
    resourceGroupQueryType: Optional[str]
    tables: List[str]
    defaultCatalog: Optional[str]
    defaultSchema: Optional[str]
    catalogs: Set[str]
    schemas: Set[str]
    catalogSchemas: Set[str]
    isNewQuerySubmission: bool
    errorMessage: Optional[str]


@dataclass
class TrinoRequestUser(JsonDataClass):
    user: str
    userInfo: Optional[Dict[str, str]]


@dataclass
class RoutingGroupExternalResponse:
    routingGroup: str
    errors: List[str]

    def to_json(self):
        return dumps(self.__dict__)


@dataclass
class RoutingGroupExternalBody(JsonDataClass):
    trinoQueryProperties: Optional[TrinoQueryProperties]
    trinoRequestUser: Optional[TrinoRequestUser]
    contentType: str
    remoteUser: Optional[str]
    method: str
    requestURI: str
    queryString: Optional[str]
    session: Optional[Dict[str, Any]]  # TODO: make proper jakarta.servlet.http.HttpSession dataclass
    remoteAddr: str
    remoteHost: str
    parameters: Dict[str, str]

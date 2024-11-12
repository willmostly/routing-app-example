from getrouting import TrinoQueryProperties, TrinoRequestUser
from getrouting.views import do_get_routing_group, input_pickles
import json


def test_models():
    trino_query_properties_dict = {
        'body': 'SELECT * from foo.bar.baz',
        'queryType': 'SELECT',
        'resourceGroupQueryType': 'SELECT',
        'tables': ['foo.bar.baz'],
        'catalogs': ['foo'],
        'schemas': ['bar'],
        'catalogSchemas': ['foo.bar'],
        'isNewQuerySubmission': True,
        'isQueryParsingSuccessful': True
    }

    trino_query_properties = TrinoQueryProperties.from_json(json.dumps(trino_query_properties_dict))
    print(trino_query_properties.body)
    print(trino_query_properties.errorMessage)

    trino_query_properties = TrinoQueryProperties.from_dict(trino_query_properties_dict)
    print(trino_query_properties.body)
    print(trino_query_properties.errorMessage)

    userinfo = {
        "sub": "248289761001",
        "name": "Jane Doe",
        "given_name": "Jane",
        "family_name": "Doe",
        "preferred_username": "j.doe",
        "email": "janedoe@example.com",
        "picture": "http://example.com/janedoe/me.jpg"
    }

    trino_request_user_dict = {
        'user': 'jane',
        'userInfo': userinfo
    }

    trino_request_user = TrinoRequestUser.from_dict(trino_request_user_dict)
    print(trino_request_user.user)

    trino_request_user = TrinoRequestUser.from_json(json.dumps(trino_request_user_dict))
    print(trino_request_user.userInfo['sub'])


def test_with_saved_input():
    import pickle
    from werkzeug.datastructures import Headers
    import os.path

    if os.path.isfile(input_pickles['routing_info']) and os.path.isfile(input_pickles['headers']):
        routing_info = pickle.load(open(input_pickles['routing_info'], 'rb'))
        headers = Headers(pickle.load(open(input_pickles['headers'], 'rb')))
        do_get_routing_group(routing_info, headers)


if __name__ == '__main__':
    test_models()
    test_with_saved_input()

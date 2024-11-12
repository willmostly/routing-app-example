from flask import Flask, request, Response
from getrouting import *
from werkzeug.datastructures import Headers

app = Flask(__name__)

save_input_in_debug_mode = True
mimetype = 'application/json'
input_pickles = {
    'routing_info': './test-routing-info.pickle',
    'headers': './headers.pickle'
}


@app.route("/health")
def healthy():
    return "true"


@app.route("/get-routing-group", methods=['POST'])
def get_routing_group():
    routing_info = RoutingGroupExternalBody.from_json(request.get_data(as_text=True))
    return Response(do_get_routing_group(routing_info, request.headers).to_json(), mimetype=mimetype)


@app.route("/debug-routing-info", methods=['POST'])
def debug_routing_info():
    routing_info = RoutingGroupExternalBody.from_json(request.get_data(as_text=True))
    print(f'Deserialized data: {routing_info}')
    print(f'Headers: {request.headers}')
    if save_input_in_debug_mode:
        save_input(routing_info, request.headers)
    routing_group = do_get_routing_group(routing_info, request.headers)
    print(routing_group)
    return Response(routing_group.to_json(), mimetype=mimetype)


def do_get_routing_group(routing_info: RoutingGroupExternalBody, headers: Headers):
    try:
        #  Sample logic
        if (routing_info.trinoRequestUser is not None
                and routing_info.trinoRequestUser.userInfo is not None
                and 'role' in routing_info.trinoRequestUser.userInfo):
            match routing_info.trinoRequestUser.userInfo['role']:
                case 'vp' | 'c-level':
                    return RoutingGroupExternalResponse('vip', [])
                case 'eng':
                    origin_ip = headers.get('X-Forwarded-For')
                    if origin_ip.startswith('192') or origin_ip.startswith('10') or origin_ip.startswith('127'):
                        return RoutingGroupExternalResponse('eng-internal', [])
                    return RoutingGroupExternalResponse('eng', [])

        if (routing_info.trinoQueryProperties is not None and ('tpch' in routing_info.trinoQueryProperties.catalogs
                                                               or 'tpch' in routing_info.trinoQueryProperties.schemas)):
            print()
            return RoutingGroupExternalResponse('benchmarking', [])

        return RoutingGroupExternalResponse('adhoc', [])
    except Exception as e:
        return RoutingGroupExternalResponse('__ERROR__', flatten_exceptions(e.__cause__, []))


def flatten_exceptions(e: BaseException, causes: List, depth: int = 100):
    causes.append(e)
    if e.__cause__ is not None and depth > 0:
        return flatten_exceptions(e.__cause__, causes, depth - 1)
    return causes


def save_input(routing_info: RoutingGroupExternalBody, headers: Headers):
    import pickle
    f = open(input_pickles['routing_info'], 'wb')
    pickle.dump(routing_info, f)
    f.close()
    f = open(input_pickles['headers'], 'wb')
    pickle.dump(list(headers.values()), f)
    f.close()

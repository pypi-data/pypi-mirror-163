import inspect
import json
import signal
from collections import defaultdict
from datetime import datetime
from types import SimpleNamespace

import websockets
#from websockets.protocol import State
import asyncio
import logging
import sys
from os.path import join

from websockets.connection import State

from eme.entities import load_handlers, EntityJSONEncoder

CTRL_ATTRIBUTES = ['server', 'app']


class EmeWebsocketClient(websockets.WebSocketServerProtocol):
    token = None
    user = None
    room_id = None


class RouteNotFoundError(Exception):
    pass


class RouteForbiddenError(Exception):
    pass


class WebsocketApp():
    def __init__(self, config: dict, path='wsapp'):
        if len(config) == 0:
            raise Exception("Empty config file provided")
        conf = config['websocket']
        app_type = conf.get('type')
        sys.path.append(path)

        # Socket
        self.host = conf.get('host', '0.0.0.0')
        self.port = conf.get('port', 3000)
        self.route_sep = '/'

        # Flags
        self.debug = conf.get('debug')

        # ws handlers
        self._endpoints_to_methods = {}
        self._methods = {}

        if app_type == 'wsapp':
            self.load_groups(load_handlers(self, 'Group', path=join(path, 'groups')), conf)

        signal.signal(signal.SIGINT, self.close_sig_handler)

        if conf.get('rooms'):
            self.rooms = defaultdict(set)
        else:
            self.rooms = None

    def close_sig_handler(self, signal, frame):
        self.close()

    async def handle_requests(self, websocket, path):
        self.on_connect(websocket, path)

        try:
            async for message in websocket:
                rws = json.loads(message)

                # get action
                route = rws.pop("route", self.route_sep)
                group, method = route.split(self.route_sep)
                msid = rws.pop('msid', None)

                # check if action is valid
                if route not in self._endpoints_to_methods:
                    if self.debug:
                        print(f"  [{datetime.now()}] {msid} {route} - 404")
                    return  # todo: return with error?

                # @TODO: itt: websocket has no user and token (it's not that class!)
                # @todo:   how to inject token as authenticate?

                # Build request
                method_id = self._endpoints_to_methods[route]
                action, sig = self._methods[method_id]

                params = {}
                if 'msid' in sig: params['msid'] = msid
                if 'user' in sig: params['user'] = websocket.user
                if 'client' in sig: params['client'] = websocket
                if 'token' in sig: params['token'] = websocket.token
                if 'data' in sig: params['data'] = SimpleNamespace(**rws)
                if 'route' in sig: params['route'] = route

                # Execute request & send response
                if self.debug:
                    print(f"  [{datetime.now()}] {msid} {route}")

                try:
                    response = await action(**params)

                    if response is not None:
                        await self.send(response, websocket, route=route, msid=msid)
                except RouteNotFoundError:
                    if self.debug:
                        print(f"  [{datetime.now()}] {msid} {route} - 404")
                except RouteForbiddenError:
                    if self.debug:
                        print(f"  [{datetime.now()}] {msid} {route} - 403")
                except Exception as e:
                    logging.exception("METHOD")

                    if self.debug:
                        raise e
        except websockets.exceptions.ConnectionClosedError:
            self.on_disconnect(websocket, path)

    async def send(self, rws, client, route=None, msid=None):
        if client.state is State.CLOSED:
            return

        if isinstance(rws, dict):
            if route is not None:
                rws['route'] = route

            if msid is not None:
                rws['msid'] = msid

            await client.send(json.dumps(rws, cls=EntityJSONEncoder))
        elif isinstance(rws, str):
            await client.send(rws)
        elif isinstance(rws, list):
            for rw_ in rws:
                await self.send(rw_, client, route=route)
        else:
            raise Exception("Unsupported message type: {}".format(type(rws)))

    async def send_to_room(self, rws, room_id=None, client=None):
        if room_id is None and client is not None:
            room_id = client.room_id
        elif self.rooms is None:
            raise Exception("send_to_room was called but rooms are not configured in this app")

        room_client: EmeWebsocketClient
        for room_client in self.rooms[room_id]:
            if room_client.state == State.OPEN:
                await self.send(rws, room_client)

    async def send_broadcast(self, rws):
        for room_id in self.rooms:
            await self.send_to_room(rws, room_id)

    def start(self):
        print("Websocket: listening on {}:{}".format(self.host, self.port))

        asyncio.get_event_loop().run_until_complete(websockets.serve(self.handle_requests, self.host, self.port, klass=EmeWebsocketClient))
        asyncio.get_event_loop().run_forever()

    def close(self):
        print("Exited websocket server")
        sys.exit()

    def init_modules(self, modules, webconf):
        for module in modules:
            module.init_dal()

            if hasattr(module, 'init_wsapp'):
                module.init_wsapp(self, webconf)

    def preset_endpoint(self, route_key, endpoint):
        # strip the verb from the url
        sp = route_key.split(' ')
        prefix = 'WS' if len(sp) == 1 else sp[0].upper()
        route_key = ''.join(sp[1:])

        # force the GET keyword into the endpoint
        controller, method = endpoint.split(':')
        if prefix == 'WS' and method[0:2].lower() != 'ws':
            method = prefix.lower() + '_' + method

        # custom routes are a map of {Controller.verb_method -> overridden_url}
        endpoint = controller + self.route_sep + method
        self._endpoints_to_methods[route_key] = endpoint

    def preset_endpoints(self, rules):
        for route_key, endpoint in rules.items():
            self.preset_endpoint(route_key, endpoint)

    def load_groups(self, groups, conf):
        if not groups: return
        # Similar to WebApp's load_controllers
        debug_len = conf.get('__debug_len__', 20)

        # todo: later: override by presets (like in webapp)
        print(('\n{0: <' + str(debug_len) + '}{1}').format('ROUTE', 'ENDPOINT'))

        covered_methods = set(self._endpoints_to_methods.values())

        for group_name, group in groups.items():
            for method_name in dir(group):
                if method_name.startswith("_") or method_name in CTRL_ATTRIBUTES:
                    continue
                method = getattr(group, method_name)
                if not callable(method):
                    continue

                if not hasattr(group, 'group'):
                    group.group = group_name
                if not hasattr(group, 'route'):
                    group.route = group.group.lower()

                method_id = f'{group_name}:{method_name}'

                # discover signature - what the function requires
                sig = list(inspect.signature(method).parameters.keys())
                self._methods[method_id] = (method, sig)

                if method_id not in covered_methods:
                    # if custom URL(=routekey) mapping hasn't been found, generate a route
                    route = f'{group.route}{self.route_sep}{method_name}'
                    self._endpoints_to_methods[route] = method_id
                else:
                    route = list(self._endpoints_to_methods.keys())[list(self._endpoints_to_methods.values()).index(method_id)]
                print(('{0: <' + str(debug_len) + '}{1}').format(route, method_name))

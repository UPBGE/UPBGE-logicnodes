from bge import logic, constraints
from mathutils import Euler
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.nodes import STATUS_WAITING
from uplogic.nodes import debug
from uplogic.nodes import is_waiting
from uplogic.nodes import not_met
import json


class ULLoadGame(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.slot = None
        self.path = ''
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def get_game_vec(self, data):
        return Euler((data['x'], data['y'], data['z']))

    def get_custom_path(self, path):
        if not path.endswith('/') and not path.endswith('json'):
            path = path + '/'
        return path

    def evaluate(self):
        self.done = STATUS_WAITING
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        self._set_ready()
        slot = self.get_socket_value(self.slot)
        if is_waiting(slot):
            return
        cust_path = self.get_custom_path(self.path)

        path = (
            logic.expandPath('//Saves/') if self.path == ''
            else cust_path
        )

        scene = logic.getCurrentScene()

        try:
            with open(path + 'save' + str(slot) + '.json') as json_file:
                data = json.load(json_file)
                # for obj in scene.objects:
                #     if obj.name not in data['objects']:
                #         obj.endObject()
                for obj in data['objects']:
                    if obj['name'] in scene.objects:
                        game_obj = scene.objects[obj['name']]
                    else:
                        debug(
                            'Could not load Object {}: Not in active Scene!'
                            .format(obj['name'])
                        )
                        continue

                    wPos = self.get_game_vec(obj['data']['worldPosition'])
                    wOri = self.get_game_vec(obj['data']['worldOrientation'])
                    wSca = self.get_game_vec(obj['data']['worldScale'])

                    game_obj.worldPosition = wPos
                    game_obj.worldOrientation = wOri.to_matrix()
                    game_obj.worldScale = wSca

                    if obj['type'] == 'dynamic':
                        linVel = self.get_game_vec(
                            obj['data']['worldLinearVelocity']
                        )
                        angVel = self.get_game_vec(
                            obj['data']['worldAngularVelocity']
                        )
                        game_obj.worldLinearVelocity = linVel
                        game_obj.worldAngularVelocity = angVel

                    if obj['type'] == 'light':
                        energy = obj['data']['energy']
                        game_obj.energy = energy

                    if obj['type'] == 'character':
                        wDir = self.get_game_vec(obj['data']['walkDirection'])
                        (
                            constraints
                            .getCharacter(game_obj)
                            .walkDirection
                        ) = wDir

                    for prop in obj['data']['props']:
                        game_obj[prop['name']] = prop['value']
        except Exception:
            debug(
                'Load Game Node: Could Not Find Saved Game on Slot {}!'
                .format(slot)
            )

        self.done = True

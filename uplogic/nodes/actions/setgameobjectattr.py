from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import not_met
from uplogic.utils import debug


class ULSetGameObjectAttribue(ULActionNode):
    def __init__(self, value_type='worldPosition'):
        ULActionNode.__init__(self)
        self.value_type = str(value_type)
        self.condition = None
        self.xyz = None
        self.game_object = None
        self.attribute_value = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        xyz = self.get_input(self.xyz)
        game_object = self.get_input(self.game_object)
        attribute = self.get_input(self.value_type)
        value = self.get_input(self.attribute_value)
        if is_waiting(xyz, game_object, attribute, value):
            return

        if hasattr(value, attribute):
            value = getattr(value, attribute).copy()
        self._set_ready()
        if not hasattr(game_object, attribute):
            debug(
                'Set Object Data Node: {} has no attribute {}!'
                .format(game_object, attribute)
            )
            return
        data = getattr(game_object, attribute)
        if 'Orientation' in attribute:
            data = data.to_euler()
        for axis in xyz:
            if not xyz[axis]:
                setattr(value, axis, getattr(data, axis))
        setattr(
            game_object,
            attribute,
            value
        )
        if value == 'worldScale':
            game_object.reinstancePhysicsMesh(
                game_object,
                game_object.meshes[0]
            )
        self.done = True

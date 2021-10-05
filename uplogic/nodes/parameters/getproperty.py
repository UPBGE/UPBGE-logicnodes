from uplogic.nodes import ULOutSocket, ULParameterNode
from uplogic.utils import STATUS_WAITING, is_invalid


class ULGetProperty(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.game_object = None
        self.property_name = None
        self.OUT = ULOutSocket(self, self.get_property)

    def get_property(self):
        game_object = self.get_socket_value(self.game_object)
        property_name = self.get_socket_value(self.property_name)
        if is_invalid(game_object, property_name):
            return STATUS_WAITING
        if property_name in game_object:
            return game_object[property_name]
        game_object[property_name] = None

    def evaluate(self):
        self._set_ready()

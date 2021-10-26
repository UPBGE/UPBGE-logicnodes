from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting


class ULActionStatus(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.game_object = None
        self.action_layer = None
        self._action_name = None
        self._action_frame = None
        self.NOT_PLAYING = ULOutSocket(self, self.get_not_playing)
        self.ACTION_NAME = ULOutSocket(self, self.get_action_name)
        self.ACTION_FRAME = ULOutSocket(self, self.get_action_frame)

    def get_action_name(self):
        return self._action_name

    def get_action_frame(self):
        return self._action_frame

    def get_not_playing(self):
        return not self.get_value()

    def evaluate(self):
        game_object = self.get_socket_value(self.game_object)
        action_layer = self.get_socket_value(self.action_layer)
        if is_waiting(game_object, action_layer):
            return
        self._set_ready()
        if is_invalid(game_object):
            self._action_name = STATUS_WAITING
            self._action_frame = STATUS_WAITING
            self._set_value(False)
        else:
            self._set_value(game_object.isPlayingAction(action_layer))
            self._action_name = game_object.getActionName(action_layer)
            self._action_frame = game_object.getActionFrame(action_layer)

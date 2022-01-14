from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting
from uplogic.utils import not_met
import bpy


class ULSetActionFrame(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.action_layer = None
        self.action_frame = None
        self.freeze = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        game_object = self.get_input(self.game_object)
        action_layer = self.get_input(self.action_layer)
        action_frame = self.get_input(self.action_frame)
        freeze = self.get_input(self.freeze)
        action_name = self.get_input(self.action_name)
        layer_weight = self.get_input(self.layer_weight)
        self._set_ready()
        if is_waiting(
            action_layer,
            action_frame,
            layer_weight
        ):
            return
        if is_invalid(
            game_object,
        ):
            return
        is_playing = game_object.isPlayingAction(action_layer)
        same_action = game_object.getActionName(action_layer) == action_name
        action = bpy.data.actions[action_name]
        start_frame = action.frame_range[0]
        end_frame = action.frame_range[1]
        finished = game_object.getActionFrame(action_layer) >= end_frame
        if not (is_playing or same_action) or finished:
            game_object.stopAction(action_layer)
            speed = .000000000000000001 if freeze else 1
            game_object.playAction(
                action_name,
                start_frame,
                end_frame,
                action_layer,
                layer_weight=1-layer_weight,
                speed=speed
            )
        game_object.setActionFrame(action_frame, action_layer)
        self.done = True

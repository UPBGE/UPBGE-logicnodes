from bge import logic
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULPlayAction(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.action_name = None
        self.stop_anim = None
        self.frames = None
        self.start_frame = None
        self.end_frame = None
        self.layer = None
        self.priority = None
        self.play_mode = None
        self.layer_weight = None
        self.old_layer_weight = None
        self.speed = None
        self.old_speed = None
        self.blendin = None
        self.blend_mode = None
        self._started = False
        self._running = False
        self._finished = False
        self._frame = 0.0
        self._finish_notified = False
        self.STARTED = ULOutSocket(self, self._get_started)
        self.FINISHED = ULOutSocket(self, self._get_finished)
        self.RUNNING = ULOutSocket(self, self._get_running)
        self.FRAME = ULOutSocket(self, self._get_frame)

    def _get_started(self):
        return self._started

    def _get_finished(self):
        return self._finished

    def _get_running(self):
        return self._running

    def _get_frame(self):
        return self._frame

    def _reset_subvalues(self):
        self._started = False
        self._finished = False
        self._running = False
        self._frame = 0.0
        self._finish_notified = False

    def _notify_finished(self, obj, layer):
        if not self._finish_notified and self.stop_anim:
            self._finish_notified = True
            self._finished = True
            obj.stopAction(layer)
        else:
            self._finished = False

    def evaluate(self):
        condition = self.get_input(self.condition)
        game_object = self.get_input(self.game_object)
        action_name = self.get_input(self.action_name)
        start_frame = self.get_input(self.start_frame)
        end_frame = self.get_input(self.end_frame)
        layer = self.get_input(self.layer)
        priority = self.get_input(self.priority)
        play_mode = self.get_input(self.play_mode)
        layer_weight = self.get_input(self.layer_weight)
        speed = self.get_input(self.speed)
        blendin = self.get_input(self.blendin)
        blend_mode = self.get_input(self.blend_mode)
        if is_invalid(
            game_object,
            action_name,
            start_frame,
            end_frame,
            layer,
            priority,
            play_mode,
            layer_weight,
            speed,
            blendin,
            blend_mode
        ):
            return
        if play_mode > 2:
            if not_met(condition):
                self._notify_finished(game_object, layer)
                return
            else:
                play_mode -= 3
        if layer_weight <= 0:
            layer_weight = 0.0
        elif layer_weight >= 1:
            layer_weight = 1.0
        if speed <= 0:
            speed = 0.01
        self._set_ready()
        if is_invalid(game_object):  # can't play
            self._reset_subvalues()
        else:
            # Condition might be false and the animation running
            # because it was started in a previous evaluation
            playing_action = game_object.getActionName(layer)
            playing_frame = game_object.getActionFrame(layer)
            min_frame = start_frame
            max_frame = end_frame
            if end_frame < start_frame:
                min_frame = end_frame
                max_frame = max_frame
            if (
                (playing_action == action_name) and
                (playing_frame >= min_frame) and
                (playing_frame <= max_frame)
            ):
                self._started = False
                self._running = True
                is_near_end = False
                self._frame = playing_frame
                if (
                    layer_weight != self.old_layer_weight or
                    speed != self.old_speed
                ):
                    reset_frame = (
                        start_frame
                        if play_mode == logic.KX_ACTION_MODE_LOOP else
                        end_frame
                    )
                    next_frame = (
                        playing_frame + speed
                        if
                        playing_frame + speed <= end_frame
                        else
                        reset_frame
                    )
                    game_object.stopAction(layer)
                    game_object.playAction(
                        action_name,
                        start_frame,
                        end_frame,
                        layer=layer,
                        priority=priority,
                        blendin=blendin,
                        play_mode=play_mode,
                        speed=speed,
                        layer_weight=1 - layer_weight,
                        blend_mode=blend_mode)
                    game_object.setActionFrame(next_frame, layer)
                # TODO: the meaning of start-end depends
                # also on the action mode
                if end_frame > start_frame:  # play 0 to 100
                    is_near_end = (playing_frame >= (end_frame - 0.5))
                else:  # play 100 to 0
                    is_near_end = (playing_frame <= (end_frame + 0.5))
                if is_near_end:
                    self._notify_finished(game_object, layer)
            elif condition:  # start the animation if the condition is True
                is_playing = game_object.isPlayingAction(layer)
                same_action = game_object.getActionName(layer) == action_name
                if not same_action and is_playing:
                    game_object.stopAction(layer)
                if not (is_playing or same_action):
                    game_object.playAction(
                        action_name,
                        start_frame,
                        end_frame,
                        layer=layer,
                        priority=priority,
                        blendin=blendin,
                        play_mode=play_mode,
                        speed=speed,
                        layer_weight=1-layer_weight,
                        blend_mode=blend_mode)
                    self._started = True
                    self._frame = start_frame
                self._running = True
                self._finished = False
                self._finish_notified = False
            else:  # game_object is existing and valid but condition is False
                self._reset_subvalues()
        self.old_layer_weight = layer_weight
        self.old_speed = speed

from bge import logic
from random import randint, random
from bge.types import KX_GameObject as GameObject
from uplogic.animation import ULActionSystem
from uplogic.data import GlobalDB


PLAY_MODES = {
    'play': logic.KX_ACTION_MODE_PLAY,
    'pingpong': logic.KX_ACTION_MODE_PING_PONG,
    'loop': logic.KX_ACTION_MODE_LOOP
}


BLEND_MODES = {
    'blend': logic.KX_ACTION_BLEND_BLEND,
    'add': logic.KX_ACTION_BLEND_ADD
}


class ULAction():
    '''TODO: Documentation
    '''
    game_object = None
    act_system = 'default'
    acion_name: str
    start_frame: int
    end_frame: int
    layer: int
    priority: int
    blendin: float
    play_mode: str
    blend_mode: int
    speed: float
    old_speed: float = 0
    layer_weight: float
    old_layer_weight: float = 0
    frame: float = 0

    def __init__(
        self,
        game_object: GameObject,
        action_name: str,
        start_frame: int = 0,
        end_frame: int = 250,
        layer: int = -1,
        priority: int = 0,
        blendin: float = 0,
        play_mode: str = 'play',
        speed: float = 1,
        layer_weight: float = 1,
        blend_mode: str = 'blend',
    ):
        self.act_system = self.get_act_sys(self.act_system)
        self.layer = layer
        self.game_object = game_object
        if self.layer == -1:
            ULActionSystem.find_free_layer(self)
        elif ULActionSystem.check_layer(self):
            return
        layer = self.layer
        self.acion_name = action_name
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.priority = priority
        self.blendin = blendin
        self.play_mode = play_mode
        self.blend_mode = blend_mode
        self.speed = speed
        self.layer_weight = layer_weight
        is_playing = game_object.isPlayingAction(layer)
        same_action = game_object.getActionName(layer) == action_name
        if not same_action and is_playing:
            game_object.stopAction(layer)
        if not (is_playing or same_action):
            game_object.playAction(
                action_name,
                start_frame,
                end_frame,
                play_mode=PLAY_MODES[play_mode],
                speed=speed,
                layer=layer,
                priority=priority,
                blendin=blendin,
                layer_weight=1-layer_weight,
                blend_mode=BLEND_MODES[blend_mode])
            self._started = True
            self._frame = start_frame
        self.act_system.add(self)

    def update(self):
        layer_weight = self.layer_weight
        speed = self.speed
        if layer_weight <= 0:
            layer_weight = 0.0
        elif layer_weight >= 1:
            layer_weight = 1.0
        if speed <= 0:
            speed = 0.01
        game_object = self.game_object
        layer = self.layer
        start_frame = self.start_frame
        end_frame = self.end_frame
        action_name = self.acion_name
        play_mode = self.play_mode
        priority = self.priority
        blendin = self.blendin
        blend_mode = self.blend_mode
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
            self._frame = playing_frame
            if (
                layer_weight != self.old_layer_weight or
                speed != self.old_speed
            ):
                reset_frame = (
                    start_frame if
                    play_mode == logic.KX_ACTION_MODE_LOOP else
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
                    play_mode=PLAY_MODES[play_mode],
                    speed=speed,
                    layer_weight=1 - layer_weight,
                    blend_mode=BLEND_MODES[blend_mode]
                )
                game_object.setActionFrame(next_frame, layer)
            if play_mode == 'play':
                if end_frame > start_frame:  # play 0 to 100
                    is_near_end = (playing_frame >= (end_frame - 0.5))
                else:  # play 100 to 0
                    is_near_end = (playing_frame <= (end_frame + 0.5))
                if is_near_end:
                    self.act_system.remove(self)
        self.frame = game_object.getActionFrame(layer)
        self.old_layer_weight = layer_weight
        self.old_speed = speed

    def stop(self):
        self.game_object.stopAction(self.layer)

    def randomize_frame(self, min=None, max=None):
        if min is None:
            min = self.start_frame
        if max is None:
            max = self.end_frame
        frame = randint(min, max)
        self.frame = frame
        self.game_object.setActionFrame(
            frame,
            self.layer
        )

    def randomize_speed(self, min=.9, max=1.1):
        delta = max - min
        self.speed = min + (delta * random())

    def set_frame(self, frame):
        self.frame = frame
        self.game_object.setActionFrame(
            frame,
            self.layer
        )

    def get_act_sys(self, name: str):
        act_systems = GlobalDB.retrieve('uplogic.animation')
        if act_systems.check(name):
            return act_systems.get(name)
        else:
            return ULActionSystem(name)

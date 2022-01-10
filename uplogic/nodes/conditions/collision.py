from bge.types import KX_GameObject
from uplogic.nodes import ULConditionNode
from uplogic.nodes import ULLogicContainer
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting


class ULCollision(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.game_object = None
        self.use_mat = None
        self.prop = None
        self.material = None
        self._set_value("False")
        self.pulse = False
        self._target = None
        self._point = None
        self._normal = None
        self._collision_triggered = False
        self._consumed = False
        self._last_monitored_object = None
        self._objects = []
        self.TARGET = ULOutSocket(self, self.get_target)
        self.POINT = ULOutSocket(self, self.get_point)
        self.NORMAL = ULOutSocket(self, self.get_normal)
        self.OBJECTS = ULOutSocket(self, self.get_objects)

    def get_point(self):
        return self._point

    def get_normal(self):
        return self._normal

    def get_target(self):
        return self._target

    def get_objects(self):
        return self._objects

    def _collision_callback(self, obj, point, normal):
        self._objects.append(obj)
        use_mat = self.get_input(self.use_mat)
        if use_mat:
            material = self.get_input(self.material)
            if material:
                for obj in self._objects:
                    bo = obj.blenderObject
                    if material not in [
                        slot.material.name for
                        slot in
                        bo.material_slots
                    ]:
                        self._objects.remove(obj)
                    else:
                        self._collision_triggered = True
                        self._target = obj
                        self._point = point
                        self._normal = normal
                        return
                self._collision_triggered = False
                return
        else:
            prop = self.get_input(self.prop)
            if prop:
                for obj in self._objects:
                    if prop not in obj:
                        self._objects.remove(obj)
                    else:
                        self._collision_triggered = True
                        self._target = obj
                        self._point = point
                        self._normal = normal
                        return
                self._collision_triggered = False
                return
        self._collision_triggered = True
        self._target = obj
        self._point = point
        self._normal = normal

    def reset(self):
        ULLogicContainer.reset(self)
        self._collision_triggered = False
        self._objects = []

    def _reset_last_monitored_object(self, new_monitored_object):
        if is_invalid(new_monitored_object):
            new_monitored_object = None
        if self._last_monitored_object == new_monitored_object:
            return
        if not isinstance(new_monitored_object, KX_GameObject):
            if self._last_monitored_object is not None:
                self._last_monitored_object.collisionCallbacks.remove(
                    self._collision_callback
                )
                self._last_monitored_object = None
        else:
            if self._last_monitored_object is not None:
                self._last_monitored_object.collisionCallbacks.remove(
                    self._collision_callback
                )
            if new_monitored_object is not None:
                new_monitored_object.collisionCallbacks.append(
                    self._collision_callback
                )
                self._last_monitored_object = new_monitored_object
        self._set_value(False)
        self._target = None
        self._point = None
        self._normal = None
        self._collision_triggered = False

    def evaluate(self):
        last_target = self._target
        game_object = self.get_input(self.game_object)
        self._reset_last_monitored_object(game_object)
        if is_waiting(game_object):
            return
        self._set_ready()
        collision = self._collision_triggered
        if last_target is not self._target:
            self._consumed = False
        if collision and not self.pulse:
            self._set_value(collision and not self._consumed)
            self._consumed = True
        elif self.pulse:
            self._set_value(collision)
        else:
            self._consumed = False
            self._set_value(False)

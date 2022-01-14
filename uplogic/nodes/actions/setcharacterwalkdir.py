from bge import constraints
from bge import logic
from mathutils import Vector
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting
from uplogic.utils import not_met
import bpy


class ULSetCharacterWalkDir(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.walkDir = None
        self.local = False
        self.active = False
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            if self.active:
                game_object = self.get_input(self.game_object)
                physics = constraints.getCharacter(game_object)
                physics.walkDirection = Vector((0, 0, 0))
                self.active = False
            return
        elif not self.active:
            self.active = True
        game_object = self.get_input(self.game_object)
        local = self.local
        walkDir = self.get_input(self.walkDir)
        if is_waiting(game_object, local, walkDir):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if local:
            walkDir = game_object.worldOrientation @ walkDir
        physics = constraints.getCharacter(game_object)
        physics.walkDirection = (
            walkDir /
            bpy.data.scenes[
                logic.getCurrentScene().name
            ].game_settings.physics_step_sub
        )
        self.done = True

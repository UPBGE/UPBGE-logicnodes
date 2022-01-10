from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting
from uplogic.utils import not_met
from uplogic.utils import debug
import bpy


class ULSetMaterial(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.slot = None
        self.mat_name = None
        self.done = False
        self.OUT = ULOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        game_object = self.get_input(self.game_object)
        slot = self.get_input(self.slot) - 1
        mat_name = self.get_input(self.mat_name)
        if not_met(condition):
            return
        if is_invalid(game_object):
            return
        if is_waiting(mat_name, slot):
            return
        self._set_ready()
        bl_obj = game_object.blenderObject
        if slot > len(bl_obj.material_slots) - 1:
            debug('Set Material: Slot does not exist!')
            return
        bl_obj.material_slots[slot].material = bpy.data.materials[mat_name]
        self.done = True

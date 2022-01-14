from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid


class ULReplaceMesh(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.target_game_object = None
        self.new_mesh_name = None
        self.use_display = None
        self.use_physics = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        self._set_ready()
        if not condition:
            return
        target = self.get_input(self.target_game_object)
        mesh = self.get_input(self.new_mesh_name)
        display = self.get_input(self.use_display)
        physics = self.get_input(self.use_physics)
        if is_invalid(target):
            return
        if mesh is None:
            return
        if display is None:
            return
        if physics is None:
            return
        target.replaceMesh(mesh, display, physics)
        if physics:
            target.reinstancePhysicsMesh()
        self.done = True

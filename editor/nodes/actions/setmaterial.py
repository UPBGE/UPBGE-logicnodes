from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicInteger
from ...sockets import NodeSocketLogicMaterial


@node_type
class LogicNodeSetMaterial(LogicNodeActionType):
    bl_idname = "NLSetMaterial"
    bl_label = "Set Material"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetMaterial"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicInteger, "Slot")
        self.add_input(NodeSocketLogicMaterial, "Material")
        self.add_output(NodeSocketLogicCondition, "Done")
        LogicNodeActionType.init(self, context)

    def update_draw(self, context=None):
        if not self.ready:
            return
        obj_socket = self.inputs[1]
        if obj_socket.use_owner or not obj_socket.value:
            return
        if self.inputs[2].value > len(obj_socket.value.material_slots):
            self.inputs[2].value = len(obj_socket.value.material_slots)

    def get_input_names(self):
        return [
            "condition",
            "game_object",
            "slot",
            "mat_name",
        ]

    def get_output_names(self):
        return ['OUT']

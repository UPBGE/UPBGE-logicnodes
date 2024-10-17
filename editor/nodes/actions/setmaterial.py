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
    bl_description = 'Set the material on a slot of an object'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetMaterial"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_input(NodeSocketLogicInteger, "Slot", 'slot')
        self.add_input(NodeSocketLogicMaterial, "Material", 'mat_name')
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        LogicNodeActionType.init(self, context)

    def update_draw(self, context=None):
        if not self.ready:
            return
        obj_socket = self.inputs[1]
        if obj_socket.use_owner or not obj_socket.default_value:
            return
        if self.inputs[2].default_value > len(obj_socket.default_value.material_slots):
            self.inputs[2].default_value = len(obj_socket.default_value.material_slots)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "game_object",
            "slot",
            "mat_name",
        ]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']

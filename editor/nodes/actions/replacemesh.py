from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicMesh
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeReplaceMesh(LogicNodeActionType):
    bl_idname = "NLActionReplaceMesh"
    bl_label = "Replace Mesh"
    bl_description = 'Replace the mesh data of an object'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULReplaceMesh"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Object", 'target_game_object')
        self.add_input(NodeSocketLogicMesh, "New Mesh Name", 'new_mesh_name')
        self.add_input(NodeSocketLogicBoolean, "Use Display", 'use_display', {'default_value': True})
        self.add_input(NodeSocketLogicBoolean, "Use Physics", 'use_physics')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "target_game_object",
            "new_mesh_name",
            "use_display",
            "use_physics"
        ]

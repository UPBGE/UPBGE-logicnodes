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
    nl_module = 'actions'
    nl_class = "ULReplaceMesh"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicMesh, "New Mesh Name")
        self.add_input(NodeSocketLogicBoolean, "Use Display")
        self.add_input(NodeSocketLogicBoolean, "Use Physics")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return [
            "condition",
            "target_game_object",
            "new_mesh_name",
            "use_display",
            "use_physics"
        ]

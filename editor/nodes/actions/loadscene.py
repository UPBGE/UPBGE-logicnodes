from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicScene
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicString
from ...enum_types import _enum_writable_member_names
from bpy.props import EnumProperty


@node_type
class LogicNodeLoadScene(LogicNodeActionType):
    bl_idname = "NLLoadScene"
    bl_label = "Load Scene"
    nl_category = "Scene"
    nl_module = 'actions'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicScene, "Scene")
        self.add_output(NodeSocketLogicCondition, 'Loaded')
        self.add_output(NodeSocketLogicCondition, 'Updated')
        self.add_output(NodeSocketLogicFloat, 'Status')
        self.add_output(NodeSocketLogicString, 'Datatype')
        self.add_output(NodeSocketLogicString, 'Item')
        LogicNodeActionType.init(self, context)

    nl_class = "ULLoadScene"

    def get_input_names(self):
        return ['condition', 'scene']

    def get_output_names(self):
        return ['OUT', 'UPDATED', 'STATUS', 'DATATYPE', 'ITEM']

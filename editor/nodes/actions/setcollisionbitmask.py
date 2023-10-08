from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicBitMask
from ...enum_types import _collision_bitmask_types
from bpy.props import EnumProperty


@node_type
class LogicNodeSetCollisionBitMask(LogicNodeActionType):
    bl_idname = "NLSetCollisionGroup"
    bl_label = "Set Collision Group"
    nl_category = "Physics"
    nl_module = 'actions'
    nl_class = "ULSetCollisionGroup"

    search_tags = [
        ['Set Collision Group', {}],
        ['Set Collision Mask', {'mode': '1'}],
    ]

    mode: EnumProperty(items=_collision_bitmask_types, name='Mode')

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicObject, 'Object')
        self.add_input(NodeSocketLogicBitMask, 'Group')
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'mode')

    def get_attributes(self):
        return [('mode', self.mode)]

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "game_object", 'slots']

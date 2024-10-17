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
    bl_label = "Set Collision Mask"
    bl_description = 'Set the collision integer bitmask of an object'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetCollisionGroup"

    search_tags = [
        ['Set Collision Group', {'nl_label': 'Set Collision Group'}],
        ['Set Collision Mask', {'nl_label': 'Set Collision Mask', 'mode': '1'}],
    ]

    def update_draw(self, context):
        mode = int(self.mode)
        self.nl_label = f"Get Collision {'Mask' if mode > 0 else 'Group'}"

    mode: EnumProperty(items=_collision_bitmask_types, name='Mode', update=update_draw)

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicObject, 'Object', 'game_object')
        self.add_input(NodeSocketLogicBitMask, 'Group', 'slots')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'mode', text='')

    def get_attributes(self):
        return [('mode', self.mode)]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "game_object", 'slots']

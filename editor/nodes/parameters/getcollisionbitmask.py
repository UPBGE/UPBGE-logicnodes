from bpy.types import Context, UILayout

from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject
from ...sockets.integersocket import NodeSocketLogicInteger
from ...enum_types import _collision_bitmask_types
from bpy.props import EnumProperty


@node_type
class LogicNodeGetCollisionBitMask(LogicNodeParameterType):
    bl_idname = "LogicNodeGetCollisionBitMask"
    bl_label = "Get Collision Group"
    bl_description = 'Collision group bitmask'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "GetCollisionGroupNode"

    search_tags = [
        ['Set Collision Group', {'nl_label': 'Set Collision Group'}],
        ['Set Collision Mask', {'nl_label': 'Set Collision Mask', 'mode': '1'}],
    ]

    def update_draw(self, context):
        mode = int(self.mode)
        self.nl_label = f"Get Collision {'Mask' if mode > 0 else 'Group'}"

    mode: EnumProperty(items=_collision_bitmask_types, name='Mode', update=update_draw)

    def init(self, context):
        self.add_input(NodeSocketLogicObject, 'Object', 'game_object')
        self.add_output(NodeSocketLogicInteger, 'Bitmask', 'INT')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'mode', text='')

    def get_attributes(self):
        return [('mode', self.mode)]

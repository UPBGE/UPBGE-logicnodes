from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicVectorXYZAngle
from ...enum_types import _transform_types
from bpy.props import BoolProperty
from bpy.props import EnumProperty


@node_type
class LogicNodeApplyTransform(LogicNodeActionType):
    bl_idname = "LogicNodeApplyTransform"
    bl_label = "Apply Transform"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULApplyTransform"
    bl_description = "Apply transformation changes on an object"

    search_tags = [
        ['Apply Movement', {'nl_label': 'Apply Movement'}],
        ['Apply Rotation', {'nl_label': 'Apply Rotation', 'mode': '1'}],
        ['Apply Force', {'nl_label': 'Apply Force', 'mode': '2'}],
        ['Apply Torque', {'nl_label': 'Apply Torque', 'mode': '3'}],
        ['Apply Impulse', {'nl_label': 'Apply Impulse', 'mode': '4'}]
    ]

    def update_draw(self, context=None):
        self.inputs[2].enabled = self.mode != '1'
        self.inputs[4].enabled = not self.inputs[2].enabled
        self.nl_label = self.search_tags[int(self.mode)][0]
        if self.mode == '4':
            self.inputs[3].enabled = True
            # XXX: Set vec1 socket label?
        else:
            self.inputs[3].enabled = False

    local: BoolProperty(default=False, name='Local')
    mode: EnumProperty(items=_transform_types, name='Mode', update=update_draw)

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_input(NodeSocketLogicVectorXYZ, "Vector", 'vec1')
        self.add_input(NodeSocketLogicVectorXYZ, "Impulse", 'vec2')
        self.add_input(NodeSocketLogicVectorXYZAngle, "Vector", 'vec3')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text='')
        layout.prop(self, "local")

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "game_object", "vec1", "vec2", "vec3"]

    def get_attributes(self):
        return [("local", self.local), ("mode", self.mode)]

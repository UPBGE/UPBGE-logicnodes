from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicColorRGBA
from ...sockets import NodeSocketLogicXYZ
from ...sockets import NodeSocketLogicObject
from ...enum_types import _enum_writable_member_names
from bpy.props import EnumProperty


@node_type
class LogicNodeSetObjectAttr(LogicNodeActionType):
    bl_idname = "NLSetObjectAttributeActionNode"
    bl_label = "Set Position / Rotation / Scale etc."
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetGameObjectAttribue"

    def update_draw(self, context=None):
        color = self.value_type == 'color'
        self.inputs[3].enabled = not color
        self.inputs[4].enabled = color

    value_type: EnumProperty(
        name='Attribute',
        items=_enum_writable_member_names,
        default='worldPosition',
        update=update_draw
    )

    search_tags = [
        ['Set World Position', {'nl_label': 'Set World Position', 'value_type': 'worldPosition'}],
        ['Set World Rotation', {'nl_label': 'Set World Rotation', 'value_type': 'worldOrientation'}],
        ['Set World Linear Velocity', {'nl_label': 'Set World Linear Velocity', 'value_type': 'worldLinearVelocity'}],
        ['Set World Angular Velocity', {'nl_label': 'Set World Angular Velocity', 'value_type': 'worldAngularVelocity'}],
        ['Set World Transform', {'nl_label': 'Set World Transform', 'value_type': 'worldTransform'}],
        ['Set Local Position', {'nl_label': 'Set Local Position', 'value_type': 'localPosition'}],
        ['Set Local Rotation', {'nl_label': 'Set Local Rotation', 'value_type': 'localOrientation'}],
        ['Set Local Linear Velocity', {'nl_label': 'Set Local Linear Velocity', 'value_type': 'localLinearVelocity'}],
        ['Set Local Angular Velocity', {'nl_label': 'Set Local Angular Velocity', 'value_type': 'localAngularVelocity'}],
        ['Set Local Transform', {'nl_label': 'Set Local Transform', 'value_type': 'localTransform'}],
        ['Set Scale', {'nl_label': 'Set Scale', 'value_type': 'worldScale'}],
        ['Set Color', {'nl_label': 'Set Color', 'value_type': 'color'}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicXYZ, "")
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicVectorXYZ, "Value")
        self.add_input(NodeSocketLogicColorRGBA, "Color")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    def get_input_names(self):
        return ["condition", "xyz", "game_object", "attribute_value", "attribute_value"]

    def get_attributes(self):
        return [
            ("value_type", repr(self.value_type)),
        ]

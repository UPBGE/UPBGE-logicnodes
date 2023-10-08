from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicObject
from ...enum_types import _enum_writable_member_names
from bpy.props import EnumProperty


@node_type
class LogicNodeSetObjectAttr(LogicNodeActionType):
    bl_idname = "NLSetObjectAttributeActionNode"
    bl_label = "Set Position / Rotation / Scale etc."
    bl_icon = 'VIEW3D'
    nl_category = "Objects"
    nl_subcat = 'Object Data'
    nl_module = 'actions'
    nl_class = "ULSetGameObjectAttribue"

    value_type: EnumProperty(
        name='Attribute',
        items=_enum_writable_member_names,
        default='worldPosition'
    )
    search_tags = [
        ['Set World Position', {'value_type': 'worldPosition'}],
        ['Set World Rotation', {'value_type': 'worldOrientation'}],
        ['Set World Linear Velocity', {'value_type': 'worldLinearVelocity'}],
        ['Set World Angular Velocity', {'value_type': 'worldAngularVelocity'}],
        ['Set World Transform', {'value_type': 'worldTransform'}],
        ['Set Local Position', {'value_type': 'localPosition'}],
        ['Set Local Rotation', {'value_type': 'localOrientation'}],
        ['Set Local Linear Velocity', {'value_type': 'localLinearVelocity'}],
        ['Set Local Angular Velocity', {'value_type': 'localAngularVelocity'}],
        ['Set Local Transform', {'value_type': 'localTransform'}],
        ['Set Scale', {'value_type': 'worldScale'}],
        ['Set Color', {'value_type': 'color'}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicVectorXYZ, "")
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicVectorXYZ, "Value")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    def get_input_names(self):
        return ["condition", "xyz", "game_object", "attribute_value"]

    def get_attributes(self):
        return [
            ("value_type", f'"{self.value_type}"'),
        ]

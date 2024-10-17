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
    bl_label = "Set Attribute"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetGameObjectAttribue"
    bl_description = 'Set an attribute of an object'
    bl_width_default = 180

    def update_draw(self, context=None):
        color = self.value_type == 'color'
        self.inputs[3].enabled = not color
        self.inputs[4].enabled = color
        self.nl_label = self._names[self.value_type]

    value_type: EnumProperty(
        name='Set Attribute',
        items=_enum_writable_member_names,
        default='worldPosition',
        update=update_draw
    )

    _names = {
        'worldPosition': 'Set World Position',
        'worldOrientation': 'Set World Orientation',
        'worldLinearVelocity': 'Set World Linear Velocity',
        'worldAngularVelocity': 'Set World Angular Velocity',
        'worldTransform': 'Set World Transform',
        'localPosition': 'Set Local Position',
        'localOrietation': 'Set Local Orientation',
        'localLinearVelocity': 'Set Local Linear Velocity',
        'localAngularVelocity': 'Set Local Angular Velocity',
        'localTransform': 'Set Local Transform',
        'worldScale': 'Set Scale',
        'color': 'Set Color'
    }

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
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicXYZ, "", 'xyz', {'default_value': (True, True, True)})
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_input(NodeSocketLogicVectorXYZ, "Value", 'attribute_value')
        self.add_input(NodeSocketLogicColorRGBA, "Color", 'attribute_value')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "xyz", "game_object", "attribute_value", "attribute_value"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    def get_attributes(self):
        return [("value_type", repr(self.value_type))]

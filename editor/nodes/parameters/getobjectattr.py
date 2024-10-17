from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicMatrix
from ...sockets import NodeSocketLogicColorRGBA
from ...enum_types import _enum_readable_member_names
from ...name_maps import _object_attrs
from bpy.props import EnumProperty


@node_type
class LogicNodeGetObjectAttr(LogicNodeParameterType):
    bl_idname = "NLObjectAttributeParameterNode"
    bl_label = "Get Attribute"
    bl_description = 'An attribute of an object'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULObjectAttribute"
    bl_width_default = 180

    def update_draw(self, context=None):
        if not self.ready:
            return
        if len(self.outputs) < 2:
            self.outputs[0].enabled = True
            return
        elif self.attr_name in [
            'worldPosition',
            'localPosition',
            'worldScale',
            'localScale',
            'worldLinearVelocity',
            'localLinearVelocity',
            'worldAngularVelocity',
            'localAngularVelocity',
        ]:
            self.outputs[0].enabled = False
            self.outputs[1].enabled = True
            self.outputs[1].name = _object_attrs[self.attr_name]
            self.outputs[2].enabled = False
            self.outputs[3].enabled = False
            self.outputs[4].enabled = False
        elif self.attr_name in [
            'localOrientation',
            'worldOrientation',
            'localTransform',
            'worldTransform'
        ]:
            self.outputs[0].enabled = False
            self.outputs[1].enabled = False
            self.outputs[2].enabled = False
            self.outputs[3].enabled = True
            self.outputs[4].enabled = False
        elif self.attr_name == 'color':
            self.outputs[0].enabled = False
            self.outputs[1].enabled = False
            self.outputs[2].enabled = False
            self.outputs[3].enabled = False
            self.outputs[4].enabled = True
        elif self.attr_name == 'visible':
            self.outputs[0].enabled = False
            self.outputs[1].enabled = False
            self.outputs[2].enabled = True
            self.outputs[3].enabled = False
            self.outputs[4].enabled = False
        else:
            self.outputs[0].enabled = True
            self.outputs[1].enabled = False
            self.outputs[2].enabled = False
            self.outputs[3].enabled = False
            self.outputs[4].enabled = False
        self.nl_label = self._names[self.attr_name]

    search_tags = [
        ['Get World Position', {'nl_label': 'Get World Position', 'attr_name': 'worldPosition'}],
        ['Get World Rotation', {'nl_label': 'Get World Rotation', 'attr_name': 'worldOrientation'}],
        ['Get World Linear Velocity', {'nl_label': 'Get World Linear Velocity', 'attr_name': 'worldLinearVelocity'}],
        ['Get World Angular Velocity', {'nl_label': 'Get World Angular Velocity', 'attr_name': 'worldAngularVelocity'}],
        ['Get World Transform', {'nl_label': 'Get World Transform', 'attr_name': 'worldTransform'}],
        ['Get Local Position', {'nl_label': 'Get Local Position', 'attr_name': 'localPosition'}],
        ['Get Local Rotation', {'nl_label': 'Get Local Rotation', 'attr_name': 'localOrientation'}],
        ['Get Local Linear Velocity', {'nl_label': 'Get Local Linear Velocity', 'attr_name': 'localLinearVelocity'}],
        ['Get Local Angular Velocity', {'nl_label': 'Get Local Angular Velocity', 'attr_name': 'localAngularVelocity'}],
        ['Get Local Transform', {'nl_label': 'Get Local Transform', 'attr_name': 'localTransform'}],
        ['Get Scale', {'nl_label': 'Get Scale', 'attr_name': 'worldScale'}],
        ['Get Color', {'nl_label': 'Get Color', 'attr_name': 'color'}],
        ['Get Name', {'nl_label': 'Get Name', 'attr_name': 'name'}],
        ['Get Visibility', {'nl_label': 'Get Visibility', 'attr_name': 'visibility'}]
    ]

    _names = {
        'worldPosition': 'Get World Position',
        'worldOrientation': 'Get World Orientation',
        'worldLinearVelocity': 'Get World Linear Velocity',
        'worldAngularVelocity': 'Get World Angular Velocity',
        'worldTransform': 'Get World Transform',
        'localPosition': 'Get Local Position',
        'localOrietation': 'Get Local Orientation',
        'localLinearVelocity': 'Get Local Linear Velocity',
        'localAngularVelocity': 'Get Local Angular Velocity',
        'localTransform': 'Get Local Transform',
        'worldScale': 'Get Scale',
        'color': 'Get Color'
    }

    attr_name: EnumProperty(
        items=_enum_readable_member_names,
        name="Get Attribute",   
        default="worldPosition",
        update=update_draw
    )

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_output(NodeSocketLogicString, "Value", 'OUT')
        self.add_output(NodeSocketLogicVectorXYZ, "Vector", 'OUT', {'enabled': False})
        self.add_output(NodeSocketLogicBoolean, "Visible", 'OUT', {'enabled': False})
        self.add_output(NodeSocketLogicMatrix, "Orientation", 'OUT', {'enabled': False})
        self.add_output(NodeSocketLogicColorRGBA, "Color", 'OUT', {'enabled': False})
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'attr_name', text="")

    def get_attributes(self):
        return [("attribute_name", repr(self.attr_name))]

    # XXX Remove for 5.0
    def get_input_names(self):
        return ["game_object"]

    # XXX Remove for 5.0
    def get_output_names(self):
        return ["OUT", "OUT", "OUT", "OUT"]

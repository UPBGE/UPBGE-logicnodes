from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicVectorXYZ
from ...enum_types import _enum_readable_member_names
from ...name_maps import _object_attrs
from ....utilities import update_draw
from bpy.props import EnumProperty


@node_type
class LogicNodeGetObjectAttr(LogicNodeParameterType):
    bl_idname = "NLObjectAttributeParameterNode"
    bl_label = "Get Position / Rotation / Scale etc."
    bl_icon = 'VIEW3D'
    nl_category = "Objects"
    nl_subcat = 'Object Data'
    nl_module = 'parameters'

    search_tags = [
        ['Get World Position', {'attr_name': 'worldPosition'}],
        ['Get World Rotation', {'attr_name': 'worldOrientation'}],
        ['Get World Linear Velocity', {'attr_name': 'worldLinearVelocity'}],
        ['Get World Angular Velocity', {'attr_name': 'worldAngularVelocity'}],
        ['Get World Transform', {'attr_name': 'worldTransform'}],
        ['Get Local Position', {'attr_name': 'localPosition'}],
        ['Get Local Rotation', {'attr_name': 'localOrientation'}],
        ['Get Local Linear Velocity', {'attr_name': 'localLinearVelocity'}],
        ['Get Local Angular Velocity', {'attr_name': 'localAngularVelocity'}],
        ['Get Local Transform', {'attr_name': 'localTransform'}],
        ['Get Scale', {'attr_name': 'worldScale'}],
        ['Get Color', {'attr_name': 'color'}],
        ['Get Name', {'attr_name': 'name'}]
    ]

    attr_name: EnumProperty(items=_enum_readable_member_names, name="", default="worldPosition", update=update_draw)

    def update_draw(self):
        if len(self.outputs) < 1:
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
            'color',
            'worldOrientation',
            'localOrientation'
        ]:
            self.outputs[0].enabled = False
            self.outputs[1].enabled = True
            self.outputs[1].name = _object_attrs[self.attr_name]
            self.outputs[2].enabled = False
        elif self.attr_name == 'visible':
            self.outputs[0].enabled = False
            self.outputs[1].enabled = False
            self.outputs[2].enabled = True
        else:
            self.outputs[0].enabled = True
            self.outputs[1].enabled = False
            self.outputs[2].enabled = False

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicParameter, "Value")
        self.inputs[-1].enabled = False
        self.add_output(NodeSocketLogicParameter, "Value")
        self.add_output(NodeSocketLogicVectorXYZ, "Vector")
        self.outputs[-1].enabled = False
        self.add_output(NodeSocketLogicBoolean, "Visible")
        self.outputs[-1].enabled = False
        self.update_draw()

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'attr_name', text="")

    def get_attributes(self):
        return [("attribute_name", f'"{self.attr_name}"')]

    def get_netlogic_class_name(self):
        return "ULObjectAttribute"

    def get_input_names(self):
        return ["game_object", "_attr_name"]

    def get_output_names(self):
        return ["VAL", "VEC", "BOOL"]

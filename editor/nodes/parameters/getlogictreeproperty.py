from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicInteger
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicColorRGB
from ...sockets import NodeSocketLogicColorRGBA
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicCollection
from ...sockets import NodeSocketLogicMaterial
from ...sockets import NodeSocketLogicMesh
from ...sockets import NodeSocketLogicNodeGroup
from ...sockets import NodeSocketLogicAnimation
from ...sockets import NodeSocketLogicText
from ...sockets import NodeSocketLogicFont
from ...sockets import NodeSocketLogicSoundFile
from ...sockets import NodeSocketLogicImage
from ...sockets import NodeSocketLogicTreeProperty


@node_type
class LogicNodeGetLogicTreeProperty(LogicNodeParameterType):
    bl_idname = "LogicNodeGetLogicTreeProperty"
    bl_label = "Get Tree Property"
    bl_description = 'Retrieve a property stored on this logic tree'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetLogicTreeProperty"

    def update_draw(self, context=None):
        if context is None:
            return
        tree = getattr(context.space_data, 'edit_tree')
        if not tree:
            return
        prop = self.inputs[0].default_value
        if not (tree and prop):
            return
        vtype = tree.properties[prop].value_type
        for i, output in enumerate(self.outputs):
            output.enabled = i == int(vtype)
    
    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        # layout.operator('logic_nodes.add_logic_tree_property', text='New', icon='PLUS')
        if context is None:
            return
        tree = getattr(context.space_data, 'edit_tree')
        if not tree:
            return
        prop = self.inputs[0].default_value
        if not (tree and prop):
            return
        prop = tree.properties.get(prop, '')
        # if prop and self.inputs[0].show_prop:
        #     layout.prop(prop, 'value_type', text='')

    def init(self, context):
        self.add_input(NodeSocketLogicTreeProperty, "Property", 'property_name')
        self.add_output(NodeSocketLogicFloat, "Property", 'OUT')
        self.add_output(NodeSocketLogicString, "Property", 'OUT', {'enabled': False})
        self.add_output(NodeSocketLogicInteger, "Property", 'OUT', {'enabled': False})
        self.add_output(NodeSocketLogicBoolean, "Property", 'OUT', {'enabled': False})
        self.add_output(NodeSocketLogicVectorXYZ, "Property", 'OUT', {'enabled': False})
        self.add_output(NodeSocketLogicColorRGB, "Property", 'OUT', {'enabled': False})
        self.add_output(NodeSocketLogicColorRGBA, "Property", 'OUT', {'enabled': False})
        self.add_output(NodeSocketLogicObject, "Property", 'OUT', {'enabled': False})
        self.add_output(NodeSocketLogicCollection, "Property", 'OUT', {'enabled': False})
        self.add_output(NodeSocketLogicMaterial, "Property", 'OUT', {'enabled': False})
        self.add_output(NodeSocketLogicMesh, "Property", 'OUT', {'enabled': False})
        self.add_output(NodeSocketLogicNodeGroup, "Property", 'OUT', {'enabled': False})
        self.add_output(NodeSocketLogicAnimation, "Property", 'OUT', {'enabled': False})
        self.add_output(NodeSocketLogicText, "Property", 'OUT', {'enabled': False})
        self.add_output(NodeSocketLogicImage, "Property", 'OUT', {'enabled': False})
        self.add_output(NodeSocketLogicSoundFile, "Property", 'OUT', {'enabled': False})
        self.add_output(NodeSocketLogicFont, "Property", 'OUT', {'enabled': False})
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["property_name"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT' for x in range(len(self.outputs))]

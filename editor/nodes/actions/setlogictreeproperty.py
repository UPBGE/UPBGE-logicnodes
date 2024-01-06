from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
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
class LogicNodeSetLogicTreeProperty(LogicNodeActionType):
    bl_idname = "LogicNodeSetLogicTreeProperty"
    bl_label = "Set Tree Property"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetLogicTreeProperty"

    def update_draw(self, context=None):
        if context is None:
            return
        tree = getattr(context.space_data, 'edit_tree')
        if not tree:
            return
        prop = self.inputs[1].default_value
        if not (tree and prop):
            return
        vtype = tree.properties[prop].value_type
        for i, input in enumerate(self.inputs):
            input.enabled = i < 2 or i == int(vtype) + 2

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicTreeProperty, "Property")
        self.add_input(NodeSocketLogicFloat, "Value", None, {'enabled': False})
        self.add_input(NodeSocketLogicString, "Value", None, {'enabled': False})
        self.add_input(NodeSocketLogicInteger, "Value", None, {'enabled': False})
        self.add_input(NodeSocketLogicBoolean, "Value", None, {'enabled': False})
        self.add_input(NodeSocketLogicVectorXYZ, "Value", None, {'enabled': False})
        self.add_input(NodeSocketLogicColorRGB, "Value", None, {'enabled': False})
        self.add_input(NodeSocketLogicColorRGBA, "Value", None, {'enabled': False})
        self.add_input(NodeSocketLogicObject, "Value", None, {'enabled': False})
        self.add_input(NodeSocketLogicCollection, "Value", None, {'enabled': False})
        self.add_input(NodeSocketLogicMaterial, "Value", None, {'enabled': False})
        self.add_input(NodeSocketLogicMesh, "Value", None, {'enabled': False})
        self.add_input(NodeSocketLogicNodeGroup, "Value", None, {'enabled': False})
        self.add_input(NodeSocketLogicAnimation, "Value", None, {'enabled': False})
        self.add_input(NodeSocketLogicText, "Value", None, {'enabled': False})
        self.add_input(NodeSocketLogicSoundFile, "Value", None, {'enabled': False})
        self.add_input(NodeSocketLogicImage, "Value", None, {'enabled': False})
        self.add_input(NodeSocketLogicFont, "Value", None, {'enabled': False})
        self.add_output(NodeSocketLogicCondition, "Done")
        LogicNodeActionType.init(self, context)

    def get_input_names(self):
        names = ['condition', 'prop_name']
        names.extend(['value' for x in range(16)])
        return names

    def get_output_names(self):
        return ['OUT']

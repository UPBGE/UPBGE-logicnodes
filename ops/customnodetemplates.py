from .operator import operator
from bpy.types import Operator
from ..editor.nodetree import LogicNodeTree
import bpy

ui_node = """from bge_netlogic import custom_node
from bge_netlogic.editor.nodes.node import LogicNodeCustomType
from bge_netlogic.editor.sockets import *


# the @custom_node decorator automatically registers this node-type
# once it has been imported.
@custom_node
class LogicNodeCustomNode(LogicNodeCustomType):
    # `bl_idname` has to stay the same through later versions. Nodes
    # are registered under this ID, so if it changes, blender
    # cannot find nodes added by older versions
    bl_idname = 'LogicNodeCustomNode'
    bl_label = 'My Custom Node'
    bl_description = 'This is a custom node'

    # `nl_module` defines the module (python file) where the game-side
    # implementation of the node is found. In this case, the corresponding
    # file is a text block in the current .blend file, so we need to
    # locally import it by prefixing "."
    nl_module = '.mycustomnode'
    # `nl_class` defines the class to be instantiated and run in-game.
    nl_class = 'MyCustomNode'

    def init(self, context):
        # Add your inputs/outputs here like this:
        #    self.add_input(SOCKET_CLASS_NAME, SOCKET_DISPLAY_NAME, LOGIC_ATTRIBUTE_NAME)
        # SOCKET_CLASS_NAME: This defines the type of the socket
        # SOCKET_DISPLAY_NAME: This string will be shown next to the socket
        # LOGIC_ATTRIBUTE_NAME: This is the corresponding attribute name in the game-side implementation
        self.add_input(NodeSocketLogicObject, 'Object', 'game_object')
        self.add_output(NodeSocketLogicString, 'Name', 'NAME')

        # call the superclass constructor last, because this marks the
        # node as "ready" for the editor.
        LogicNodeCustomType.init(self, context)
"""

logic_node = """from uplogic.nodes import LogicNodeCustom


class MyCustomNode(LogicNodeCustom):

    def __init__(self):
        # Call superclass (parent class) constructor
        super().__init__()

        # Initialize input socket values
        self.game_object = None

        # Initialize output sockets.
        # 'self.add_output()' needs the getter function which is called
        # when a linked socket requests a value.
        self.NAME = self.add_output(self.get_name)

    def get_name(self):
        # This getter function contains the logic that is executed
        # when the first linked socket requests data. Once calculated,
        # the value is stored to avoid re-calculation if there's more
        # than one linked socket.
        game_object = self.get_input(self.game_object)
        return game_object.name

    def evaluate(self):
        # This function is called every frame, regardless of whether the
        # node is needed or not. Keep this as slim as possible.
        pass

    def reset(self):
        # This is called at the end of each frame. Same as with 'evaluate()',
        # keep code in here to a minimum. At the very least you need to call
        # the superclass function though.
        super().reset()

"""


@operator
class LOGIC_NODES_OT_custom_node_templates(Operator):
    bl_idname = "logic_nodes.custom_node_templates"
    bl_label = "Load Custom Logic Node Templates."
    bl_description = 'Load Custom Logic Node Templates'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        ui_node_name = 'MyCustomNode.py'
        ui_node_text = bpy.data.texts.get(ui_node_name, None)
        if ui_node_text is None:
            ui_node_text = bpy.data.texts.new(ui_node_name)
        ui_node_text.clear()
        ui_node_text.write(ui_node)

        logic_node_name = 'mycustomnode.py'
        logic_node_text = bpy.data.texts.get(logic_node_name, None)
        if logic_node_text is None:
            logic_node_text = bpy.data.texts.new(logic_node_name)
        logic_node_text.clear()
        logic_node_text.write(logic_node)
        return {"FINISHED"}
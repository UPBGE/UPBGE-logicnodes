from .operator import operator
from bpy.types import Operator
from ..editor.nodetree import LogicNodeTree
import bpy

ui_node = """from bge_netlogic import custom_node
from bge_netlogic.editor.nodes.node import LogicNodeCustomType
from bge_netlogic.editor.sockets import *


# the @node_type decorator automatically registers this node-type
# once it has been imported in another file, this is normally
# done in .editor.nodes.__init__.py
@custom_node
class MyCustomNode(LogicNodeCustomType):
    # `bl_idname` has to stay the same through later versions. Nodes
    # are registered under this ID, so if it changes blender
    # can't find nodes added by older versions
    bl_idname = "MyCustomNode"
    bl_label = "My Custom Node"

    # `nl_module` defines the exact location where the game-side
    # implementation of the node is found. In this case, the corresponding
    # file is a text block in this .blend file, so we need to locally import
    # it with "."
    nl_module = '.mycustomnode'
    # `nl_class` defines the class to be instantiated and run in-game.
    nl_class = "MyCustomNode"

    def init(self, context):
        # Add your inputs/outputs here
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_output(NodeSocketLogicString, "Name")

        # call the superclass constructor last, because this marks the
        # node as "ready" for the editor.
        LogicNodeCustomType.init(self, context)

    # This list has to have as many items as there are inputs.
    # Multiple input sockets can write on the same identifier, which
    # is useful if you enable/disable inputs and want to still only
    # use one IN value. The strings in this list have to correspond
    # to the game-side classes attribute names
    def get_input_names(self):
        return ["game_object"]

    # This list has to have as many items as there are outputs.
    # Multiple output sockets can write on the same identifier, which
    # is useful if you enable/disable outputs and want to still only
    # use one OUT value. The strings in this list have to correspond
    # to the game-side classes attribute names
    def get_output_names(self):
        return ["OUT"]

"""

logic_node = """from uplogic.nodes import LogicNodeCustom
from uplogic.nodes import Output


class MyCustomNode(LogicNodeCustom):

    def __init__(self):
        LogicNodeCustom.__init__(self)
        self.game_object = None
        self.OUT = Output(self, self.get_done)

    def get_done(self):
        game_object = self.get_input(self.game_object)
        return game_object.name

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
        ui_node_name = 'MyCustomNode'
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
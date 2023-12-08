from ...editor.nodes.node import node_type
from ...editor.nodes.node import LogicNodeParameterType
from ...editor.sockets import NodeSocketLogicObject
from ...editor.sockets import NodeSocketLogicString


# the @node_type decorator automatically registers this node-type
# once it has been imported in another file, this is normally
# done in .editor.nodes.__init__.py
@node_type
class LogicNodeCustomNode(LogicNodeParameterType):
    # `bl_idname` has to stay the same through later versions. Nodes
    # are registered under this ID, so if it changes blender
    # can't find nodes added by older versions
    bl_idname = "LogicNodeCustomNode"
    bl_label = "My Custom Node"

    # `nl_module` defines the exact location where the game-side
    # implementation of the node is found.
    nl_module = 'my_custom_package.nodes'
    # `nl_class` defines the class to be instantiated and run in-game.
    nl_class = "MyCustomNode"

    def init(self, context):
        # Add your inputs/outputs here
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_output(NodeSocketLogicString, "Name")

        # call the superclass constructor last, because this marks the
        # node as "ready" for the editor.
        LogicNodeParameterType.init(self, context)

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

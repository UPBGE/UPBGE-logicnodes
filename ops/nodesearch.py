from ..editor.nodes.node import LogicNode
from bpy.props import EnumProperty
from .operator import operator
import itertools
import bpy


class NodeItem:

    def __init__(self, node, label=None, settings={}):
        self.node = node
        self._label = label
        self.settings = settings.copy()

    @property
    def label(self):
        return self._label if self._label is not None else self.node.bl_label

    @property
    def id(self):
        return self.node.bl_idname + self.label

    @property
    def packed(self):
        return (
            self.id,
            self.label,
            ''
        )

    def add(self):
        bpy.ops.node.add_node(type=self.node.bl_idname)
        node = bpy.context.space_data.node_tree.nodes[-1]
        bpy.ops.node.translate_attach("INVOKE_DEFAULT")
        disable_inputs = self.settings.pop('disable_in', [])
        for ipt in disable_inputs:
            node.inputs[ipt].hide = True
        disable_outputs = self.settings.pop('disable_out', [])
        for ipt in disable_outputs:
            node.outputs[ipt].hide = True

        for key, value in self.settings.items():
            setattr(node, key, value)
        # invokeTranslation()



_node_items = {}


@operator
class LOGIC_NODES_OT_node_search(bpy.types.Operator):
    bl_idname = "logic_nodes.node_search"
    bl_label = "Node Search"
    bl_options = {"REGISTER"}
    bl_description = "Search for registered Logic Nodes"
    bl_property = "node"

    def getSearchItems(self, context):
        items = []
        _node_items.clear()
        for item in itertools.chain(getNodeItems()):
            _node_items[item.id] = item
            items.append(item.packed)
        return items

    node: EnumProperty(items=getSearchItems)

    @classmethod
    def poll(cls, context):
        try:
            return context.space_data.node_tree.bl_idname == "BGELogicTree"
        except:
            return False

    def invoke(self, context, event):
        wm = context.window_manager           
        wm.invoke_search_popup(self)
        return {"FINISHED"}

    def execute(self, context):
        _node_items[self.node].add()
        return {"FINISHED"}


def getNodeItems():
    for node in iterLogicNodeClasses():
        if node.deprecated:
            continue
        elif not node.search_tags:
            yield NodeItem(node)
        else:
            for tag in node.search_tags:
                yield NodeItem(node, tag[0], tag[1])


def iterLogicNodeClasses():
    yield from iterSubclassesWithAttribute(LogicNode, "bl_idname")


def iterSubclassesWithAttribute(cls, attribute):
    for subcls in cls.__subclasses__():
        if hasattr(subcls, attribute):
            yield subcls
        else:
            yield from iterSubclassesWithAttribute(subcls, attribute)
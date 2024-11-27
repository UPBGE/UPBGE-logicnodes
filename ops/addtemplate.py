from ..utilities import debug
from ..utilities import error
from ..utilities import success
from .operator import operator
from bpy.types import Operator
from bpy.props import StringProperty
from ..editor.nodetree import LogicNodeTree
import os
import bpy
import json


@operator
class LOGIC_NODES_OT_add_template(Operator):
    bl_idname = "logic_nodes.add_template"
    bl_label = "Add Template"
    bl_description = "Add a template"
    bl_options = {'REGISTER', 'UNDO'}
    nl_template_name: StringProperty()
    owner: StringProperty()

    @classmethod
    def poll(cls, context):
        if not hasattr(context.space_data, 'edit_tree'):
            return False
        tree = context.space_data.edit_tree
        if not tree:
            return False
        if not (tree.bl_idname == LogicNodeTree.bl_idname):
            return False
        elif tree:
            return True
        return False

    def add_node(self, x, y, name, node_type, node_list, links=[], values=[]):
        tree = bpy.context.space_data.edit_tree

        node = tree.nodes.new(node_type)
        node.label = name
        node.location = (x, y)
        node_list.append(node)
        # value looks like this: [input_index or attribute, value_type, value]
        for value in values:
            index = value['index']
            val_type = value.get('type', 'default_value')
            val = value['value']
            if isinstance(index, int):
                node.inputs[index].use_default_value = True
                setattr(node.inputs[index], val_type, val)
            else:
                setattr(node, index, val)
        return node

    def link_node(self, node, links, node_list):
        tree = bpy.context.space_data.edit_tree
        # link looks like this: [from_node, outlink, inlink]
        for link in links:
            from_node = node_list[link[0]]
            outsocket = from_node.outputs[link[1]]
            insocket = node.inputs[link[2]]
            tree.links.new(
                outsocket,
                insocket
            )

    def get_template_path(self):
        addon_path = os.path.join(''.join(bpy.utils.script_paths(subdir='addons', user_pref=False, check_all=False, use_user=False)), 'bge_netlogic')
        addon_path = addon_path if os.path.exists(addon_path) else os.path.join(''.join(bpy.utils.script_paths(subdir='addons_core', user_pref=False, check_all=False, use_user=False)), 'bge_netlogic')
        addon_path = addon_path if os.path.exists(addon_path) else os.path.join(bpy.utils.user_resource('SCRIPTS', path="addons"), 'bge_netlogic')
        return os.path.join(
            addon_path,
            'templates',
            self.nl_template_name + '.json'
        )

    def execute(self, context):
        debug('Adding template...')
        tree = context.space_data.edit_tree
        jf = json.load(open(self.get_template_path()))
        content = jf['nodes']

        if tree is None:
            error('Cannot add template! Aborting...')
            return {'FINISHED'}
        for node in tree.nodes:
            node.select = False

        nodes = []
        for c in content:
            self.add_node(
                c['x'],
                c['y'],
                c['label'],
                c['node_type'],
                nodes,
                values=c['values']
            )
        i = 0
        for c in content:
            self.link_node(nodes[i], c['links'], nodes)
            i += 1

        for node in nodes:
            node.select = True
            if node.label == 'Speed':
                continue
            node.hide = True
            for socket in node.inputs:
                if not socket.is_linked:
                    socket.hide = True
            for socket in node.outputs:
                if not socket.is_linked:
                    socket.hide = True

        bpy.ops.node.translate_attach("INVOKE_DEFAULT")
        success('Added Template.')
        return {'FINISHED'}
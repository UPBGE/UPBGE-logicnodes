from ..utilities import warn
from ..utilities import debug
from ..utilities import error
from ..utilities import success
from .operator import operator
from bpy.types import Operator
from bpy.props import StringProperty
import bpy


NODE_ATTRS = [
    'default_value',
    'value',
    'game_object',
    'use_toggle',
    'use_value',
    'true_label',
    'false_label',
    'value_type',
    'bool_editor',
    'int_editor',
    'float_editor',
    'string_editor',
    'radians',
    'portal',
    'filepath_value',
    'sound_value',
    'float_field',
    'expression_field',
    'input_type',
    'title',
    'local',
    'operator',
    'formatted',
    'pulse',
    'hide',
    'label',
    'ref_index',
    'use_owner',
    'use_active',
    'advanced'
]


@operator
class LOGIC_NODES_OT_pack_new_tree(Operator):
    bl_idname = "logic_nodes.pack_new_tree"
    bl_label = "Pack Into New Tree"
    bl_description = "Convert selected Nodes to a new tree. Will be applied to selected object.\nWARNING: All Nodes connected to selection must be selected too"
    bl_options = {'REGISTER', 'UNDO'}
    new_tree_name: StringProperty(default='NewTree', name='New Tree Name')

    @classmethod
    def poll(cls, context):
        return True

    def _index_of(self, item, a_iterable):
        i = 0
        for e in a_iterable:
            if e == item:
                return i
            i += 1

    def group_make(self, group_name, add_nodes):
        node_tree = bpy.data.node_groups.new(group_name, 'BGELogicTree')
        group_name = node_tree.name

        nodes = node_tree.nodes
        new_nodes = {}
        parent_tree = bpy.context.space_data.edit_tree
        locs = []

        for node in add_nodes:
            added_node = nodes.new(node.bl_idname)
            added_node.location = node.location
            new_nodes[node] = added_node

        for old_node in new_nodes:
            new_node = new_nodes[old_node]
            for attr in dir(old_node):
                try:
                # if attr in NODE_ATTRS:
                    setattr(new_node, attr, getattr(old_node, attr))
                except:
                    warn('Attribute {} not writable.'.format(attr))
                    
            for socket in old_node.outputs:
                for link in socket.links:
                    to_node = link.to_node
                    if to_node not in add_nodes:
                        msg = 'Some linked Nodes are not selected!'
                        self.report({"ERROR"}, msg)
                        error(msg)
                        bpy.data.node_groups.remove(node_tree)
                        return None
            for socket in old_node.inputs:
                index = self._index_of(socket, old_node.inputs)
                for attr in dir(socket):
                    if attr in NODE_ATTRS or attr.startswith('slot_'):
                        try:
                            if attr != 'label':
                                setattr(new_node.inputs[index], attr, getattr(socket, attr))
                        except Exception:
                            warn('Attribute {} not writable.'.format(attr))
                for link in socket.links:
                    try:
                        output_socket = link.from_socket
                        output_node = new_nodes[output_socket.node]
                        outdex = self._index_of(output_socket, output_socket.node.outputs)
                        node_tree.links.new(new_node.inputs[index], output_node.outputs[outdex])
                    except Exception:
                        bpy.data.node_groups.remove(node_tree)
                        msg = 'Some linked Nodes are not selected! Aborting...'
                        self.report({"ERROR"}, msg)
                        error(msg)
                        return None
            locs.append(old_node.location)

        redir = parent_tree.nodes.new('NLActionExecuteNetwork')
        redir.inputs[0].default_value = True

        # try:
        redir.inputs[1].use_owner = True
        # except Exception:
        #     msg = 'No Object was selected; Set Object in tree {} manually!'.format(parent_tree.name)
        #     self.report({"WARNING"}, msg)
        #     warn(msg)
        redir.inputs[2].value = bpy.data.node_groups[group_name]  # XXX: Legacy
        redir.inputs[2].default_value = bpy.data.node_groups[group_name]
        redir.location = self.avg_location(locs)
        node_tree.use_fake_user = True
        success(f'Created Node Tree {group_name}.')
        for old_node in new_nodes:
            parent_tree.nodes.remove(old_node)
        return node_tree

    def avg_location(self, locs):
        avg_x = 0
        avg_y = 0
        for v in locs:
            avg_x += v[0]
            avg_y += v[1]
        avg_x /= len(locs)
        avg_y /= len(locs)
        return (avg_x, avg_y)

    def execute(self, context):
        debug('Packing Group...')
        if not self.new_tree_name:
            return {'CANCELLED'}
        nodes_to_group = []
        tree = context.space_data.edit_tree

        if tree is None:
            error('Could not pack group! Aborting...')
            return {'FINISHED'}
        for node in tree.nodes:
            if node.select:
                nodes_to_group.append(node)
        if len(nodes_to_group) > 0:
            name = self.new_tree_name
            self.group_make(name, nodes_to_group)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)
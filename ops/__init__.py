import os
import sys
import json
import bpy
import bge_netlogic
import bge_netlogic.utilities as utils
from bpy_extras.io_utils import ImportHelper
import webbrowser


NODE_ATTRS = [
    'value',
    'game_object',
    'default_value',
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
    'filepath_value',
    'sound_value',
    'float_field',
    'expression_field',
    'input_type',
    'value_x',
    'value_y',
    'value_z',
    'title',
    'local',
    'operator',
    'formatted',
    'pulse',
    'hide',
    'label',
    'ref_index',
    'use_owner',
    'advanced'
]


class NLInstallUplogicModuleOperator(bpy.types.Operator):
    bl_idname = "bge_netlogic.install_uplogic_module"
    bl_label = "Install or Update Uplogic Module"
    bl_description = (
        'Downloads the latest version of the uplogic module required for '
        'running logic nodes.\n\n'
        'NOTE: This may take a few seconds and requires internet connection.'
    )
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        utils.notify('Installing uplogic module...')
        try:
            os.system(f'"{sys.executable}" -m ensurepip')
            os.system(f'"{sys.executable}" -m pip install uplogic --upgrade')
            bge_netlogic.UPLOGIC_INSTALLED = True
            utils.success('Installed.')
        except Exception as e:
            utils.error('Install failed. Error:')
            utils.error(e)
        return {"FINISHED"}


class NLInstallFakeBGEModuleOperator(bpy.types.Operator):
    bl_idname = "bge_netlogic.install_fake_bge_module"
    bl_label = "Install or Update BGE Stub Module"
    bl_description = (
        'Downloads the latest version of the fake bge module to avoid errors.'
        'NOTE: This may take a few seconds and requires internet connection.'
    )
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        utils.notify('Installing bge stub module...')
        try:
            os.system(f'"{sys.executable}" -m ensurepip')
            os.system(f'"{sys.executable}" -m pip install upbge-stubs==0.3.1.26.dev1705922753')
            bge_netlogic.UPLOGIC_INSTALLED = True
            utils.success('Installed.')
        except Exception as e:
            utils.error('Install failed. Error:')
            utils.error(e)
        return {"FINISHED"}


class TreeCodeWriterOperator(bpy.types.Operator):
    bl_idname = "bgenetlogic.treecodewriter_operator"
    bl_label = "Timed code writer"
    bl_options = {'REGISTER', 'UNDO'}
    timer = None

    def modal(self, context, event):
        if event.type == "TIMER":
            bge_netlogic._consume_update_tree_code_queue()
        return {'PASS_THROUGH'}

    def execute(self, context):
        if context.window is None:
            utils.warn('Working Window not found, hibernating...')
            bge_netlogic._tree_code_writer_started = False
            return {"FINISHED"}
        if context.window_manager is None:
            utils.warn('Window Manager not found, hibernating...')
            bge_netlogic._tree_code_writer_started = False
            return {"FINISHED"}
        if self.timer is not None:
            utils.warn('No Timer Set. Hibernating...')
            return {'FINISHED'}
        self.timer = context.window_manager.event_timer_add(
            1.0,
            window=context.window
        )
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}


class WaitForKeyOperator(bpy.types.Operator):
    bl_idname = "bge_netlogic.waitforkey"
    bl_label = "Press a Key"
    bl_options = {'REGISTER', 'UNDO'}
    keycode: bpy.props.StringProperty()

    def __init__(self):
        self.socket = None
        self.node = None

    def __del__(self):
        pass

    def execute(self, context):
        return {'FINISHED'}

    def cleanup(self, context):
        if self.socket.value == "Press a key...":
            self.socket.value = ""
        self.socket = None
        self.node = None
        try:
            context.region.tag_redraw()
        except Exception:
            utils.warn("Couldn't redraw panel, code updated.")

    def modal(self, context, event):
        if event.value == "PRESS":
            if (
                event.type == "LEFTMOUSE" or
                event.type == "MIDDLEMOUSE" or
                event.type == "RIGHTMOUSE"
            ):
                self.socket.value = "Press & Choose"
                return {'FINISHED'}
            else:
                value = event.type
                if(self.socket):
                    self.socket.value = value
                else:
                    self.node.value = value
                self.cleanup(context)
                return {'FINISHED'}
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        self.socket = context.socket
        self.node = context.node

        if(not self.socket) and (not self.node):
            utils.error("No socket or Node")
            return {'FINISHED'}

        if(self.socket):
            self.socket.value = "Press a key..."

        else:
            self.node.value = "Press a key..."
        try:
            context.region.tag_redraw()
        except Exception:
            utils.warn("Couldn't redraw panel, code updated.")
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class NLImportProjectNodes(bpy.types.Operator):
    bl_idname = "bge_netlogic.import_nodes"
    bl_label = "Import Logic Nodes"
    bl_options = {'REGISTER', 'UNDO'}
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    @classmethod
    def poll(cls, context):
        if not hasattr(context.space_data, 'tree_type'):
            return False
        tree_type = context.space_data.tree_type
        return tree_type == bge_netlogic.ui.BGELogicTree.bl_idname

    def _create_directories(self):
        local_bge_netlogic_folder = bpy.path.abspath("//bgelogic")
        if not os.path.exists(local_bge_netlogic_folder):
            os.mkdir(local_bge_netlogic_folder)
        local_cells_folder = bpy.path.abspath("//bgelogic/cells")
        if not os.path.exists(local_cells_folder):
            os.mkdir(local_cells_folder)
        local_nodes_folder = bpy.path.abspath("//bgelogic/nodes")
        if not os.path.exists(local_nodes_folder):
            os.mkdir(local_nodes_folder)
        return local_cells_folder, local_nodes_folder

    def _entry_filename(self, p):
        ws = p.rfind("\\")
        us = p.rfind("/")
        if us >= 0 and us > ws:
            return p.split("/")[-1]
        if ws >= 0 and ws > us:
            return p.split("\\")[-1]
        return p

    def _generate_unique_filename(self, output_dir, file_name):
        dot_index = file_name.rfind(".")
        name_part = file_name[:dot_index]
        ext_part = file_name[dot_index + 1:]
        path = os.path.join(output_dir, file_name)
        index = 0
        while os.path.exists(path):
            name = '{}_{}.{}'.format(name_part, index, ext_part)
            path = os.path.join(output_dir, name)
            index += 1
            if index > 100:
                raise RuntimeError(
                    "Can't find a unique name for {}".format(file_name)
                )
        return path

    def _zipextract(self, zip, entry_name, output_dir):
        import shutil
        with zip.open(entry_name) as entry:
            out_file = self._generate_unique_filename(
                output_dir, self._entry_filename(entry_name)
            )
            with open(out_file, "wb") as f:
                shutil.copyfileobj(entry, f)

    def execute(self, context):
        import zipfile
        if not self.filepath:
            return {"FINISHED"}

        if not self.filepath.endswith(".zip"):
            return {"FINISHED"}

        if not zipfile.is_zipfile(self.filepath):
            return {"FINISHED"}

        with zipfile.ZipFile(self.filepath, "r") as f:
            entries = f.namelist()
            cells = [
                x for x in entries if x.startswith("bgelogic/cells/") and
                x.endswith(".py")
            ]
            nodes = [
                x for x in entries if x.startswith("bgelogic/nodes/") and
                x.endswith(".py")
            ]
            if cells or nodes:
                local_cells_folder, local_nodes_folder = (
                    self._create_directories()
                )
                for cell in cells:
                    self._zipextract(f, cell, local_cells_folder)
                for node in nodes:
                    self._zipextract(f, node, local_nodes_folder)
        _do_load_project_nodes(context)
        return {"FINISHED"}

    def invoke(self, context, event):
        self.filepath = ""
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


def _do_load_project_nodes(context):
    utils.notify("Loading project nodes and cells...")
    current_file = context.blend_data.filepath
    file_dir = os.path.dirname(current_file)
    netlogic_dir = os.path.join(file_dir, "bgelogic")
    # cells_dir = os.path.join(netlogic_dir, "cells")
    nodes_dir = os.path.join(netlogic_dir, "nodes")
    if os.path.exists(nodes_dir):
        bge_netlogic.remove_project_user_nodes()
        bge_netlogic.load_nodes_from(nodes_dir)


class NLLoadProjectNodes(bpy.types.Operator):
    bl_idname = "bge_netlogic.load_nodes"
    bl_label = "Reload Project Nodes"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Reload the custom nodes' definitions."

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        _do_load_project_nodes(context)
        return {"FINISHED"}


class NLSelectTreeByNameOperator(bpy.types.Operator):
    bl_idname = "bge_netlogic.select_tree_by_name"
    bl_label = "Edit"
    bl_description = "Edit"
    tree_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        assert self.tree_name is not None
        assert len(self.tree_name) > 0
        blt_groups = [
            g for g in bpy.data.node_groups if (
                g.name == self.tree_name
            ) and (
                g.bl_idname == bge_netlogic.ui.BGELogicTree.bl_idname
            )
        ]
        if len(blt_groups) != 1:
            utils.error("Something went wrong here...")
        for t in blt_groups:
            context.space_data.node_tree = t
        return {'FINISHED'}


class NLRemoveTreeByNameOperator(bpy.types.Operator):
    bl_idname = "bge_netlogic.remove_tree_by_name"
    bl_label = "Remove"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Remove the tree from the selected objects"
    tree_name: bpy.props.StringProperty()
    from_obj_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        import bge_netlogic.utilities as tools
        stripped_tree_name = tools.strip_tree_name(self.tree_name)
        py_module_name = tools.py_module_name_for_stripped_tree_name(
            stripped_tree_name
        )
        py_module_name = py_module_name.split('NL')[-1]
        orig_ob = bpy.context.object
        try:
            ob = bpy.data.objects[self.from_obj_name]
        except Exception:
            ob = orig_ob

        if not ob:
            return {'FINISHED'}

        bpy.context.view_layer.objects.active = ob
        tree_name = utils.make_valid_name(self.tree_name)
        module = f'nl_{tree_name.lower()}'
        for text in bpy.data.texts:
            if text.name == f'{module}.py':
                bpy.data.texts.remove(text)
        gs = ob.game
        for idx, c in enumerate(gs.components):
            if c.module == module:
                bpy.ops.logic.python_component_remove(index=idx)
        controllers = [
            c for c in gs.controllers if py_module_name in c.name
        ]
        actuators = [
            a for a in gs.actuators if py_module_name in a.name
        ]
        sensors = [
            s for s in gs.sensors if py_module_name in s.name
        ]
        for s in sensors:
            bpy.ops.logic.sensor_remove(sensor=s.name, object=ob.name)
        for c in controllers:
            bpy.ops.logic.controller_remove(
                controller=c.name, object=ob.name
            )
        for a in actuators:
            bpy.ops.logic.actuator_remove(actuator=a.name, object=ob.name)

        bge_netlogic.utilities.remove_tree_item_from_object(
            ob, self.tree_name
        )
        bge_netlogic.utilities.remove_network_initial_status_key(
            ob, self.tree_name
        )
        utils.success("Successfully removed tree {} from object {}.".format(
            self.tree_name,
            ob.name
        ))
        bpy.context.view_layer.objects.active = orig_ob
        return {'FINISHED'}

    def remove_tree_from_object_pcoll(self, ob, treename):
        index = None
        i = 0
        for item in ob.bgelogic_treelist:
            if item.tree_name == treename:
                index = i
                break
            i += 1
        if index is not None:
            ob.bgelogic_treelist.remove(index)


class NLUpdateTreeVersionOperator(bpy.types.Operator):
    bl_idname = "bge_netlogic.update_tree_version"
    bl_label = "Update Trees"
    bl_description = "Update trees to the current version of the Addon"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        cases = {
            'NLConditionLogicOperation': self.update_compare_node,
            'NLActionRayCastNode': self.update_ray_node,
            'NLActionStart3DSoundAdv': self.update_3dsound_node,
            'NLActionStartSound': self.update_sound_node,
            'NLActionGetCharacterInfo': self.update_charinfo_node,
            'NLConditionCollisionNode': self.update_collision_node,
            'NLParameterTypeCast': self.update_typecast_node
        }
        for tree in bpy.data.node_groups:
            if tree.bl_idname == bge_netlogic.ui.BGELogicTree.bl_idname:
                for node in tree.nodes:
                    f = cases.get(node.bl_idname, None)
                    if f:
                        f(tree, node)
        return {'FINISHED'}

    def restore_input(self, tree, node, replacer, idx, new_idx=None):
        if new_idx is None:
            new_idx = idx
        ipt = node.inputs[idx]
        new_ipt = replacer.inputs[new_idx]
        for attr in NODE_ATTRS:
            if attr == 'label':
                continue
            if hasattr(ipt, attr):
                setattr(new_ipt, attr, getattr(ipt, attr))
        if ipt.is_linked:
            for link in ipt.links:
                tree.links.new(link.from_socket, new_ipt)

    def restore_output(self, tree, node, replacer, idx, new_idx=None):
        if new_idx is None:
            new_idx = idx
        opt = node.outputs[idx]
        new_opt = replacer.outputs[new_idx]
        if opt.is_linked:
            for link in opt.links:
                tree.links.new(new_opt, link.to_socket)

    def restore_inputs(self, tree, node, replacer, start=0, scope=0, offset=0):
        if scope == 0:
            scope = len(node.inputs) - 1
        for idx in range(scope):
            i = node.inputs[idx+start]
            for attr in NODE_ATTRS:
                if attr == 'label':
                    continue
                if hasattr(i, attr):
                    setattr(replacer.inputs[idx+offset], attr, getattr(i, attr))
            if i.is_linked:
                for link in i.links:
                    tree.links.new(
                        link.from_socket,
                        replacer.inputs[idx+offset]
                    )

    def restore_outputs(self, tree, node, replacer, start=0, scope=0, offset=0):
        if scope == 0:
            scope = len(node.outputs) - 1
        for idx in range(scope):
            o = node.outputs[idx+start]
            if o.is_linked:
                for link in o.links:
                    tree.links.new(
                        replacer.outputs[idx+offset],
                        link.from_socket
                    )

    def update_typecast_node(self, tree, node):
        if node.inputs[0].bl_idname == 'NLTypeCastSocket':
            replacer = tree.nodes.new(node.bl_idname)
            replacer.location = node.location
            replacer.label = node.label
            self.restore_input(tree, node, replacer, 0, 1)
            self.restore_input(tree, node, replacer, 1, 0)
            self.restore_outputs(tree, node, replacer)
            tree.nodes.remove(node)

    def update_collision_node(self, tree, node):
        if len(node.inputs) == 2:
            replacer = tree.nodes.new(node.bl_idname)
            replacer.location = node.location
            replacer.label = node.label
            self.restore_input(tree, node, replacer, 0)
            self.restore_input(tree, node, replacer, 1, 2)
            self.restore_outputs(tree, node, replacer)
            replacer.update_draw()
            tree.nodes.remove(node)

    def update_charinfo_node(self, tree, node):
        if len(node.inputs) > 1:
            replacer = tree.nodes.new(node.bl_idname)
            replacer.location = node.location
            replacer.label = node.label
            self.restore_input(tree, node, replacer, 1, 0)
            self.restore_outputs(tree, node, replacer)
            tree.nodes.remove(node)

    def update_ray_node(self, tree, node):
        if len(node.inputs) < 8:
            replacer = tree.nodes.new(node.bl_idname)
            replacer.location = node.location
            replacer.label = node.label
            self.restore_inputs(tree, node, replacer, 0, 3)
            self.restore_inputs(tree, node, replacer, 4, 2)
            self.restore_input(tree, node, replacer, 6, 7)
            self.restore_outputs(tree, node, replacer)
            tree.nodes.remove(node)

    def update_sound_node(self, tree, node):
        if len(node.outputs) < 3:
            replacer = tree.nodes.new(node.bl_idname)
            replacer.location = node.location
            replacer.label = node.label
            self.restore_inputs(tree, node, replacer)
            self.restore_output(tree, node, replacer, 0)
            self.restore_output(tree, node, replacer, 1, 2)
            tree.nodes.remove(node)

    def update_3dsound_node(self, tree, node):
        if node.inputs[5].bl_idname != 'NLSocketAlphaFloat':
            replacer = tree.nodes.new(node.bl_idname)
            replacer.location = node.location
            replacer.label = node.label
            self.restore_inputs(tree, node, replacer, scope=4)
            self.restore_inputs(
                tree,
                node,
                replacer,
                scope=6,
                start=7,
                offset=8
            )
            self.restore_output(tree, node, replacer, 0)
            self.restore_output(tree, node, replacer, 1, 2)
            tree.nodes.remove(node)
        elif len(node.outputs) < 3:
            replacer = tree.nodes.new(node.bl_idname)
            replacer.location = node.location
            replacer.label = node.label
            self.restore_inputs(tree, node, replacer)
            self.restore_output(tree, node, replacer, 0)
            self.restore_output(tree, node, replacer, 1, 2)
            tree.nodes.remove(node)

    def update_compare_node(self, tree, node):
        if node.inputs[0].bl_idname != 'NLPositiveFloatSocket':
            return
        replacer = tree.nodes.new(node.bl_idname)
        replacer.location = node.location
        replacer.label = node.label
        replacer.operator = node.operator
        replacer.inputs[0].value_type = node.inputs[1].value_type
        replacer.inputs[0].value = node.inputs[1].value
        replacer.inputs[1].value_type = node.inputs[2].value_type
        replacer.inputs[1].value = node.inputs[2].value

        if node.inputs[0].is_linked:
            link = node.inputs[0].links[0]
            tree.links.new(
                link.from_socket,
                replacer.inputs[2]
            )
        if node.inputs[1].is_linked:
            link = node.inputs[1].links[0]
            tree.links.new(
                link.from_socket,
                replacer.inputs[0]
            )
        if node.inputs[2].is_linked:
            link = node.inputs[2].links[0]
            tree.links.new(
                link.from_socket,
                replacer.inputs[1]
            )
        self.restore_outputs(tree, node, replacer)
        tree.nodes.remove(node)


class NLMakeGroupOperator(bpy.types.Operator):
    bl_idname = "bge_netlogic.group_make"
    bl_label = "Pack Into New Tree"
    bl_description = "Convert selected Nodes to a new tree. Will be applied to selected object.\nWARNING: All Nodes connected to selection must be selected too"
    bl_options = {'REGISTER', 'UNDO'}
    owner: bpy.props.StringProperty()

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
                if attr in NODE_ATTRS:
                    setattr(new_node, attr, getattr(old_node, attr))
            for socket in old_node.outputs:
                for link in socket.links:
                    to_node = link.to_node
                    if to_node not in add_nodes:
                        msg = 'Some linked Nodes are not selected!'
                        self.report({"ERROR"}, msg)
                        utils.error(msg)
                        return None
            for socket in old_node.inputs:
                index = self._index_of(socket, old_node.inputs)
                for attr in dir(socket):
                    if attr in NODE_ATTRS or attr.startswith('slot_'):
                        try:
                            if attr != 'label':
                                setattr(new_node.inputs[index], attr, getattr(socket, attr))
                        except Exception:
                            utils.warn('Attribute {} not writable.'.format(attr))
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
                        utils.error(msg)
                        return None
            locs.append(old_node.location)

        for old_node in new_nodes:
            parent_tree.nodes.remove(old_node)
        redir = parent_tree.nodes.new('NLActionExecuteNetwork')
        redir.inputs[0].value = True

        try:
            redir.inputs[1].value = bpy.context.object
        except Exception:
            msg = 'No Object was selected; Set Object in tree {} manually!'.format(parent_tree.name)
            self.report({"WARNING"}, msg)
            utils.warn(msg)
        redir.inputs[2].value = bpy.data.node_groups[group_name]
        redir.location = self.avg_location(locs)
        node_tree.use_fake_user = True
        utils.success(f'Created Node Tree {group_name}.')
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
        utils.debug('Packing Group...')
        nodes_to_group = []
        tree = context.space_data.edit_tree

        if tree is None:
            utils.error('Could not pack group! Aborting...')
            return {'FINISHED'}
        for node in tree.nodes:
            if node.select:
                nodes_to_group.append(node)
        if len(nodes_to_group) > 0:
            name = bpy.context.scene.nl_group_name.name
            if self.group_make(name, nodes_to_group):
                bge_netlogic._update_all_logic_tree_code()
        return {'FINISHED'}


class NLAdd4KeyTemplateOperator(bpy.types.Operator):
    bl_idname = "bge_netlogic.add_4_key_temp"
    bl_label = "4 Key Movement"
    bl_description = "Add 4 Key Movement (WASD with normalized vector)"
    bl_options = {'REGISTER', 'UNDO'}
    nl_template_name = '4keymovement'
    owner: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        if not hasattr(context.space_data, 'edit_tree'):
            return False
        tree = context.space_data.edit_tree
        if not tree:
            return False
        if not (tree.bl_idname == bge_netlogic.ui.BGELogicTree.bl_idname):
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
            val_type = value.get('type', 'value')
            val = value['value']
            if isinstance(index, int):
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
        addon_path = ''.join(bpy.utils.script_paths(subdir='addons', user_pref=False, check_all=False, use_user=False))
        addon_path = os.path.join(addon_path, 'bge_netlogic')
        addon_path = addon_path if os.path.exists(addon_path) else os.path.join(bpy.utils.user_resource('SCRIPTS', path="addons"), 'bge_netlogic')
        return os.path.join(
            addon_path,
            'templates',
            'prefabs',
            self.nl_template_name + '.json'
        )

    def execute(self, context):
        utils.debug('Adding template...')
        tree = context.space_data.edit_tree
        jf = json.load(open(self.get_template_path()))
        content = jf['nodes']

        if tree is None:
            utils.error('Cannot add template! Aborting...')
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

        bpy.ops.transform.translate()
        utils.success('Added 4 Key Template.')
        return {'FINISHED'}


class NLApplyLogicOperator(bpy.types.Operator):
    bl_idname = "bge_netlogic.apply_logic"
    bl_label = "Apply Logic"
    bl_description = "Apply the current tree to the selected objects."
    bl_options = {'REGISTER', 'UNDO'}
    owner: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        if not hasattr(context.space_data, 'edit_tree'):
            return False
        tree = context.space_data.edit_tree
        if not tree:
            return False
        if not (tree.bl_idname == bge_netlogic.ui.BGELogicTree.bl_idname):
            return False
        scene = context.scene
        for ob in scene.objects:
            if ob.select_get():
                return True
        return False

    def execute(self, context):
        current_scene = context.scene
        tree = context.space_data.edit_tree
        active_object = context.object
        if not active_object:
            utils.error('Missing active object, aborting...')
            return {'FINISHED'}
        tree.use_fake_user = True
        # py_module_name = bge_netlogic.utilities.py_module_name_for_tree(tree)
        selected_objects = [
            ob for ob in current_scene.objects if ob.select_get()
        ]
        initial_status = bge_netlogic.utilities.compute_initial_status_of_tree(
            tree.name, selected_objects
        )
        try:
            tree_code_generator.TreeCodeGenerator().write_code_for_tree(tree)
        except Exception as e:
            utils.error(f"Couldn't compile tree {tree.name}!")
            print(e)
        initial_status = True if initial_status is None else False
        for obj in selected_objects:
            tree_name = utils.make_valid_name(tree.name)
            module = f'nl_{tree_name.lower()}'
            name = f'{module}.{tree_name}'
            comps = [c.module for c in obj.game.components]
            if obj.name in bpy.context.view_layer.objects:
                bpy.context.view_layer.objects.active = obj
            else:
                utils.error(f'Object {obj.name} not in view layer, please check for references. Skipping...')
                continue
            if module not in comps:
                bpy.ops.logic.python_component_register(component_name=name)
                utils.success(
                    "Applied tree {} to object {}.".format(
                        tree.name,
                        obj.name
                    )
                )
            else:
                utils.success(
                    "Tree {} already applied to object {}. Updating status.".format(
                        tree.name,
                        obj.name
                    )
                )
            tree_collection = obj.bgelogic_treelist
            contains = False
            for t in tree_collection:
                if t.tree_name == tree.name:
                    contains = True
                    break
            if not contains:
                new_entry = tree_collection.add()
                new_entry.tree_name = tree.name
                new_entry.tree = tree
                # this will set both new_entry.tree_initial_status and add a
                # game property that makes the status usable at runtime
                bge_netlogic.utilities.set_network_initial_status_key(
                    obj, tree.name, initial_status
                )
        bpy.context.view_layer.objects.active = active_object
        return {'FINISHED'}

    def _setup_logic_bricks_for_object(
        self,
        tree,
        py_module_name,
        obj,
        context
    ):
        game_settings = obj.game
        disp_name = py_module_name
        disp_name = disp_name.split('NL')[-1] + '_NL'
        sensor_name = disp_name
        sensor = None
        for s in game_settings.sensors:
            if s.name == sensor_name:
                sensor = s
                break
        if sensor is None:
            bpy.ops.logic.sensor_add(
                type="ALWAYS",
                object=obj.name
            )
            sensor = game_settings.sensors[-1]
            sensor.show_expanded = False
        sensor.pin = True
        sensor.use_pulse_true_level = True
        sensor.name = sensor_name
        # create the controller
        controller_name = disp_name + '_PY'
        controller = None
        for c in game_settings.controllers:
            if c.name == controller_name:
                controller = c
                break
        if controller is None:
            bpy.ops.logic.controller_add(
                type="PYTHON",
                object=obj.name
            )
            controller = game_settings.controllers[-1]
            controller.show_expanded = False
            # if 'NL_OR' not in game_settings.controllers:
            #     bpy.ops.logic.controller_add(
            #         type="LOGIC_OR",
            #         object=obj.name,
            #         name='NL_OR'
            #     )
            # game_settings.controllers[-1].show_expanded = False
        controller.name = controller_name
        controller.type = "PYTHON"
        controller.mode = "MODULE"
        controller.module = bge_netlogic.utilities.py_controller_module_string(
            py_module_name
        )
        # link the brick
        sensor.link(controller)


class NLGenerateLogicNetworkOperatorAll(bpy.types.Operator):
    bl_idname = "bge_netlogic.generate_logicnetwork_all"
    bl_label = "Generate LogicNetwork"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Create the code needed to execute all logic trees"

    @classmethod
    def poll(cls, context):
        return True

    def __init__(self):
        pass

    def _create_external_text_buffer(self, context, buffer_name):
        file_path = bpy.path.abspath("//{}".format(buffer_name))
        return FileTextBuffer(file_path)

    def _create_text_buffer(self, context, buffer_name, external=False):
        if external is True:
            return self._create_external_text_buffer(context, buffer_name)
        blender_text_data_index = bpy.data.texts.find(buffer_name)
        blender_text_data = None
        if blender_text_data_index < 0:
            blender_text_data = bpy.data.texts.new(name=buffer_name)
        else:
            blender_text_data = bpy.data.texts[blender_text_data_index]
        return BLTextBuffer(blender_text_data)

    def execute(self, context):
        for tree in bpy.data.node_groups:
            if tree.bl_idname == bge_netlogic.ui.BGELogicTree.bl_idname:
                try:
                    tree_code_generator.TreeCodeGenerator().write_code_for_tree(tree)
                except Exception as e:
                    utils.error(f"Couldn't compile tree {tree.name}!")
                    utils.error(e)
        utils.set_compile_status(utils.TREE_COMPILED_ALL)
        try:
            context.region.tag_redraw()
        except Exception:
            utils.warn("Couldn't redraw panel, code updated.")
        return {"FINISHED"}



class NLResetEmptySize(bpy.types.Operator):
    bl_idname = "bge_netlogic.reset_empty_scale"
    bl_label = "Set Reverb Volume"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Reset the volume scale"

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return ob and ob.name

    def execute(self, context):
        context.active_object.scale = Vector((1, 1, 1))
        context.active_object.empty_display_type = 'CUBE'
        return {"FINISHED"}


class NLGenerateLogicNetworkOperator(bpy.types.Operator):
    bl_idname = "bge_netlogic.generate_logicnetwork"
    bl_label = "Generate LogicNetwork"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Create the code needed to execute the current logic tree"

    @classmethod
    def poll(cls, context):
        if not hasattr(context.space_data, 'edit_tree'):
            return False
        tree = context.space_data.edit_tree
        if utils.TREE_COMPILED in context.scene.logic_node_settings.tree_compiled:
            return False
        if not tree:
            return False
        if not (tree.bl_idname == bge_netlogic.ui.BGELogicTree.bl_idname):
            return False
        return context.space_data.edit_tree is not None

    def __init__(self):
        pass

    def _create_external_text_buffer(self, context, buffer_name):
        file_path = bpy.path.abspath("//{}".format(buffer_name))
        return FileTextBuffer(file_path)

    def _create_text_buffer(self, context, buffer_name, external=False):
        if external is True:
            return self._create_external_text_buffer(context, buffer_name)
        blender_text_data_index = bpy.data.texts.find(buffer_name)
        blender_text_data = None
        if blender_text_data_index < 0:
            blender_text_data = bpy.data.texts.new(name=buffer_name)
        else:
            blender_text_data = bpy.data.texts[blender_text_data_index]
        return BLTextBuffer(blender_text_data)

    def execute(self, context):
        # ensure that the local "bgelogic" folder exists
        local_bgelogic_folder = bpy.path.abspath("//bgelogic")
        if not os.path.exists(local_bgelogic_folder):
            try:
                os.mkdir(local_bgelogic_folder)
            except PermissionError:
                self.report(
                    {"ERROR"},
                    "Cannot generate the code because the blender file has "
                    "not been saved or the user has no write permission for "
                    "the containing folder."
                )
                utils.set_compile_status(utils.TREE_FAILED)
                return {"FINISHED"}
        # write the current tree in a python module,
        # in the directory of the current blender file
        context = bpy.context
        try:
            tree = context.space_data.edit_tree
            tree_code_generator.TreeCodeGenerator().write_code_for_tree(tree)
        except Exception as e:
            utils.error(e)
            utils.warn('Automatic Update failed, attempting hard generation...')
            if getattr(bpy.context.scene.logic_node_settings, 'use_generate_all', False):
                self.report(
                    {'ERROR'},
                    'Tree to edit not found! Updating All Trees.'
                )
                for tree in bpy.data.node_groups:
                    if tree.bl_idname == bge_netlogic.ui.BGELogicTree.bl_idname:
                        tree_code_generator.TreeCodeGenerator().write_code_for_tree(tree)
                utils.set_compile_status(utils.TREE_FAILED)
                return {"FINISHED"}
            else:
                self.report(
                    {'ERROR'},
                    'Tree to edit not found! Aborting.'
                )
                utils.error('Tree to edit not found! Aborting.')
                utils.set_compile_status(utils.TREE_FAILED)
                return {"FINISHED"}
        utils.set_compile_status(utils.TREE_COMPILED)
        try:
            context.region.tag_redraw()
        except Exception:
            utils.warn("Couldn't redraw panel, code updated.")
        return {"FINISHED"}


class NLAddGlobalOperator(bpy.types.Operator):
    bl_idname = "bge_netlogic.add_global"
    bl_label = "Add Global Value"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Add a value accessible from anywhere"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        category = utils.get_global_category()
        prop = category.content.add()
        prop.name = 'prop'
        prop.string_val = ''
        prop.float_val = 0.0
        prop.int_val = 0
        prop.bool_val = False
        prop.filepath_val = ''
        category.selected = len(category.content) - 1

        return {'FINISHED'}


class NLRemoveGlobalOperator(bpy.types.Operator):
    bl_idname = "bge_netlogic.remove_global"
    bl_label = "Remove Global Value"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Remove a value accessible from anywhere"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        category = utils.get_global_category()
        category.content.remove(category.selected)
        if category.selected > len(category.content) - 1:
            category.selected = len(category.content) - 1
        return {'FINISHED'}


class NLAddGlobalCatOperator(bpy.types.Operator):
    bl_idname = "bge_netlogic.add_global_cat"
    bl_label = "Add Global Category"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Add a global value category"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = context.scene
        cats = scene.nl_global_categories
        cat = cats.add()
        cat.name = 'category'
        scene.nl_global_cat_selected = len(scene.nl_global_categories) - 1

        return {'FINISHED'}


class NLRemoveGlobalCatOperator(bpy.types.Operator):
    bl_idname = "bge_netlogic.remove_global_cat"
    bl_label = "Remove Global Category"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Remove a global value category"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = context.scene
        scene.nl_global_categories.remove(scene.nl_global_cat_selected)
        if scene.nl_global_cat_selected > len(scene.nl_global_categories) - 1:
            scene.nl_global_cat_selected = len(scene.nl_global_categories) - 1
        return {'FINISHED'}


class NLLoadSoundOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "bge_netlogic.load_sound"
    bl_label = "Load Sound"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Load a sound file"

    filter_glob: bpy.props.StringProperty(
        default='*.wav;*.mp3;*.ogg*',
        options={'HIDDEN'}
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.sound.open_mono(
            filepath=self.filepath,
            mono=True,
            relative_path=True,
            filter_sound=True
        )
        return {'FINISHED'}


class NLLoadImageOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "bge_netlogic.load_image"
    bl_label = "Load Image"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Load an image file"

    filter_glob: bpy.props.StringProperty(
        default='*.jpg;*.png;*.jpeg;*.JPEG;',
        options={'HIDDEN'}
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.image.open(
            filepath=self.filepath,
            relative_path=True,
            filter_image=True
        )
        # .value = os.path.basename(self.filepath)
        return {'FINISHED'}


class NLAddPropertyOperator(bpy.types.Operator):
    bl_idname = "bge_netlogic.add_game_prop"
    bl_label = "Add Game Property"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Adds a property available to the UPBGE"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.object.game_property_new()
        print(context)
        bge_netlogic.update_current_tree_code()
        return {'FINISHED'}


class NLAddComponentOperator(bpy.types.Operator):
    bl_idname = "bge_netlogic.add_component"
    bl_label = "Add Component"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Add a python Component to the selected object."

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.logic.python_component_register()
        bge_netlogic.update_current_tree_code()
        return {'FINISHED'}


class NLRemovePropertyOperator(bpy.types.Operator):
    bl_idname = "bge_netlogic.remove_game_prop"
    bl_label = "Add Game Property"
    bl_description = "Remove this property"
    bl_options = {'REGISTER', 'UNDO'}
    index: bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.object.game_property_remove(index=self.index)
        bge_netlogic.update_current_tree_code()
        return {'FINISHED'}


class NLMovePropertyOperator(bpy.types.Operator):
    bl_idname = "bge_netlogic.move_game_prop"
    bl_label = "Move Game Property"
    bl_description = "Move Game Property"
    bl_options = {'REGISTER', 'UNDO'}
    index: bpy.props.IntProperty()
    direction: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.object.game_property_move(
            index=self.index,
            direction=self.direction
        )
        bge_netlogic.update_current_tree_code()
        return {'FINISHED'}


class NLRefreshNodeCode(bpy.types.Operator):
    bl_idname = "bge_netlogic.refresh_node_code"
    bl_label = "Refresh Nodes"
    bl_description = "Update the node package installed in UPBGE python"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.object.game_property_move(
            index=self.index,
            direction=self.direction
        )
        bge_netlogic.update_current_tree_code()
        return {'FINISHED'}


class NLSwitchInitialNetworkStatusOperator(bpy.types.Operator):
    bl_idname = "bge_netlogic.switch_network_status"
    bl_label = "Enable/Disable at start"
    bl_description = "Enables of disables the logic tree at start for the \
        selected objects"
    bl_options = {'REGISTER', 'UNDO'}
    tree_name: bpy.props.StringProperty()
    current_status: bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        current_status = self.current_status
        new_status = not current_status
        tree_name = self.tree_name
        scene = context.scene
        updated_objects = [
            ob for ob in scene.objects if ob.select_get() and
            bge_netlogic.utilities.object_has_treeitem_for_treename(
                ob, tree_name
            )
        ]
        for ob in updated_objects:
            bge_netlogic.utilities.set_network_initial_status_key(
                ob, tree_name, new_status
            )
        bge_netlogic.update_current_tree_code()
        return {'FINISHED'}


# Popup the code templates for custom nodes and cells
class NLPopupTemplatesOperator(bpy.types.Operator):
    bl_idname = "bge_netlogic.popup_templates"
    bl_label = "Show Custom Node Templates"
    bl_description = (
        'Load the template code for custom nodes '
        'and cells in the text editor'
    )
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        node_code = self.get_or_create_text_object("my_custom_nodes.py")
        cell_code = self.get_or_create_text_object("my_custom_cells.py")
        self.load_template(node_code, "my_custom_nodes.txt")
        self.load_template(cell_code, "my_custom_cells.txt")
        self.report({"INFO"}, "Templates available in the text editor")
        return {'FINISHED'}

    def load_template(self, text_object, file_name):
        import os
        this_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.dirname(this_dir)
        templates_dir = os.path.join(parent_dir, "templates")
        template_file = os.path.join(templates_dir, file_name)
        text_data = "Error Reading Template File"
        with open(template_file, "r") as f:
            text_data = f.read()
        text_object.from_string(text_data)

    def get_or_create_text_object(self, name):
        index = bpy.data.texts.find(name)
        if index < 0:
            bpy.ops.text.new()
            result = bpy.data.texts[-1]
            result.name = name
            return result
        else:
            return bpy.data.texts[index]


#################################################################################
# Web Buttons
#################################################################################


class NLAddonPatreonButton(bpy.types.Operator):
    bl_idname = "bge_netlogic.donate"
    bl_label = "Support this Project"
    bl_description = "Consider supporting this Add-On"

    def execute(self, context):
        webbrowser.open('https://www.buymeacoffee.com/izaz')
        return {"FINISHED"}


class NLBGEDocsButton(bpy.types.Operator):
    bl_idname = "bge_netlogic.bge_docs"
    bl_label = "Engine API"

    def execute(self, context):
        webbrowser.open('https://upbge.org/api')
        return {"FINISHED"}


class NLUPBGEDocsButton(bpy.types.Operator):
    bl_idname = "bge_netlogic.upbge_docs"
    bl_label = "Manual"

    def execute(self, context):
        webbrowser.open('https://upbge.org/manual')
        return {"FINISHED"}


class NLDocsButton(bpy.types.Operator):
    bl_idname = "bge_netlogic.nl_docs"
    bl_label = "Logic Nodes Documentation"

    def execute(self, context):
        webbrowser.open('https://github.com/IzaZed/Uchronian-Logic-UPBGE-Logic-Nodes/wiki')
        return {"FINISHED"}


class NLAddonGithubButton(bpy.types.Operator):
    bl_idname = "bge_netlogic.github"
    bl_label = "GitHub"
    bl_description = "Get involved with development"

    def execute(self, context):
        webbrowser.open('https://github.com/IzaZed/Uchronian-Logic-UPBGE-Logic-Nodes/issues')
        return {"FINISHED"}
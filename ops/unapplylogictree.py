from .operator import operator
from ..utilities import success
from ..utilities import strip_tree_name
from ..utilities import py_module_name_for_stripped_tree_name
from ..utilities import make_valid_name
from ..utilities import success
from ..utilities import remove_tree_item_from_object
from ..utilities import remove_network_initial_status_key
from bpy.types import Operator
import bpy


@operator
class LOGIC_NODES_OT_unapply_logic_tree(Operator):
    bl_idname = "logic_nodes.unapply_logic_tree"
    bl_label = "Remove"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Remove the tree from the selected objects"
    tree_name: bpy.props.StringProperty()
    from_obj_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        stripped_tree_name = strip_tree_name(self.tree_name)
        py_module_name = py_module_name_for_stripped_tree_name(
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
        tree_name = make_valid_name(self.tree_name)
        module = f'nl_{tree_name.lower()}'
        for text in bpy.data.texts:
            if text.name == f'{module}.py':
                bpy.data.texts.remove(text)
        gs = ob.game
        for idx, c in enumerate(gs.components):
            if c.module == module:
                bpy.ops.logic.python_component_remove(index=idx)

        # XXX: Remove this block in a future update; Legacy code
        #-------------------------------------------------------
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
        # XXX: Finish
        #-----------------------------------------------------------------

        remove_tree_item_from_object(
            ob, self.tree_name
        )
        remove_network_initial_status_key(
            ob, self.tree_name
        )
        success("Successfully removed tree {} from object {}.".format(
            self.tree_name,
            ob.name
        ))
        bpy.context.view_layer.objects.active = orig_ob
        return {'FINISHED'}

    def remove_tree_from_object_pcoll(self, ob, treename):
        index = None
        i = 0
        for item in ob.logic_trees:
            if item.tree_name == treename:
                index = i
                break
            i += 1
        if index is not None:
            ob.logic_trees.remove(index)
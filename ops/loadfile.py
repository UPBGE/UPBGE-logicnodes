from ..utilities import notify
from ..utilities import error
from ..utilities import success
from .operator import operator
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.props import IntProperty
from bpy.props import PointerProperty
import bpy


@operator
class LOGIC_NODES_OT_load_sound(Operator, ImportHelper):
    bl_idname = "logic_nodes.load_sound"
    bl_label = "Load Sound"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Load a sound file"

    filter_glob: StringProperty(
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


@operator
class LOGIC_NODES_OT_load_image(Operator, ImportHelper):
    bl_idname = "logic_nodes.load_image"
    bl_label = "Load Image"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Load an image file"

    filter_glob: StringProperty(
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
        return {'FINISHED'}


@operator
class LOGIC_NODES_OT_load_font(Operator, ImportHelper):
    bl_idname = "logic_nodes.load_font"
    bl_label = "Load Font"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Load an image file"

    filter_glob: StringProperty(
        default='*.ttf;*.otf;',
        options={'HIDDEN'}
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.data.fonts.load(self.filepath, check_existing=True)
        return {'FINISHED'}

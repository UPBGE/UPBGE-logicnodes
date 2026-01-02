from .operator import operator
from bpy.types import Operator
import os
import sys
import bpy
from ..utilities import install_scripts
import shutil
import json
import subprocess


@operator
class LOGIC_NODES_OT_generate_project(Operator):
    bl_idname = "logic_nodes.generate_project"
    bl_label = "Generate"
    # bl_options = {'REGISTER'}
    bl_description = "Generate basic structure for a new project"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        prefs = bpy.context.preferences.addons['bge_netlogic'].preferences
        project_path = bpy.path.abspath(prefs.project_path)

        upbge_path = os.path.join(bpy.path.abspath(sys.executable), os.path.pardir, os.path.pardir, os.path.pardir, os.path.pardir)

        paths = [
            os.path.join(project_path, 'bin'),
            os.path.join(project_path, 'data', 'assets', 'music'),
            os.path.join(project_path, 'data', 'assets', 'sfx'),
            os.path.join(project_path, 'data', 'assets', 'fonts'),
            os.path.join(project_path, 'data', 'assets', 'textures'),
            os.path.join(project_path, 'data', 'assets', 'ui'),
            os.path.join(project_path, 'data', 'assets', 'videos'),
            os.path.join(project_path, 'data', 'assets', 'models'),
            os.path.join(project_path, 'data', 'levels'),
            os.path.join(project_path, 'data', 'scripts')
        ]
        if prefs.copy_engine:
            try:
                engine_path = os.path.join(project_path, 'engine')
                paths.append(engine_path)
                shutil.copytree(upbge_path, engine_path, dirs_exist_ok=True, symlinks=prefs.use_symlink)
                shutil.copyfile(os.path.join(__file__, os.path.pardir, os.path.pardir, 'utilities', 'build.py'), os.path.join(project_path, 'build.py'))
            except Exception as e:
                print(e)
        for path in paths:
            os.makedirs(path, exist_ok=True)

        mainfile_path = os.path.join(project_path, 'data', 'levels', 'main.blend')
        bpy.ops.wm.save_as_mainfile(filepath=mainfile_path)
        
        subprocess.run(
            f"{upbge_path}/blender --python {os.path.join(__file__, os.path.pardir, os.path.pardir, 'utilities', 'make_launcher.py')} -- {project_path}"
        )

        build_file = os.path.join(project_path, 'build.windows.bat')
        settings_file = os.path.join(project_path, 'bin', 'settings.json')

        with open(build_file, 'w') as f:
            f.write(install_scripts.windows_build)

        # with open(settings_file, 'w') as f:
        settings = {      
            "fullscreen": bpy.context.scene.game_settings.show_fullscreen,
            "resolution": [
                bpy.context.scene.game_settings.resolution_x,
                bpy.context.scene.game_settings.resolution_y
            ]
        }
        json.dump(settings, open(settings_file, 'w'), indent=2)

        def working_message(self, context):
            self.layout.label(text='Successfully generated Project.')
        
        bpy.context.window_manager.popup_menu(working_message, title="Success", icon='INFO')
        mainfile = os.path.join(project_path, 'data', 'levels', 'main.blend')
        bpy.ops.wm.open_mainfile(filepath=bpy.path.abspath(mainfile))
        return {'FINISHED'}
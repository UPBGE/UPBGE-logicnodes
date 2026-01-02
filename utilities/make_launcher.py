import bpy
import os
import sys


launch_script = '''
import bge
import json
import os
import bpy

print(os.path.join(bpy.path.abspath('//'), 'settings.json'))
settings = json.load(open(os.path.join(bpy.path.abspath('//'), 'settings.json')))
bge.render.setFullScreen(settings.get('fullscreen', False))
res = settings.get('resolution', (1280, 720))
bge.render.setWindowSize(res[0], res[1])

bge.logic.getCurrentController().activate('launch')
'''


def save_launcher():
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]  # get all args after "--"
    project_path = argv[0]

    # prefs = bpy.context.preferences.addons['bge_netlogic'].preferences
    # project_path = bpy.path.abspath(prefs.project_path)

    # mainfile_path = os.path.join(project_path, 'data', 'levels', 'main.blend')
    # bpy.ops.wm.save_as_mainfile(filepath=mainfile_path)

    for obj in [o for o in bpy.data.objects]:
        bpy.data.objects.remove(obj)

    cam_data = bpy.data.cameras.new(name='Launcher Camera')
    cam = bpy.data.objects.new(name='Launcher Camera', object_data=cam_data)

    bpy.context.collection.objects.link(cam)
    bpy.context.view_layer.objects.active = cam
    
    text = bpy.data.texts.new(name='launch')
    text.write(launch_script)

    cam = bpy.context.view_layer.objects.active
    bpy.ops.logic.sensor_add(type='ALWAYS')
    bpy.ops.logic.controller_add(type='PYTHON')
    bpy.ops.logic.actuator_add(type='GAME', name='launch')
    sen = cam.game.sensors[0]
    con = cam.game.controllers[0]
    act = cam.game.actuators[0]
    con.text = text
    # act.filename = mainfile_path
    act.filename = '//../data/levels/main.blend'
    con.link(sensor=sen, actuator=act)

    # bpy.ops.file.make_paths_relative()
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(project_path, 'bin', 'launcher.blend'))
    
    bpy.ops.wm.quit_blender()

save_launcher()

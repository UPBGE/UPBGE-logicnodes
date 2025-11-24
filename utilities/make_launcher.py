import bpy
import os


def save_launcher():
    prefs = bpy.context.preferences.addons['bge_netlogic'].preferences
    project_path = bpy.path.abspath(prefs.project_path)

    mainfile_path = os.path.join(project_path, 'data', 'levels', 'main.blend')
    bpy.ops.wm.save_as_mainfile(filepath=mainfile_path)

    for obj in [o for o in bpy.data.objects]:
        bpy.data.objects.remove(obj)

    cam_data = bpy.data.cameras.new(name='Launcher Camera')
    cam = bpy.data.objects.new(name='Launcher Camera', object_data=cam_data)

    bpy.context.collection.objects.link(cam)
    bpy.context.view_layer.objects.active = cam

    cam = bpy.context.view_layer.objects.active
    bpy.ops.logic.sensor_add(type='ALWAYS')
    bpy.ops.logic.controller_add(type='LOGIC_AND')
    bpy.ops.logic.actuator_add(type='GAME')
    sen = cam.game.sensors[0]
    con = cam.game.controllers[0]
    act = cam.game.actuators[0]
    # act.filename = mainfile_path
    act.filename = '//../data/levels/main.blend'
    con.link(sensor=sen, actuator=act)

    # bpy.ops.file.make_paths_relative()
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(project_path, 'bin', 'launcher.blend'))
    
    bpy.ops.wm.quit_blender()

save_launcher()

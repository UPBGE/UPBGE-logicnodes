import bpy
import os
import sys
import shutil
import tempfile
import subprocess


def copy_libs(dst, report=print):
    import platform

    # use python module to find python's libpath
    src = os.path.dirname(platform.__file__)

    # dst points to lib/, but src points to current python's library path, eg:
    #  '/usr/lib/python3.2' vs '/usr/lib'
    # append python's library dir name to destination, so only python's
    # libraries would be copied
    if os.name == 'posix':
        dst = os.path.join(dst, os.path.basename(src))

    if os.path.exists(src):
        write = False
        if os.path.exists(dst):
            write = True
        else:
            write = True
        if write:
            shutil.copytree(src, dst, ignore=lambda dir, contents: [i for i in contents if i == '__pycache__'])
    else:
        report({'WARNING'}, "Python not found in %r, skipping python copy" % src)


def WriteAppleRuntime(player_path, output_path):
    # Enforce the extension
    if not output_path.endswith('.app'):
        output_path += '.app'

    # Use the system's cp command to preserve some meta-data
    os.system('cp -R "%s" "%s"' % (player_path, output_path))

    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(output_path, "Contents/Resources/game.blend"),
                                relative_remap=False,
                                compress=False,
                                copy=True,
                                )

    # Python doesn't need to be copied for OS X since it's already inside blenderplayer.app


def WriteRuntime(
    player_path,
    output_path,
    report=print
):
    import struct

    # Check the paths
    if not os.path.isfile(player_path) and not(os.path.exists(player_path) and player_path.endswith('.app')):
        report({'ERROR'}, "The player could not be found! Runtime not saved")
        return

    # Check if we're bundling a .app
    if player_path.endswith('.app'):
        WriteAppleRuntime(player_path, output_path)
        return

    # Enforce "exe" extension on Windows
    if player_path.endswith('.exe') and not output_path.endswith('.exe'):
        output_path += '.exe'

    # Setup main folders
    blender_dir = os.path.dirname(bpy.app.binary_path)
    runtime_dir = os.path.dirname(output_path)

    # Extract new version string. Only take first 3 digits (i.e 3.0)
    string = bpy.app.version_string.split()[0]
    version_string = string[:3]

    # Create temporal directory
    tempdir = tempfile.mkdtemp()
    player_path_temp = player_path

    # Change the icon for Windows
    player_path_temp = os.path.join(tempdir, bpy.path.clean_name(player_path))
    shutil.copyfile(player_path, player_path_temp)
    rcedit_folder = os.path.join(version_string, "rceditcustom")
    rcedit_path = os.path.join(blender_dir, rcedit_folder, "rcedit-x64.exe")
    if os.path.isfile(os.path.join(runtime_dir, 'icon.ico')):
        subprocess.check_call([rcedit_path, player_path_temp, "--set-icon", os.path.join(runtime_dir, 'icon.ico')])

    # Get the player's binary and the offset for the blend
    file = open(player_path_temp, 'rb')
    player_d = file.read()
    offset = file.tell()
    file.close()

    # Create a tmp blend file (Blenderplayer doesn't like compressed blends)
    blend_path = os.path.join(tempdir, bpy.path.clean_name(output_path))
    bpy.ops.wm.save_as_mainfile(filepath=blend_path,
                                relative_remap=False,
                                compress=False,
                                copy=True,
                                )

    # Get the blend data
    blend_file = open(blend_path, 'rb')
    blend_d = blend_file.read()
    blend_file.close()

    # Get rid of the tmp blend, we're done with it
    os.remove(blend_path)
    os.remove(player_path_temp)
    os.rmdir(tempdir)

    # Create a new file for the bundled runtime
    output = open(output_path, 'wb')

    # Write the player and blend data to the new runtime
    print("Writing runtime...", end=" ")
    output.write(player_d)
    output.write(blend_d)

    # Store the offset (an int is 4 bytes, so we split it up into 4 bytes and save it)
    output.write(struct.pack('B', (offset>>24)&0xFF))
    output.write(struct.pack('B', (offset>>16)&0xFF))
    output.write(struct.pack('B', (offset>>8)&0xFF))
    output.write(struct.pack('B', (offset>>0)&0xFF))

    # Stuff for the runtime
    output.write(b'BRUNTIME')
    output.close()

    print("done")

    # Make the runtime executable on Linux
    if os.name == 'posix':
        os.chmod(output_path, 0o755)

    print("Copying Python files...", end=" ")
    py_folder = os.path.join(version_string, "python", "lib")
    dst = os.path.join(runtime_dir, py_folder)
    copy_libs(dst, report)
    if output_path.endswith('.exe'):
        py_folder = os.path.join(version_string, "python", "DLLs")
        src = os.path.join(blender_dir, py_folder)
        dst = os.path.join(runtime_dir, py_folder)
        shutil.copytree(src, dst)
    print("done")

    # Copy DLLs
    print("Copying DLLs...", end=" ")
    # Dlls at executable level
    for file in [i for i in os.listdir(blender_dir) if i.lower().endswith('.dll')]:
        src = os.path.join(blender_dir, file)
        dst = os.path.join(runtime_dir, file)
        shutil.copy2(src, dst)
    # blender.crt DLLs
    src = os.path.join(blender_dir, "blender.crt")
    dst = os.path.join(runtime_dir, "blender.crt")
    shutil.copytree(src, dst)
    # blender.shared DLLs
    src = os.path.join(blender_dir, "blender.shared")
    dst = os.path.join(runtime_dir, "blender.shared")
    shutil.copytree(src, dst)
    print("done")

#    # Copy linux shared libs
#    print("Copying shared libs...", end=" ")
#    # blender.crt DLLs
#    src = os.path.join(blender_dir, "lib")
#    dst = os.path.join(runtime_dir, "lib")
#    shutil.copytree(src, dst)
#    print("done")

    # Copy datafiles folder
    print("Copying datafiles...", end=" ")
    datafiles_folder = os.path.join(version_string, "datafiles", "gamecontroller")
    src = os.path.join(blender_dir, datafiles_folder)
    dst = os.path.join(runtime_dir, datafiles_folder)
    shutil.copytree(src, dst)
    datafiles_folder = os.path.join(version_string, "datafiles", "colormanagement")
    src = os.path.join(blender_dir, datafiles_folder)
    dst = os.path.join(runtime_dir, datafiles_folder)
    shutil.copytree(src, dst)
    datafiles_folder = os.path.join(version_string, "datafiles", "fonts")
    src = os.path.join(blender_dir, datafiles_folder)
    dst = os.path.join(runtime_dir, datafiles_folder)
    shutil.copytree(src, dst)
    datafiles_folder = os.path.join(version_string, "datafiles", "studiolights")
    src = os.path.join(blender_dir, datafiles_folder)
    dst = os.path.join(runtime_dir, datafiles_folder)
    shutil.copytree(src, dst)
    print("done")

    # Copy modules folder (to have bpy working)
    print("Copying modules...", end=" ")
    modules_folder = os.path.join(version_string, "scripts", "modules")
    src = os.path.join(blender_dir, modules_folder)
    dst = os.path.join(runtime_dir, modules_folder)
    shutil.copytree(src, dst)
    print("done")

    # Copy license folder
    print("Copying UPBGE license folder...", end=" ")
    src = os.path.join(blender_dir, "license")
    dst = os.path.join(runtime_dir, "engine.license")
    shutil.copytree(src, dst)
    license_folder = os.path.join(runtime_dir, "engine.license")
    src = os.path.join(blender_dir, "copyright.txt")
    dst = os.path.join(license_folder, "copyright.txt")
    shutil.copy2(src, dst)
    print("done")
    
    print("Build Finished.")
    


if sys.platform == 'darwin':
    blender_bin_dir = '/' + os.path.join(*bpy.app.binary_path.split('/')[0:-4])
    ext = '.app'
    blenderplayer_name = 'Blenderplayer'
else:
    blender_bin_path = bpy.app.binary_path
    blender_bin_dir = os.path.dirname(blender_bin_path)
    ext = os.path.splitext(blender_bin_path)[-1].lower()
    blenderplayer_name = 'blenderplayer'

default_player_path = os.path.join(blender_bin_dir, blenderplayer_name + ext)

print('\n###########################################################')
print('#   Building Executable, this may take a few minutes...   #')
print('###########################################################\n')

WriteRuntime(default_player_path, bpy.path.abspath('//Launcher'))
import bpy


app_version = bpy.app.version_file
v = f'{app_version[0]}.{app_version[1]}'

windows_build = f"""
echo off

:: Remove old Launcher files
rmdir .\\bin\\{v} /s /q
rmdir .\\bin\\blender.crt /s /q
rmdir .\\bin\\blender.shared /s /q
rmdir .\\bin\\engine.license /s /q
del .\\bin\\*.dll
del .\\bin\\*.exe

:: Remove old build files
rmdir _build /s /q


.\\engine\\{v}\\python\\bin\python -m pip install python-osc
.\\engine\\{v}\python\\bin\python -m pip install pyserial
.\\engine\\blender .\\bin\\launcher.blend --background --python build.py

:: Move content
mkdir _build
mkdir "_build\\bin"
mkdir "_build\\data"
robocopy ".\\bin" ".\\_build\\bin" /s /e
robocopy ".\\data" ".\\_build\\data" /is /s /xf *.blend1 *.blend11 *~

:: Add some build information
echo Time of build: >> .\\_build\\build_data.log
echo %date% %time% >> .\\_build\\build_data.log

set /P "=Build Finished. Press any key to close this window." <nul & pause >nul & echo("""
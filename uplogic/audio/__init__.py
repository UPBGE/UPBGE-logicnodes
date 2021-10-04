from uplogic.audio.audiosystem import ULAudioSystem
from uplogic.audio.sound import ULSound3D
from uplogic.audio.sound import ULSound
from uplogic.data.globaldb import GlobalDB


def update():
    systems = GlobalDB.retrieve('.uplogic_audio').data
    print(systems)
    for system in systems:
        systems[system].update()

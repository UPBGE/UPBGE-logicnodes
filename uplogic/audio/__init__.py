from .audiosystem import ULAudioSystem
from .sound import ULSound2D
from .sound import ULSound3D
from .sound import ULSound
from uplogic.data.globaldb import GlobalDB


def update_sounds():
    systems = GlobalDB.retrieve('.uplogic_audio')
    for system in systems.data:
        if system == 'ln_audio_system':
            continue
        systems.data[system].update()



#volume up, volume down, reset to 100%

#push to talk, invert ptt,
import sound_functers
from node_types import *

def handle_event(event):
    '''Base function for taking in a sdl event and navigating the choice tree'''



root=list_node('root',[
        list_node('soundctl',[
            functer_node('mute mics',sound_functers.soundctl.mute),
            functer_node('unmute mics',sound_functers.soundctl.unmute)
            ]),
        functer_node('s2f1',None)
        ])
if __name__ == '__main__':
    for node,depth in root.get_all():
        print '    '*depth+"%s"%node.title
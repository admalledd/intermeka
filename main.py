import os
import logging
import sys
import itertools
import random

log_name=os.path.join(os.getcwd(),'intermeka.log')
# set up logging to file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=log_name,
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)
logger = logging.getLogger('main')
logger.info('logger set. logging to file:"%s"'%(log_name))
logger.debug('current path: %s'%os.getcwd())


logger.info('importing pysdl-cffi, if it fails good luck!')
sys.path.insert(0, "/home/admalledd/Documents/code/lazer/zzpypy/libs/pysdl-cffi/")
import sdl

from sdl.internal import _ffi
import sdlcffi_event_helper as sdleh

#generate colors: we have three tables: (x,0,0) (x,y,0), (x,y,z) where xyz locations are random
#meaning that we have primary colors, colors with two, and colors with all three
#for the "target" colors, we only allow 4 per primary (dark, dim, lit, bright) (64,128,192,255)
c_range=(192,255)
#first, ct1
ct1=[]
for color in range(3):
    for level in c_range:
        tmp_color=[0,0,0]
        tmp_color[color]=level
        ct1.append(tuple(tmp_color))
ct1=tuple(ct1)
#two randomish...
ct2=[]
for hold_this in range(3):
    tmp_lists=[c_range,c_range,c_range]
    tmp_lists[hold_this]=(0,0,0)#the one color we hold to 0 throughout
    ct2.append(tuple(itertools.product(*tmp_lists)))
ct2=tuple(itertools.chain(*ct2))
COLORS=(ct1,ct2)

import choicer

def main():
    assert sdl.SDL_Init(sdl.SDL_INIT_JOYSTICK|sdl.SDL_INIT_VIDEO) >= 0, 'Unable to initialize SDL'

    mainwindow = sdl.SDL_CreateWindow("SDL Test Window", sdl.SDL_WINDOWPOS_CENTERED,
        sdl.SDL_WINDOWPOS_CENTERED, 512, 512, sdl.SDL_WINDOW_OPENGL | sdl.SDL_WINDOW_SHOWN)
    assert mainwindow, "Unable to create main window"

    renderer = sdl.SDL_CreateRenderer(mainwindow, -1, sdl.SDL_RENDERER_ACCELERATED)
    sdl.SDL_SetRenderDrawColor(renderer,0,255,0,sdl.SDL_ALPHA_OPAQUE)

    #create joystick
    sdl.SDL_JoystickEventState(sdl.SDL_ENABLE)
    for i in range(sdl.SDL_NumJoysticks()):
        logger.info('Joystick #%i is "%s"'%(i,_ffi.string(sdl.SDL_JoystickNameForIndex(i))))
    else:
        joy = sdl.SDL_JoystickOpen(0)
        logger.info('Joystick bound is #0, "%s"',sdl.SDL_JoystickName(joy))

    running=True
    while running:
        #sleep to save CPU
        event = sdleh.get_event_wait(250)
        if event.type != 0:# dont log null-events (timed out on queue wait)
            #logger.debug(event)
            pass
        if event.type == sdl.SDL_JOYBUTTONDOWN:
            if event.button==7:
                #for development, allow closing of intermeka via the controller.
                running = False
            else:
                #call into choicer, where we keep the desicion tree and all that jazz.
                choicer.handle_event(event)
        elif event.type == sdl.SDL_QUIT:
            running = False
        sdl.SDL_RenderClear(renderer)
        sdl.SDL_RenderPresent(renderer)
        color = random.choice(random.choice(COLORS))
        sdl.SDL_SetRenderDrawColor(renderer,color[0],color[1],color[2],sdl.SDL_ALPHA_OPAQUE)
    sdl.SDL_DestroyRenderer(renderer)
    sdl.SDL_DestroyWindow(mainwindow)
    sdl.SDL_Quit()
    
if __name__ == '__main__':
    main()
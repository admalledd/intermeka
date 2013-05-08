import os
import logging
import sys

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

def main():
    assert sdl.SDL_Init(sdl.SDL_INIT_JOYSTICK) >= 0, 'Unable to initialize SDL'

    #create joystick
    sdl.SDL_JoystickEventState(sdl.SDL_ENABLE)
    joy = sdl.SDL_JoystickOpen(0)
    logger.info('Joystick name is "%s"',sdl.SDL_JoystickName(joy))

    running=True
    while running:
        #sleep to save CPU
        event = sdleh.get_event_wait(2500)
        if event == None: continue
        logger.debug(event)
        if event.type == sdl.SDL_JOYBUTTONDOWN:
            if event.button==7:
                #for development, allow closing of intermeka via the controller.
                running = False
            else:
                #call into choicer, where we keep the desicion tree and all that jazz.
                choicer.handle_event(event)

    
    sdl.SDL_Quit()
    
if __name__ == '__main__':
    main()
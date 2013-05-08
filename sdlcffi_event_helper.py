
import sdl
from sdl.internal import _ffi,_LIB,guard,lookup,check_error
class event(object):
    def __init__(self,type,**kwargs):
        self.dict=kwargs
        self.dict['type'] = type 

    def __getattr__(self,name):
        return self.dict[name]
    def __str__(self):
        return '<event(%d-%s %s)>'%(self.type, name_from_eventtype(self.type), self.dict)

def name_from_eventtype(type):
    if type == sdl.SDL_WINDOWEVENT:
        return "WindowEvent"
    if type == sdl.SDL_KEYDOWN:
        return "KeyDown"
    elif type == sdl.SDL_KEYUP:
        return "KeyUp"
    elif type == sdl.SDL_MOUSEMOTION:
        return "MouseMotion"
    elif type == sdl.SDL_MOUSEBUTTONDOWN:
        return "MouseButtonDown"
    elif type == sdl.SDL_MOUSEBUTTONUP:
        return "MouseButtonUp"
    elif type == sdl.SDL_JOYAXISMOTION:
        return "JoyAxisMotion"
    elif type == sdl.SDL_JOYBALLMOTION:
        return "JoyBallMotion"
    elif type == sdl.SDL_JOYHATMOTION:
        return "JoyHatMotion"
    elif type == sdl.SDL_JOYBUTTONUP:
        return "JoyButtonUp"
    elif type == sdl.SDL_JOYBUTTONDOWN:
        return "JoyButtonDown"
    elif type == sdl.SDL_QUIT:
        return "Quit"
    elif type == sdl.SDL_SYSWMEVENT:
        return "SysWMEvent"
    
    if type >= sdl.SDL_USEREVENT and type < sdl.SDL_NUMEVENTS:
        return "UserEvent"
    return "Unknown"

def get_events():
    event = get_event_single()
    while event != None:
        yield event
        event=get_event_single()
def get_event_single():
    __event=sdl.SDL_PollEvent()
    return _convert_event(__event)
def _convert_event(__event):
    if __event == None:     
        return None #out of events

    #print __event.type #test?
    if __event.type == sdl.SDL_QUIT:
        return event(sdl.SDL_QUIT)

    elif __event.type == sdl.SDL_WINDOWEVENT:
        #this one is a bit strange, it really is most if not all "window management" events that occur..
        #print sdl._ffi.string(__event)
        subtype = __event.window.event
        if subtype == sdl.SDL_WINDOWEVENT_SHOWN:
            _msg="Window %d shown"% (__event.window.windowID)

        elif subtype == sdl.SDL_WINDOWEVENT_HIDDEN:
            _msg = "Window %d hidden"% (__event.window.windowID)

        elif subtype == sdl.SDL_WINDOWEVENT_EXPOSED:
            _msg = "Window %d exposed"%(__event.window.windowID)
            
        elif subtype == sdl.SDL_WINDOWEVENT_MOVED:
            _msg = "Window %d moved to %d,%d"%(
                    __event.window.windowID, __event.window.data1,
                    __event.window.data2)
            
        elif subtype == sdl.SDL_WINDOWEVENT_RESIZED:
            _msg = "Window %d resized to %dx%d"%(
                    __event.window.windowID, __event.window.data1,
                    __event.window.data2)
            
        elif subtype == sdl.SDL_WINDOWEVENT_MINIMIZED:
            _msg = "Window %d minimized"%(__event.window.windowID)
            
        elif subtype == sdl.SDL_WINDOWEVENT_MAXIMIZED:
            _msg = "Window %d maximized"%(__event.window.windowID)
            
        elif subtype == sdl.SDL_WINDOWEVENT_RESTORED:
            _msg = "Window %d restored"%(__event.window.windowID)
            
        elif subtype == sdl.SDL_WINDOWEVENT_ENTER:
            _msg = "Mouse entered window %d"%(__event.window.windowID)
            
        elif subtype == sdl.SDL_WINDOWEVENT_LEAVE:
            _msg = "Mouse left window %d"%(__event.window.windowID)
            
        elif subtype == sdl.SDL_WINDOWEVENT_FOCUS_GAINED:
            _msg = "Window %d gained keyboard focus"%(__event.window.windowID)
            
        elif subtype == sdl.SDL_WINDOWEVENT_FOCUS_LOST:
            _msg = "Window %d lost keyboard focus"%(__event.window.windowID)
            
        elif subtype == sdl.SDL_WINDOWEVENT_CLOSE:
            _msg = "Window %d closed"%(__event.window.windowID)
            
        else:
            _msg = "Window %d got unknown event %d"% (__event.window.windowID, __event.window.event)

        return event(__event.type,
                        windowID= __event.window.windowID,
                        event = __event.window.event,
                        data1 = __event.window.data1,
                        data2 = __event.window.data2,
                        msg = _msg
                        )
        
    elif __event.type == sdl.SDL_KEYDOWN:
        return event(__event.type,
                        unicode=__event.key.keysym.unicode,
                        key=__event.key.keysym.sym,
                        mod=__event.key.keysym.mod,
                        scancode=__event.key.keysym.scancode
                        )

    elif __event.type == sdl.SDL_KEYUP:
        return event(__event.type,
                        key=__event.key.keysym.sym,
                        mod=__event.key.keysym.mod,
                        scancode=__event.key.keysym.scancode
                        )

    elif __event.type == sdl.SDL_MOUSEMOTION:
        return event(__event.type,
                            pos=(__event.motion.x, __event.motion.y),
                            rel=(__event.motion.xrel, __event.motion.yrel),
                            buttons=(
                                    (__event.motion.state&(1 << ((1)-1))),
                                    (__event.motion.state&(1 << ((2)-1))),
                                    (__event.motion.state&(1 << ((3)-1)))
                                    )
                            )

    elif __event.type == sdl.SDL_MOUSEBUTTONUP or __event.type == sdl.SDL_MOUSEBUTTONDOWN:
        return event(__event.type,
                            pos=(__event.button.x, __event.button.y),
                            button=__event.button.button
                            )

    elif __event.type == sdl.SDL_JOYAXISMOTION:
        value = __event.jaxis.value/32767.0
        if value >1.0: value = 1.0
        elif value <-1.0: value = -1.0
        return event(__event.type,
                            joy=__event.jaxis.which,
                            axis=__event.jaxis.axis,
                            value=value
                            )

    elif __event.type == sdl.SDL_JOYBALLMOTION:
        return event(__event.type,
                            joy=__event.jball.which,
                            ball=__event.jball.ball,
                            rel=(__event.jball.xrel, __event.jball.yrel)
                            )

    elif __event.type == sdl.SDL_JOYHATMOTION:
        hx = hy = 0
        if __event.jhat.value&sdl.SDL_HAT_UP:
            hy = 1
        elif __event.jhat.value&sdl.SDL_HAT_DOWN:
            hy = -1
        if __event.jhat.value&sdl.SDL_HAT_RIGHT:
            hx = 1
        elif __event.jhat.value&sdl.SDL_HAT_LEFT:
            hx = -1
        return event(__event.type,
                            joy=__event.jhat.which,
                            hat=__event.jhat.hat,
                            value=(hx, hy)
                            )

    elif __event.type == sdl.SDL_JOYBUTTONDOWN or __event.type == sdl.SDL_JOYBUTTONUP:
        return event(__event.type,
                                joy=__event.jbutton.which,
                                button=__event.jbutton.button
                                )
    
    elif __event.type == sdl.SDL_SYSWMEVENT:
        return event(__event.type, msg=event.syswm.msg)
    
    else:
        return event(__event.type, rawevent=__event)
def get_event_wait(timeout=500):
    event = _ffi.new('SDL_Event *')
    lookup("SDL_WaitEventTimeout")(event,timeout)
    if event.type == 0:
        #no event?
        return None
    return _convert_event(event)
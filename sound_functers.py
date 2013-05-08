import logging
import subprocess

__all__ = ['PulseAudioInterface', ]

class pulse_audio(object):
    INPUTS = {}

    def __init__(self):
        self.logger = logging.getLogger('intermeka.sound_functers.pulse_audio')
        self.update_input_list()

    def update_input_list(self):
        self.INPUTS = {}

        proc = subprocess.Popen(
                ['pactl','list','short','sources'], 
                stdout = subprocess.PIPE
            )
        out, err = proc.communicate()
        input_lines = out.split('\n')
        for input_line in input_lines:
            input_line = input_line.strip()
            if not input_line:
                break

            details = input_line.split('\t')

            index = details[0]
            parsed = {
                        'name': details[1],
                        'module': details[2],
                        'sound': details[3],
                        'status': details[4],
                    }
            self.logger.debug("Found device %s" % parsed['name'])
            self.INPUTS[index] = parsed

    def mute(self):
        for index in self.INPUTS.keys():
            subprocess.call(['pactl', 'set-source-mute', str(index),'1'])

    def unmute(self):
        for index in self.INPUTS.keys():
            retval = subprocess.call(['pactl', 'set-source-mute', str(index), '0'])
            
soundctl=pulse_audio()
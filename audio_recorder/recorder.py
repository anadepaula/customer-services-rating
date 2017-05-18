# coding=utf-8

import pyaudio
import wave
from sys import byteorder
from array import array
from struct import pack

class Recorder:
    def __init__(self, audio_file_path):
        self.audio_file_path = audio_file_path
        self.threshold = 3500
        self.chunk_size = 2048
        self.format = pyaudio.paInt16
        self.rate = 32000
        #self.maximum = 16384
        self.maximum = 8192

    # Returns 'True' if below the 'silent' threshold
    def is_silent(self, snd_data):
        return max(snd_data) < self.threshold

    # Average the volume out
    def normalize(self, snd_data):
        times = float(self.maximum)/max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i*times))
        return r

    # Trim the blank spots at the start and end
    def trim(self, snd_data):
        def _trim(snd_data):
            snd_started = False
            r = array('h')

            for i in snd_data:
                if not snd_started and abs(i)>self.threshold:
                    snd_started = True
                    r.append(i)

                elif snd_started:
                    r.append(i)
            return r

        # Trim to the left
        snd_data = _trim(snd_data)

        # Trim to the right
        snd_data.reverse()
        snd_data = _trim(snd_data)
        snd_data.reverse()
        return snd_data

    # Add silence to the start and end of 'snd_data' of length 'seconds' (float)
    def add_silence(self, snd_data, seconds):
        r = array('h', [0 for i in range(int(seconds*self.rate))])
        r.extend(snd_data)
        r.extend([0 for i in range(int(seconds*self.rate))])
        return r

    # Record a word or words from the microphone andreturn the data as an array
    # of signed shorts. Normalizes the audio, trims silence from the start and
    # end, and pads with 0.5 seconds of blank sound to make sure players can
    # play it.

    def record(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.format, channels=1, rate=self.rate,
            input=True, output=True, frames_per_buffer=self.chunk_size)

        num_silent = 0
        snd_started = False

        r = array('h')

        while True:
            # little endian, signed short
            snd_data = array('h', stream.read(self.chunk_size))
            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)

            silent = self.is_silent(snd_data)

            if silent and snd_started:
                num_silent += 1
            elif not silent and not snd_started:
                snd_started = True

            if snd_started and num_silent > 32:
                break

        sample_width = p.get_sample_size(self.format)
        stream.stop_stream()
        stream.close()
        p.terminate()

        r = self.normalize(r)
        r = self.trim(r)
        r = self.add_silence(r, 0.2)
        return sample_width, r

    # Records from the microphone and outputs the resulting data to
    #    'self.audio_file_path'
    def record_to_file(self):
        sample_width, data = self.record()
        data = pack('<' + ('h'*len(data)), *data)

        wf = wave.open(self.audio_file_path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(self.rate)
        wf.writeframes(data)
        wf.close()

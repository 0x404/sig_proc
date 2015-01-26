#!/usr/bin/env python
# encoding: utf-8

# Jakub Młokosiewicz, 2015

from copy import deepcopy
from math import sin, cos, pi
from matplotlib import pyplot
from pylab import zeros, fft

class Wave(object):
    DEFAULT_FS = 500
    DEFAULT_DURATION = 2 * pi

    def __init__(self, values, domain=None, fs=DEFAULT_FS):
        self.values = values
        self.domain = domain
        self.fs = fs

    def plot(self, *args, **kwargs):
        if 'label' not in kwargs:
            try:
                kwargs['label'] = self.label
            except AttributeError:
                pass
        if self.domain:
            pyplot.plot(self.domain, self.values, *args, **kwargs)
        else:
            pyplot.plot(self.values, *args, **kwargs)

    @classmethod
    def x_range(cls, *args):
        min_ = float('inf')
        max_ = float('-inf')
        for wave in args:
            min_ = min(min_, min(wave.domain))
            max_ = max(max_, max(wave.domain))
        return [min_, max_]

    @classmethod
    def y_range(cls, *args, spacing=1):
        if type(spacing) == type(2) or type(spacing) == type(2.):
            spacing = (spacing, spacing)
        min_ = float('inf')
        max_ = float('-inf')
        for wave in args:
            min_ = min(min_, min(wave.values))
            max_ = max(max_, max(wave.values))
        return [min_ - spacing[1], max_ + spacing[0]]


    def __add__(self, other_wave):
        if other_wave.fs != self.fs:
            raise Exception('fs values must be the same in order to multiplicate waves')
        if(len(other_wave.domain) > len(self.domain)):
            longer_wave = other_wave
            shorter_wave = self
        else:
            longer_wave = self
            shorter_wave = other_wave
        new_values = deepcopy(longer_wave.values)
        for index, value in enumerate(shorter_wave.values):
            new_values[index] += value
        return self.__class__(new_values, longer_wave.domain, self.fs)

    def __mul__(self, other_wave):
        if other_wave.fs != self.fs:
            raise Exception('fs values must be the same in order to multiplicate waves')
        if(len(other_wave.domain) > len(self.domain)):
            longer_wave = other_wave
            shorter_wave = self
        else:
            longer_wave = self
            shorter_wave = other_wave
        new_values = deepcopy(longer_wave.values)
        for index, value in enumerate(shorter_wave.values):
            new_values[index] *= value
        return self.__class__(new_values, longer_wave.domain, self.fs)

    @classmethod
    def sine(cls, amp, freq, phi=0, duration=DEFAULT_DURATION, fs=DEFAULT_FS, label=None, autolabel=False, label_prefix=''):
        values = []
        domain = []
        for t in range(int((duration * fs) + 1)):
            domain.append(t / fs)
            values.append(amp * sin(freq * t / fs + phi))
        new_wave = cls(values, domain, fs)
        new_wave.amp = amp
        new_wave.freq = freq
        new_wave.phi = phi
        new_wave.duration = duration
        if autolabel:
            new_wave.label = label_prefix + '$A = {}, f = {}, \\phi = {}$'.format(amp, freq, phi)
        else:
            if label:
                new_wave.label = label_prefix + label
            else:
                new_wave.label = None
        return new_wave

    def freq_spectrum(self, use_fft=True):
        if use_fft:
            transform = fft(self.values)
        else:
            N = len(self.values)
            transform = zeros(N, dtype=complex)
            for m in range(self.fs):
                sum = 0
                for n in range(N):
                    inner = -(2 * pi * n * m) / N
                    sum += self.values[n] * (cos(inner) + 1j * sin(inner))
                transform[m] = sum
        transform_abs = [abs(x) for x in transform]
        N = len(transform_abs)
        values = [transform_abs[f] / self.fs / pi for f in range(int(self.fs / 2))]
        values = [val for val in values if val > 1e-15]
        return self.__class__(values)

    def amplitude_modulation(self, carrier):
        values = []
        domain = deepcopy(self.domain)
        for t in range(len(self.values)):
            values.append((carrier.amp + self.values[t]) * sin(carrier.freq * t / self.fs + carrier.phi))
        return self.__class__(values, domain, self.fs)

    def frequency_modulation(self, carrier):
        values = []
        domain = deepcopy(self.domain)
        for t in range(len(self.values)):
            values.append(carrier.amp * sin((carrier.freq + self.values[t]) * t / self.fs + carrier.phi))
        return self.__class__(values, domain, self.fs)

    def phase_modulation(self, carrier):
        values = []
        domain = deepcopy(self.domain)
        for t in range(len(self.values)):
            values.append(carrier.amp * sin(carrier.freq * t / self.fs + carrier.phi + self.values[t]))
        return self.__class__(values, domain, self.fs)

    @classmethod
    def square(cls, digital_values, tick_duration=DEFAULT_DURATION, fs=DEFAULT_FS, label=None, autolabel=False, label_prefix=''):
        values = []
        domain = []
        value_length = int(tick_duration * fs)
        for index, value in enumerate(digital_values):
            for pos in range(value_length):
                domain.append((value_length * index + pos) / fs)
                values.append(digital_values[index])
        new_wave = cls(values, domain, fs)
        new_wave.tick_duration = tick_duration
        new_wave.duration = tick_duration * len(digital_values)
        if autolabel:
            new_wave.label = label_prefix + str(digital_values)
        else:
            if label:
                new_wave.label = label_prefix + label
            else:
                new_wave.label = None
        return new_wave

    def amplitude_shift_keying(self, wave):
        values = []
        domain = deepcopy(self.domain)
        for t, value in enumerate(self.values):
            values.append(wave.values[t] * value)
        return self.__class__(values, domain, self.fs)

    def frequency_shift_keying(self, wave, logical_zero_freq_divider=2):
        values = []
        domain = deepcopy(self.domain)
        ones_wave = wave
        zeros_wave = Wave.sine(
            amp=wave.amp, freq=wave.freq/logical_zero_freq_divider,
            phi=wave.phi, duration=(len(wave.values) / wave.fs), fs=wave.fs
        )
        for t, value in enumerate(self.values):
            if self.values[t] == 1:
                values.append(ones_wave.values[t])
            else:
                values.append(zeros_wave.values[t])
        return self.__class__(values, domain, self.fs)

    def phase_shift_keying(self, wave):
        values = []
        domain = deepcopy(self.domain)
        zeros_wave = Wave.sine(
            amp=wave.amp, freq=wave.freq,
            phi=wave.phi + pi, duration=(len(wave.values) / wave.fs), fs=wave.fs
        )
        ones_wave = wave
        for t, value in enumerate(self.values):
            if self.values[t] == 1:
                values.append(ones_wave.values[t])
            else:
                values.append(zeros_wave.values[t])
        return self.__class__(values, domain, self.fs)

    def amplitude_shift_demodulation(self, amp, tick_duration=DEFAULT_DURATION, fs=DEFAULT_FS):
        digital_values = []
        abs_values = [abs(x) for x in self.values]
        value_length = int(tick_duration * fs)
        for offset in range(0, len(abs_values), value_length):
            sum_value = 0
            for inner_offset in range(value_length):
                sum_value += abs_values[offset + inner_offset]
            if sum_value >= amp * 0.8:
                digital_values.append(1)
            else:
                digital_values.append(0)
        return digital_values

    def frequency_shift_demodulation(self, wave, tick_duration=DEFAULT_DURATION, fs=DEFAULT_FS):
        digital_values = []
        values = (self * wave).values[:len(self.values)]
        value_length = int(tick_duration * fs)
        for offset in range(0, len(values), value_length):
            if offset + value_length > len(values):
                break
            sum_value = 0
            for inner_offset in range(value_length):
                sum_value += values[offset + inner_offset]
            if sum_value >= wave.amp * 0.8:
                digital_values.append(1)
            else:
                digital_values.append(0)
        return digital_values

    def phase_shift_demodulation(self, wave, tick_duration=DEFAULT_DURATION, fs=DEFAULT_FS):
        digital_values = []
        values = (self * wave).values[:len(self.values)]
        value_length = int(tick_duration * fs)
        for offset in range(0, len(values), value_length):
            if offset + value_length > len(values):
                break
            sum_value = 0
            for inner_offset in range(value_length):
                sum_value += values[offset + inner_offset]
            if sum_value >= wave.amp * 0.8:
                digital_values.append(1)
            else:
                digital_values.append(0)
        return digital_values
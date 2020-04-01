#!/usr/bin/env python
# encoding: utf-8

# Jakub Młokosiewicz, 2015

from matplotlib import rc
from matplotlib.pyplot import *
from math import pi
from matplotlib.backends.backend_pdf import PdfPages

from mysignalslib import Wave
from waveplothelper import multiplot

rc('figure', figsize=(8.27, 11.7), dpi=100)
rc('savefig', bbox='tight')
rc('legend', fontsize=10, fancybox=True)
rc('text', usetex=True)
rc('text.latex', preamble=r'\usepackage[T1]{polski}')

pdf_pages = PdfPages('pdf/lab5.pdf')

###

figure()
text(0.05, 0.3, u'{\\textsc {\\huge Sprawozdanie z Przetwarzania Sygnałów}} \\\\\\\\\\\\ {\\Large Demodulacja ASK, FSK, PSK} \\\\\\\\\\\\\\\\ {\\large Wykonał: Jakub Młokosiewicz}', fontsize=12, ha='left', va='top')
axis('off')
tight_layout()
pdf_pages.savefig()

###

signal = Wave.square([1, 0, 0, 1, 1, 0], autolabel=True, label_prefix='Sygnał modulowany: ')
carrier = Wave.sine(amp=3, freq=10, autolabel=True, label_prefix='Fala nośna: ', duration=signal.duration)
modulated_signal = signal.amplitude_shift_keying(carrier)
modulated_signal.label = 'Sygnał zmodulowany'
demodulated_signal = Wave.square(modulated_signal.amplitude_shift_demodulation(amp=3))
demodulated_signal.label = 'Sygnał zdemodulowany'

figure()
suptitle(u'Demodulacja ASK', fontsize=16)
multiplot([modulated_signal], [carrier], [demodulated_signal])
pdf_pages.savefig()

###

signal = Wave.square([1, 0, 0, 1, 1, 0], autolabel=True, label_prefix='Sygnał modulowany: ')
carrier = Wave.sine(amp=3, freq=10, autolabel=True, label_prefix='Fala nośna: ', duration=signal.duration)
modulated_signal = signal.frequency_shift_keying(carrier)
modulated_signal.label = 'Sygnał zmodulowany'
demodulated_signal = Wave.square(modulated_signal.frequency_shift_demodulation(carrier))
demodulated_signal.label = 'Sygnał zdemodulowany'

figure()
suptitle(u'Demodulacja FSK', fontsize=16)
multiplot([modulated_signal], [carrier], [demodulated_signal])
pdf_pages.savefig()

###

signal = Wave.square([1, 0, 0, 1, 1, 0], autolabel=True, label_prefix='Sygnał modulowany: ')
carrier = Wave.sine(amp=3, freq=10, autolabel=True, label_prefix='Fala nośna: ', duration=signal.duration)
modulated_signal = signal.phase_shift_keying(carrier)
modulated_signal.label = 'Sygnał zmodulowany'
demodulated_signal = Wave.square(modulated_signal.phase_shift_demodulation(carrier))
demodulated_signal.label = 'Sygnał zdemodulowany'

figure()
suptitle(u'Demodulacja PSK', fontsize=16)
multiplot([modulated_signal], [carrier], [demodulated_signal])
pdf_pages.savefig()

###

figure()
suptitle(r'\textsc{Podsumowanie}', fontsize=18)
findings = '''
Demodulację ASK zaimplementowałem jako sumowanie kolejnych fragmentów o długości jednej próbki pobieranych z wartości bezwzględnej sygnału. Gdy wartość ta jest większa niż 0.8 amplitudy fali nośnej - algorytm odczytuje próbkę jako logiczne 1, w przeciwnym razie - jako logiczne 0.
Demodulacje FSK oraz PSK udało mi się sprowadzić do postaci, w których można zastosować podobny algorytm zliczania, jak przedstawiony wyżej dla ASK.
I tak - demodulacja FSK polega u mnie na przemnożeniu sygnału demodulowanego przez falę nośną. Otrzymany sygnał demoduluję analogicznie jak ASK.
Demodulowany sygnał PSK również najpierw mnożę przez falę nośną, a następnie demoduluję analogicznie jak ASK.
'''.strip()
text(0, 1, r'\begin{minipage}{7.4 in} \setlength{\parindent}{2em} %s \end{minipage}' % findings.replace('\n', ' \\par '), fontsize=12, va='top')
axis('off')
tight_layout()
subplots_adjust(top=0.95)
pdf_pages.savefig()

###

pdf_pages.close()

# show()
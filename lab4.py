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

pdf_pages = PdfPages('pdf/lab4.pdf')

###

figure()
text(0.05, 0.3, u'{\\textsc {\\huge Sprawozdanie z Przetwarzania Sygnałów}} \\\\\\\\\\\\ {\\Large ASK, FSK, PSK} \\\\\\\\\\\\\\\\ {\\large Wykonał: Jakub Młokosiewicz}', fontsize=12, ha='left', va='top')
axis('off')
tight_layout()
pdf_pages.savefig()

###

signal = Wave.square([1, 0, 0, 1, 1, 0], autolabel=True, label_prefix='Sygnał modulowany: ')
carrier = Wave.sine(amp=3, freq=10, autolabel=True, label_prefix='Fala nośna: ', duration=signal.duration)
modulated_signal = signal.amplitude_shift_keying(carrier)
modulated_signal.label = 'Sygnał zmodulowany'
modulated_signal_spectrum = modulated_signal.amplitude_spectrum()
modulated_signal_spectrum.label = 'Widmo sygnału zmodulowanego'

figure()
suptitle(u'Kluczowanie amplitudy (ASK)', fontsize=16)
multiplot([carrier, signal], [modulated_signal], others=[modulated_signal_spectrum])
pdf_pages.savefig()

###

signal = Wave.square([1, 0, 0, 1, 1, 0], autolabel=True, label_prefix='Sygnał modulowany: ')
carrier = Wave.sine(amp=3, freq=10, autolabel=True, label_prefix='Fala nośna: ', duration=signal.duration)
modulated_signal = signal.frequency_shift_keying(carrier)
modulated_signal.label = 'Sygnał zmodulowany'
modulated_signal_spectrum = modulated_signal.amplitude_spectrum()
modulated_signal_spectrum.label = 'Widmo sygnału zmodulowanego'

figure()
suptitle(u'Cyfrowa modulacja częstotliwości (FSK)', fontsize=16)
multiplot([carrier, signal], [modulated_signal], others=[modulated_signal_spectrum])
pdf_pages.savefig()

###

signal = Wave.square([1, 0, 0, 1, 1, 0], autolabel=True, label_prefix='Sygnał modulowany: ')
carrier = Wave.sine(amp=3, freq=10, autolabel=True, label_prefix='Fala nośna: ', duration=signal.duration)
modulated_signal = signal.phase_shift_keying(carrier)
modulated_signal.label = 'Sygnał zmodulowany'
modulated_signal_spectrum = modulated_signal.amplitude_spectrum()
modulated_signal_spectrum.label = 'Widmo sygnału zmodulowanego'

figure()
suptitle(u'Kluczowanie fazy (PSK)', fontsize=16)
multiplot([carrier, signal], [modulated_signal], others=[modulated_signal_spectrum])
pdf_pages.savefig()

###

figure()
suptitle(r'\textsc{Wnioski}', fontsize=18)
findings = '''
Jak podaje Wikipedia, widmo sygnału zmodulowanego ASK składa się z dwóch części. Za pierwszą część odpowiada składnik harmoniczny, natomiast druga część to widmo sygnału modulującego.
Widmo sygnału zmodulowanego FSK jest podobne do nałożonych na siebie dwóch widm sygnałów zmodulowanych ASK o różnych częstotliwościach nośnych. Szerokość pasma FSK jest nico szersza niż dla ASK.
Widmo sygnału zmodulowanego fazowo również jest podobne do nałożonych dwóch widm sygnałów ASK, jednak dwa szczyty znajdują się bliżej siebie, niż to wygląda w przypadku FSK. PSK zdaje się równiż zajmować nieco większą szerokość pasma niż FSK.
'''.strip()
text(0, 1, r'\begin{minipage}{7.4 in} \setlength{\parindent}{2em} %s \end{minipage}' % findings.replace('\n', ' \\par '), fontsize=12, va='top')
axis('off')
tight_layout()
subplots_adjust(top=0.95)
pdf_pages.savefig()

###

pdf_pages.close()

# show()
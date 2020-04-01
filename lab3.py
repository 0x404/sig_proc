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

pdf_pages = PdfPages('pdf/lab3.pdf')

###

figure()
text(0.05, 0.3, u'{\\textsc {\\huge Sprawozdanie z Przetwarzania Sygnałów}} \\\\\\\\\\\\ {\\Large modulacja ciągła amplitudy (AM), częstotliwości (FM) oraz fazy (PM)} \\\\\\\\\\\\\\\\ {\\large Wykonał: Jakub Młokosiewicz}', fontsize=12, ha='left', va='top')
axis('off')
tight_layout()
pdf_pages.savefig()

###

signal = Wave.sine(amp=5, freq=50, autolabel=True, label_prefix='Sygnał modulowany: ')
carrier = Wave.sine(amp=10, freq=100, autolabel=True, label_prefix='Fala nośna: ')
modulated_signal = signal.amplitude_modulation(carrier)
modulated_signal.label = 'Sygnał zmodulowany'
modulated_signal_spectrum = modulated_signal.amplitude_spectrum()
modulated_signal_spectrum.label = 'Widmo sygnału zmodulowanego'

figure()
suptitle(u'Modulacja amplitudy (AM)', fontsize=16)
multiplot([carrier, signal], [modulated_signal], others=[modulated_signal_spectrum], x_range=[0, pi/2])
pdf_pages.savefig()

###

signal = Wave.sine(amp=2, freq=50, autolabel=True, label_prefix='Sygnał modulowany: ')
carrier = Wave.sine(amp=3, freq=100, autolabel=True, label_prefix='Fala nośna: ')
modulated_signal = signal.frequency_modulation(carrier)
modulated_signal.label = 'Sygnał zmodulowany'
modulated_signal_spectrum = modulated_signal.amplitude_spectrum()
modulated_signal_spectrum.label = 'Widmo sygnału zmodulowanego'

figure()
suptitle(u'Modulacja częstotliwości (FM)', fontsize=16)
multiplot([carrier, signal], [modulated_signal], others=[modulated_signal_spectrum], x_range=[0, pi/2])
pdf_pages.savefig()

###

signal = Wave.sine(amp=1, freq=80, autolabel=True, label_prefix='Sygnał modulowany: ')
carrier = Wave.sine(amp=3, freq=100, autolabel=True, label_prefix='Fala nośna: ')
modulated_signal = signal.phase_modulation(carrier)
modulated_signal.label = 'Sygnał zmodulowany'
modulated_signal_spectrum = modulated_signal.amplitude_spectrum()
modulated_signal_spectrum.label = 'Widmo sygnału zmodulowanego'

figure()
suptitle(u'Modulacja fazy (PM)', fontsize=16)
multiplot([carrier, signal], [modulated_signal], others=[modulated_signal_spectrum], x_range=[0, pi/2])
pdf_pages.savefig()

###

figure()
suptitle(r'\textsc{Wnioski}', fontsize=18)
findings = '''
Na wykresie widma sygnału zmodulowanego amplitudowo możemy zaobserwować, że składa się on, oprócz fali nośnej, również z dwóch dodatkowych fal, zwanych wstęgami bocznymi, odległych częstotliwościowo od fali nośnej o wartość najwyższej częstotliwości w sygnale modulowanym (odpowiednio w kierunku niższych i wyższych częstotliwości). Tak więc szerokość pasma zajmowanego przez sygnał zmodulowany amplitudowo równa jest dwukrotności najwyższej częstotliwości w sygnale modulowanym.
Modulacja częstotliwościowa ma ciekawą cechę - sygnały boczne na widmie rozciągają się w niskończoność (im większa częstotliwość, tym mniejsza wartość amplitudy). Jednak podstawowa (później powtarzana) część widma zajmuje małą szerokość pasma.
Szerokość pasma zajmowanego przez sygnał zmodulowany fazowo to wedle moich doświadczeń, podobnie jak w wypadku AM, dwukrotność największej częstotliwości w sygnale modulowanym.
'''.strip()
text(0, 1, r'\begin{minipage}{7.4 in} \setlength{\parindent}{2em} %s \end{minipage}' % findings.replace('\n', ' \\par '), fontsize=12, va='top')
axis('off')
tight_layout()
subplots_adjust(top=0.95)
pdf_pages.savefig()

###

pdf_pages.close()

# show()
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
rc('text.latex', unicode=True, preamble=r'\usepackage[T1]{polski}')

pdf_pages = PdfPages('pdf/lab2.pdf')

###

figure()
text(0.05, 0.3, u'{\\textsc {\\huge Sprawozdanie z Przetwarzania Sygnałów}} \\\\\\\\\\\\ {\\Large reprezentacja sygnałów w dziedzinie czasu i częstotliwości} \\\\\\\\\\\\\\\\ {\\large Wykonał: Jakub Młokosiewicz}', fontsize=12, ha='left', va='top')
axis('off')
tight_layout()
pdf_pages.savefig()

###

sinus = Wave.sine(amp=5, freq=50, phi=0, autolabel=True)
sinus_spectrum = sinus.amplitude_spectrum()
sinus_spectrum.label = 'Sinus w dziedzinie częstotliwości'

figure()
suptitle(u'Reprezentacja pojedynczej fali sinusoidalnej w dziedzinie czasu i częstotliwości', fontsize=16)
multiplot([sinus], others=[sinus_spectrum], x_range=[0, pi/2])
pdf_pages.savefig()

###

sinus_1 = Wave.sine(amp=2, freq=80, phi=0, autolabel=True)
sinus_2 = Wave.sine(amp=5, freq=120, phi=0, autolabel=True)
sinus_sum = sinus_1 + sinus_2
sinus_sum.label = u'Suma powyższych sygnałów'
sum_spectrum = sinus_sum.amplitude_spectrum()
sum_spectrum.label = u'Widmo częstotliwościowe sumy sygnałów'

figure()
suptitle(u'Suma dwóch fal sinusoidalnych', fontsize=16)
multiplot([sinus_1, sinus_2], [sinus_sum], others=[sum_spectrum], x_range=[0, pi/2])
pdf_pages.savefig()

###

sinus_1 = Wave.sine(amp=10, freq=10, phi=0, autolabel=True)
sinus_2 = Wave.sine(amp=6, freq=50, phi=0, autolabel=True)
sinus_3 = Wave.sine(amp=3, freq=120, phi=pi/2, autolabel=True)
sinus_sum = sinus_1 + sinus_2 + sinus_3
sinus_sum.label = u'Suma powyższych sygnałów'
sum_spectrum = sinus_sum.amplitude_spectrum()
sum_spectrum.label = u'Widmo częstotliwościowe sumy sygnałów'

figure()
suptitle(u'Suma trzech fal sinusoidalnych, w tym jednej przesuniętej w fazie', fontsize=16)
multiplot([sinus_1, sinus_2, sinus_3], [sinus_sum], others=[sum_spectrum], x_range=[0, pi/2])
pdf_pages.savefig()

###

square = Wave.square([0, 1, 0, 1, 0, 1], tick_duration=pi/2, label='[0, 1, 0, 1, 0, 1]')
square_spectrum = square.amplitude_spectrum()
square_spectrum.label = 'Widmo sygnału'

figure()
suptitle(u'Reprezentacja fali prostokątnej w dziedzinie czasu i częstotliwości', fontsize=16)
multiplot([square], others=[square_spectrum])
pdf_pages.savefig()

###

figure()
suptitle(r'\textsc{Wnioski}', fontsize=18)
findings = '''
Do przedstawiania sygnałów w dziedzinie częstotliwości służy transformata DFT lub jej szybszy odpowiednik - FFT. Po odpowiednim wyskalowaniu osi, na wykresie wspomnianej transformaty sygnału na osi OX będziemy mogli odczytać częstotliwość składowej sinusoidalnej sygnału, natomiast na osi OY - amplitudę tej składowej.
Na wykresie sygnału w dziedzinie częstotliwości dla każdej częstotliwości składowej sumy sygnałów możemy zaobserwować "prążek" o wartości równej amplitudzie tej składowej.
Przesnięcie fazowe składowej sygnału nie ma wpływu na widmo amplitudowe uzyskane z transformaty DFT/FFT (nie zaobserwowałem zależności).
Fala prostokątna w dziedzinie częstotliwości objawia się jako suma wielu fal sinusoidalnych.
'''.strip()
text(0, 1, r'\begin{minipage}{7.4 in} \setlength{\parindent}{2em} %s \end{minipage}' % findings.replace('\n', ' \\par '), fontsize=12, va='top')
axis('off')
tight_layout()
subplots_adjust(top=0.95)
pdf_pages.savefig()

###

pdf_pages.close()

# show()
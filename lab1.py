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

pdf_pages = PdfPages('pdf/lab1.pdf')

###

figure()
text(0.05, 0.3, u'{\\textsc {\\huge Sprawozdanie z Przetwarzania Sygnałów}} \\\\\\\\\\\\ {\\Large dodawanie i mnożenie sygnałów sinusoidalnych} \\\\\\\\\\\\\\\\ {\\large Wykonał: Jakub Młokosiewicz}', fontsize=12, ha='left', va='top')
axis('off')
tight_layout()
pdf_pages.savefig()

###

sinus_1 = Wave.sine(amp=2, freq=8, phi=0, autolabel=True)
sinus_2 = Wave.sine(amp=3, freq=8, phi=0, autolabel=True)
sinus_sum = sinus_1 + sinus_2
sinus_sum.label = u'Suma powyższych sygnałów'
sinus_mult = sinus_1 * sinus_2
sinus_mult.label = u'Iloczyn powyższych sygnałów'

figure()
suptitle(u'Sygnały o zgodnej częstotliwości i fazie', fontsize=16)
multiplot([sinus_1, sinus_2], [sinus_sum], [sinus_mult])
pdf_pages.savefig()

###

sinus_1 = Wave.sine(amp=3, freq=5, phi=0, autolabel=True)
sinus_2 = Wave.sine(amp=3, freq=20, phi=0, autolabel=True)
sinus_sum = sinus_1 + sinus_2
sinus_sum.label = u'Suma powyższych sygnałów'
sinus_mult = sinus_1 * sinus_2
sinus_mult.label = u'Iloczyn powyższych sygnałów'

figure()
suptitle(u'Sygnały o zgodnej amplitudzie i fazie', fontsize=16)
multiplot([sinus_1, sinus_2], [sinus_sum], [sinus_mult])
pdf_pages.savefig()

###

sinus_1 = Wave.sine(amp=3, freq=5, phi=0, autolabel=True)
sinus_2 = Wave.sine(amp=3, freq=5, phi=pi, label='$A = 3, f = 5, \\phi = \\pi$')
sinus_sum = sinus_1 + sinus_2
sinus_sum.label = u'Suma powyższych sygnałów'
sinus_mult = sinus_1 * sinus_2
sinus_mult.label = u'Iloczyn powyższych sygnałów'

figure()
suptitle(u'Sygnały o zgodnej amplitudzie i fazie', fontsize=16)
multiplot([sinus_1, sinus_2], [sinus_sum], [sinus_mult])
pdf_pages.savefig()

###

figure()
suptitle(r'\textsc{Wnioski}', fontsize=18)
findings = '''
W przypadku, gdy oba sygnały mają taką samą częstitliwość i fazę, amplituda sumy tych sygnałów jest sumą amplitud sygnałów składowych; gdy bierzemy pod uwagę iloczyn, maksymalne odchylenie od stanu zero to iloczyn amplitud sygnałów źródłowych. Warto również zauważyć brak wartości ujemnych na wykresie iloczynu sygnałów.
W przypadku, gdy oba sygnały mają tę samą amplitudę i fazę, na wykresie sumy sygnałów sygnał o mniejszej częstotliwości wygląda jakby był osią sygnału wynikowego, nastomiast odchylenia od tej osi przedstawiają zmienność sygnału o większej częstotliwości.
Zsumowanie dwóch sygnałów o tych samych częstotliwościach i amplitudach, przesuniętych względem siebie o $\\pi$ daje efekt wygaszenia. Wykres iloczynu tych sygnałów wygląda jak wykres sygnałów o wspólnej amplitudzie, częstotliwości i fazie, jednak odbity względem osi OX.
'''.strip()
# \begin{minipage}[pos][height][contentpos]{width} text \end{minipage}
text(0, 1, r'\begin{minipage}{7.4 in} \setlength{\parindent}{2em} %s \end{minipage}' % findings.replace('\n', ' \\par '), fontsize=12, va='top')
axis('off')
tight_layout()
subplots_adjust(top=0.95)
pdf_pages.savefig()

###

pdf_pages.close()

# show()
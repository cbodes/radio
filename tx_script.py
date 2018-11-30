from gnuradio import gr
from MyRadio import cdmagen, cdmarx, rrc_filter, cpfsk, freq_calc, phase_calc
from gnuradio import blocks

import matplotlib.pyplot as plt
import numpy as np
from time import sleep
from MessageGen import MessageGen
import osmosdr
from scipy.fftpack import fft, fftfreq, fftshift
from PyQt5 import QtGui, QtWidgets
from gnuradio import qtgui
from gnuradio import filter
import sys
import sip


class MyRadio (gr.top_block):
    def __init__(self):
        gr.top_block .__init__(self, "TEST")

        bitstream = [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1]
        self.bitstream = bitstream
        self.cdma_code = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.sample_rate = 10e6
        self.bit_width = .001
        self.freq_1 = 1 / self.bit_width * 50
        self.freq_0 = 1 / self.bit_width * 1
        self.bandwidth = self.freq_1 - self.freq_0
        self.rf_fc = 915e6-self.freq_0
        self.bit_samps = int(self.bit_width * self.sample_rate)

        self.samples_per_symbol = self.bit_width * self.sample_rate

        self.msg_gen = MessageGen(self.cdma_code)
        self.encoded_data = self.msg_gen.gen_message_from_raw(self.bitstream)

        self.rrc_taps = filter.firdes.root_raised_cosine(
            self.samples_per_symbol, self.samples_per_symbol, 1, .5, int(20 * self.samples_per_symbol))

        self.rrc_filt = filter.interp_fir_filter_fff(
            int(self.samples_per_symbol), self.rrc_taps)

        self.short_to_float = blocks.short_to_float()

        self.sdr_sink = osmosdr.sink(
            args="hackrf=0000000000000000325866e629758723")
        self.sdr_sink.set_sample_rate(self.sample_rate)
        self.sdr_sink.set_center_freq(self.rf_fc)
        self.sdr_sink.set_gain(14, 0)
        self.sdr_sink.set_if_gain(47, 0)

        self.file_sink = blocks.file_sink(8, "output.txt")

        self.repeater = blocks.repeat(2, self.bit_samps)

        self.vec_source = blocks.vector_source_s(
            data=self.encoded_data, repeat=True, vlen=len(self.encoded_data))

        self.vec_stream = blocks.vector_to_stream(2, len(self.encoded_data))

        self.cpfsk_mod = cpfsk(self.sample_rate)

        self.thr = blocks.throttle(gr.sizeof_gr_complex, self.sample_rate)

        self.conv = blocks.complex_to_float()

        self.freq_calc = freq_calc(self.freq_1, self.freq_0)

        self.phase_calc = phase_calc(self.sample_rate)

        Rs = 1
        fftsize = 2048
        self.qapp = QtWidgets.QApplication(sys.argv)
        self.qtsnk = qtgui.sink_c(fftsize, 5, self.rf_fc, self.bandwidth * 2, "Complex Signal Example",
                                  True, True, True, True)

        self.time_sink = qtgui.time_sink_c(2000, self.sample_rate, "Time")

        self.connect(self.vec_source, self.vec_stream)
        self.connect(self.vec_stream, self.repeater)
        self.connect(self.repeater, self.freq_calc)
        self.connect(self.freq_calc, self.cpfsk_mod)
        self.connect(self.cpfsk_mod, self.thr)
        self.connect(self.thr, self.time_sink)
        self.connect(self.thr, self.qtsnk)
        self.connect(self.thr, self.sdr_sink)

        pyWin1 = sip.wrapinstance(self.qtsnk.pyqwidget(), QtWidgets.QWidget)
        pyWin1.show()
        pyWin2 = sip.wrapinstance(
            self.time_sink.pyqwidget(), QtWidgets.QWidget)
        pyWin2.show()

    def getResultData(self):
        return self.encoded_data


if __name__ == '__main__':
    test = MyRadio()
    edges = test.edge_list()
    test.start()
    test.qapp.exec_()
    test.stop()
    test.wait()

    # data = test.getResultData()
    # print len(test.cpfsk_mod.data)
    # print len(data)
    # N = len(data)
    # T = test.bit_width * len(test.bitstream) * 32 / len(data)
    # plt.plot(test.cpfsk_mod.data)
    # plt.plot(data)
    # plt.show()
    # yf = fft(data)
    # xf = fftfreq(N, T)
    # xf = fftshift(xf)
    # yplot = fftshift(yf)
    # plt.plot(xf, 1.0/N * np.abs(yplot))
    # plt.grid()
    # # plt.show()

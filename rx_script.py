from gnuradio import gr
from MyRadio import cdmarx, fm_sum, fm_demod, fm_square, fm_compare, cdma_decode
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
from gnuradio import analog
import sys
import sip


class MyRadio (gr.top_block):
    def __init__(self):
        gr.top_block .__init__(self, "TEST")

        bitstream = [1, 0, 1, 1, 0, 1]
        self.bitstream = bitstream
        self.cdma_code = [1, 1, -1, -1, -1, -1, -1, -1, 1, 1, -1, -1, -1, -1, -
                          1, -1, 1, 1, -1, -1, -1, -1, -1, -1, 1, 1, -1, -1, -1, -1, -1, -1]
        self.sample_rate = 5000000
        self.center_f = 100e6
        self.bandwidth = 10000
        self.freq_1 = 1000
        self.freq_0 = 500
        self.bit_width = .001
        self.mod_rate = 500e3
        self.samples_per_symbol = self.mod_rate * self.bit_width

        fftsize = 2048
        self.qapp = QtWidgets.QApplication(sys.argv)
        self.qtsnk = qtgui.sink_c(fftsize, 5, self.center_f, self.bandwidth * 2, "Complex Signal Example",
                                  True, True, True, True)

        self.time_sink = qtgui.time_sink_c(2000, self.sample_rate, "Time")

        self.lp_taps1 = filter.firdes.low_pass(
            20, self.sample_rate,  self.bandwidth,  10000)

        self.lp_filt1 = filter.fir_filter_ccf(
            int(self.sample_rate / self.mod_rate), self.lp_taps1)

        self.rx_test = cdmarx()

        self.sdr_source = osmosdr.source(
            args="hackrf=0000000000000000325866e6299d8023")
        self.sdr_source.set_sample_rate(self.sample_rate)
        self.sdr_source.set_center_freq(self.center_f)
        self.sdr_source.set_freq_corr(0, 0)
        self.sdr_source.set_dc_offset_mode(0, 0)
        self.sdr_source.set_iq_balance_mode(0, 0)
        self.sdr_source.set_gain_mode(False, 0)
        self.sdr_source.set_gain(10, 0)
        self.sdr_source.set_if_gain(20, 0)
        self.sdr_source.set_bb_gain(20, 0)
        self.sdr_source.set_antenna("", 0)
        self.sdr_source.set_bandwidth(0, 0)

        self.fm_demod = fm_demod(
            self.mod_rate, self.samples_per_symbol, self.freq_1, self.freq_0)

        self.fm_sum = fm_sum(self.samples_per_symbol)

        self.fm_square = fm_square()

        self.fm_compare = fm_compare()

        self.cdma_vecstack = blocks.stream_to_vector(1, len(self.cdma_code))

        self.cdma_decode = cdma_decode(self.cdma_code)

        self.connect(self.sdr_source, self.qtsnk)
        self.connect(self.sdr_source, self.lp_filt1)
        self.connect(self.lp_filt1, self.fm_demod)
        for i in np.arange(0, 4, 1):
            self.connect((self.fm_demod, i), (self.fm_sum, i))
            self.connect((self.fm_sum, i), (self.fm_square, i))

        self.connect((self.fm_square, 0), (self.fm_compare, 0))
        self.connect((self.fm_square, 1), (self.fm_compare, 1))
        self.connect(self.fm_compare, self.cdma_vecstack)
        self.connect(self.cdma_vecstack, self.cdma_decode)
        self.connect(self.cdma_decode, self.rx_test)

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

    # plt.plot(test.cpfsk_mod.data[:10000])
    # # plt.plot(data)
    # plt.show()
    # yf = fft(data)
    # xf = fftfreq(N, T)
    # xf = fftshift(xf)
    # yplot = fftshift(yf)
    # plt.plot(xf, 1.0/N * np.abs(yplot))
    # plt.grid()
    # # plt.show()

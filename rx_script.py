from gnuradio import gr
from MyRadio import cdmarx, fm_sum, fm_demod, fm_square, fm_compare, cdma_decode, fm_multiply
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
    def __init__(self, cdma_length):
        gr.top_block .__init__(self, "TEST")
        self.expected = [0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1]
        self.packet_header = [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1]
        self.cdma_code = np.repeat(1, cdma_length)
        self.sample_rate = 20e6
        self.bit_width = .001
        self.freq_1 = 1 / self.bit_width * 50
        self.freq_0 = 1 / self.bit_width * 1
        self.bandwidth = self.freq_1 - self.freq_0
        self.mod_fc = self.bandwidth
        self.rf_fc = 915e6-self.freq_0
        self.mod_rate = 1e6
        self.samples_per_symbol = int(self.mod_rate * self.bit_width)

        fftsize = 2048
        self.qapp = QtWidgets.QApplication(sys.argv)
        self.qtsnk = qtgui.sink_c(fftsize, 5, 0, self.mod_rate, "Receiver Plots",
                                  True, True, True, True)

        self.conv = blocks.complex_to_float()

        self.time_sink = qtgui.time_sink_c(2000, self.sample_rate, "Time")

        self.lp_taps1 = filter.firdes.low_pass(
            10, self.sample_rate,  self.freq_1,  10000)

        self.lp_filt1 = filter.fir_filter_ccf(
            int(self.sample_rate / self.mod_rate), self.lp_taps1)


        self.lp_taps2 = filter.firdes.low_pass(
            0, self.mod_rate,  self.freq_1,  1000)

        self.lp_filt2 = filter.fir_filter_ccf(
            1, self.lp_taps2)

        self.rx_test = cdmarx(self.packet_header, self.expected)

        self.sdr_source = osmosdr.source(
            args="hackrf=0000000000000000325866e6299d8023")
        self.sdr_source.set_sample_rate(self.sample_rate)
        self.sdr_source.set_center_freq(self.rf_fc)
        self.sdr_source.set_freq_corr(0, 0)
        self.sdr_source.set_dc_offset_mode(0, 0)
        self.sdr_source.set_iq_balance_mode(0, 0)
        self.sdr_source.set_gain_mode(False, 0)
        self.sdr_source.set_gain(14, 0)
        self.sdr_source.set_if_gain(47, 0)
        self.sdr_source.set_bb_gain(20, 0)
        self.sdr_source.set_antenna("", 0)
        self.sdr_source.set_bandwidth(0, 0)


        self.fm_multiplyr1 = fm_multiply(self.mod_rate, self.freq_1, True)
        self.fm_multiplyi1 = fm_multiply(self.mod_rate, self.freq_1, False)
        self.fm_multiplyr0 = fm_multiply(self.mod_rate, self.freq_0, True)
        self.fm_multiplyi0 = fm_multiply(self.mod_rate, self.freq_0, False)

        self.fm_sum1a = fm_sum(self.samples_per_symbol)
        self.fm_sum1b = fm_sum(self.samples_per_symbol)
        self.fm_sum0a = fm_sum(self.samples_per_symbol)
        self.fm_sum0b = fm_sum(self.samples_per_symbol)

        self.fm_square = fm_square()

        self.fm_compare = fm_compare()

        self.cdma_vecstack = blocks.stream_to_vector(1, len(self.cdma_code))

        self.sumstack1a = blocks.stream_to_vector(4, self.samples_per_symbol)
        self.sumstack1b = blocks.stream_to_vector(4, self.samples_per_symbol)
        self.sumstack0a = blocks.stream_to_vector(4, self.samples_per_symbol)
        self.sumstack0b = blocks.stream_to_vector(4, self.samples_per_symbol)

        self.dataStack = blocks.stream_to_vector(1, 5)

        self.cdma_decode = cdma_decode(self.cdma_code)

        self.connect(self.sdr_source, self.lp_filt1)
        self.connect(self.lp_filt1, self.conv)
        self.connect(self.lp_filt1, self.qtsnk)
        self.connect((self.conv, 0), self.fm_multiplyr1)
        self.connect((self.conv, 1), self.fm_multiplyi1)
        self.connect((self.conv, 0), self.fm_multiplyr0)
        self.connect((self.conv, 1), self.fm_multiplyi0)
        self.connect(self.fm_multiplyr1, self.sumstack1a)
        self.connect(self.fm_multiplyi1, self.sumstack1b)
        self.connect(self.fm_multiplyr0, self.sumstack0a)
        self.connect(self.fm_multiplyi0, self.sumstack0b)
        self.connect(self.sumstack1a, self.fm_sum1a)
        self.connect(self.sumstack1b, self.fm_sum1b)
        self.connect(self.sumstack0a, self.fm_sum0a)
        self.connect(self.sumstack0b, self.fm_sum0b)
        self.connect(self.fm_sum1a, (self.fm_square, 0))
        self.connect(self.fm_sum1b, (self.fm_square, 1))
        self.connect(self.fm_sum0a, (self.fm_square, 2))
        self.connect(self.fm_sum0b, (self.fm_square, 3))
        self.connect((self.fm_square, 0), (self.fm_compare, 0))
        self.connect((self.fm_square, 1), (self.fm_compare, 1))
        self.connect(self.fm_compare, self.cdma_vecstack)
        self.connect(self.cdma_vecstack, self.cdma_decode)
        self.connect(self.cdma_decode, self.rx_test)

        pyWin1 = sip.wrapinstance(self.qtsnk.pyqwidget(), QtWidgets.QWidget)
        pyWin1.show()
        # pyWin2 = sip.wrapinstance(
        #     self.time_sink.pyqwidget(), QtWidgets.QWidget)
        # pyWin2.show()

    def getResultData(self):
        return self.encoded_data


if __name__ == '__main__':
    test = MyRadio(int(sys.argv[1]))
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

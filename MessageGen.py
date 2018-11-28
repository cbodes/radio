#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 <+YOU OR YOUR COMPANY+>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy as np
from gnuradio import gr


class MessageGen:
    """
    docstring for block rrc_filter
    """
    stackedData = []
    curBit = 1
    samplesPerBit = 0
    pulseTime = 0
    numBits = 32
    pulseTime = []
    rrcTransfer = []
    filteredData = []
    totalSamples = 0
    data = []

    def __init__(self, cdmaCode):
        #     self.numBits = dataLength
        #     self.dataLength = dataLength
        #     self.pulseTime = []
        #     self.samplesPerBit = int(sample_rate * bit_width)
        #     self.totalSamples = int(self.samplesPerBit * self.numBits)
        self.stackedData = np.array([])

        self.myCdmaCode = np.array(cdmaCode)

        # t = -2 * bit_width * self.numBits

        # while t <= 2*bit_width*self.numBits:
        #     self.pulseTime.append(t)
        #     t += bit_width / self.samplesPerBit

        # self.rrcTransfer = np.array([])
        # for t in self.pulseTime:
        #     if t == 0:
        #         A = (1/bit_width) * (1 + beta_value*(4/np.pi - 1))
        #     elif abs(t) == bit_width/(4*beta_value):
        #         A = (beta_value/(bit_width * np.sqrt(2)))*((1 + 2 / np.pi) *
        #                                                    np.sin(np.pi/(4*beta_value)) + (1 - 2 / np.pi)*np.cos(np.pi/(4*beta_value)))
        #     else:
        #         A = (np.sin((np.pi * t / bit_width) * (1 - beta_value)) + 4 * t * beta_value / bit_width *
        #              np.cos(np.pi * t / bit_width * (1 + beta_value))) / (np.pi * t * (1 - (4 * beta_value * t / bit_width)**2))
        #     self.rrcTransfer = np.append(self.rrcTransfer, A*bit_width)

    def gen_message_from_raw(self, bits):
        bits = np.array(bits)
        return self.cdma_encode_data(bits)

    def cdma_encode_data(self, bits):
        encoded = np.array([], dtype=np.int16)
        for bit in bits:
            encoded = np.concatenate((encoded, (bit * 2 - 1) * self.myCdmaCode))
        return encoded

    def filter_data(self, bits):

        filteredData = np.zeros(self.totalSamples)
        startIDX = int(len(self.rrcTransfer) / 2 - self.samplesPerBit / 2)
        for bit in bits:
            a = np.multiply(bit, self.rrcTransfer[startIDX:startIDX + self.totalSamples])
            filteredData = np.add(filteredData, a)
            startIDX -= self.samplesPerBit

        return filteredData


if __name__ == '__main__':
    cdma_code = [1, 1, -1, -1, -1, -1, -1, -1, 1, 1, -1, -1, -1, -1, -
                 1, -1, 1, 1, -1, -1, -1, -1, -1, -1, 1, 1, -1, -1, -1, -1, -1, -1]
    bitstream = [1, 0, 0, 1, 0, 1]
    gen = MessageGen(500000, .0001, 1, len(bitstream), cdma_code)
    print gen.gen_message_from_raw(bitstream)

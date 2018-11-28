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


class rrc_filter(gr.basic_block):
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

    def __init__(self, sample_rate, bit_width, beta_value, dataLength):
        gr.basic_block.__init__(self,
                                name="rrc_filter",
                                in_sig=[(np.int8, 32)],
                                out_sig=[(np.float32, 32 * dataLength)])
        self.numBits = 32 * dataLength
        self.dataLength = dataLength
        self.pulseTime = []
        self.samplesPerBit = int(sample_rate * bit_width)
        self.totalSamples = int(self.samplesPerBit * self.numBits)
        self.stackedData = np.array([])
        self.set_min_output_buffer(2**20)

        t = -2 * bit_width * self.numBits

        while t <= 2*bit_width*self.numBits:
            self.pulseTime.append(t)
            t += bit_width / self.samplesPerBit

        self.rrcTransfer = np.array([])
        for t in self.pulseTime:
            if t == 0:
                A = (1/bit_width) * (1 + beta_value*(4/np.pi - 1))
            elif abs(t) == bit_width/(4*beta_value):
                A = (beta_value/(bit_width * np.sqrt(2)))*((1 + 2 / np.pi) *
                                                           np.sin(np.pi/(4*beta_value)) + (1 - 2 / np.pi)*np.cos(np.pi/(4*beta_value)))
            else:
                A = (np.sin((np.pi * t / bit_width) * (1 - beta_value)) + 4 * t * beta_value / bit_width *
                     np.cos(np.pi * t / bit_width * (1 + beta_value))) / (np.pi * t * (1 - (4 * beta_value * t / bit_width)**2))
            self.rrcTransfer = np.append(self.rrcTransfer, A*bit_width)

    def forecast(self, noutput_items, ninput_items_required):
        # setup size of input_items[i] for work call
        #print ninput_items_required
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = 1

    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        #print "New input: \n", in0[0]
        #print "RRC_FILT NEW INPUT: ", in0[0]
        if len(in0) == 0:
            print "Zero Length input!"
            return 0
        self.stackedData = np.concatenate((self.stackedData, in0[0]))

        if (self.curBit < self.dataLength):
            self.curBit += 1
            self.consume(0, 1)
            return 0
        #print "FULL DATA", self.stackedData
        filteredData = np.zeros(self.totalSamples)
        startIDX = int(len(self.rrcTransfer) / 2 - self.samplesPerBit / 2)
        for bit in self.stackedData:
            a = np.multiply(bit, self.rrcTransfer[startIDX:startIDX + self.totalSamples])
            filteredData = np.add(filteredData, a)
            startIDX -= self.samplesPerBit

        self.data = np.concatenate((self.data, filteredData))
        self.consume(0, 1)
        i = 0
        f = 0
        while i < len(self.data):
            output_items[0][f] = self.data[i:i+len(output_items[0][f])]
            f += 1
            i += len(output_items[0][f])
        return 1

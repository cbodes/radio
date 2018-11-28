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


class fm_demod(gr.basic_block):
    """
    docstring for block fm_demod
    """

    def __init__(self, sample_rate, samples_per_symbol, w_upper, w_lower):
        gr.basic_block.__init__(self,
                                name="fm_demod",
                                in_sig=[np.complex64],
                                out_sig=[np.float32, np.float32, np.float32, np.float32])
        self.cur_i = 0
        self.w_1 = w_upper * 2 * np.pi
        self.w_0 = w_lower * 2 * np.pi
        self.samples_per_symbol = samples_per_symbol
        self.num_samps = 2**14

        t = np.arange(0, self.num_samps * 1. / sample_rate, 1. / sample_rate)

        self.cos_1 = np.cos(self.w_1 * t)
        self.sin_1 = np.sin(self.w_1 * t)
        self.cos_0 = np.cos(self.w_0 * t)
        self.sin_0 = np.sin(self.w_0 * t)

    def forecast(self, noutput_items, ninput_items_required):
        # setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):

        in0 = input_items[0][:]
        self.consume(0, len(output_items[0]))

        output_items[0][:] = np.multiply(in0.real, self.cos_0[:len(in0)])[:len(output_items[0])]
        output_items[1][:] = np.multiply(in0.imag, self.sin_0[:len(in0)])[:len(output_items[0])]
        output_items[2][:] = np.multiply(in0.real, self.cos_1[:len(in0)])[:len(output_items[0])]
        output_items[3][:] = np.multiply(in0.imag, self.sin_1[:len(in0)])[:len(output_items[0])]

        return len(output_items[0])

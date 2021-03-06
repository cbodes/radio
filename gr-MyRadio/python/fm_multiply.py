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


class fm_multiply(gr.basic_block):
    """
    docstring for block fm_demod
    """

    def __init__(self, sample_rate, f, real):
        gr.basic_block.__init__(self,
                                name="fm_demod",
                                in_sig=[np.float32],
                                out_sig=[np.float32])
        self.num_samps = 2**14
        self.w = 2 * np.pi * f
        self.tstep = 1. / sample_rate
        self.t = np.arange(0, self.num_samps * 1. / sample_rate, 1. / sample_rate, dtype=np.float64)
        self.real = real

    def forecast(self, noutput_items, ninput_items_required):
        # setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        in0 = input_items[0][:len(output_items[0])]
        self.consume(0, len(output_items[0]))
        if (self.real):
            output_items[0][:] = np.multiply(in0, np.cos(self.w * self.t[:len(output_items[0])]))[:len(output_items[0])]
        else:
            output_items[0][:] = np.multiply(in0, np.sin(self.w * self.t[:len(output_items[0])]))[:len(output_items[0])]

        self.t += self.t[len(output_items[0])-1] - self.t[0] + self.tstep
        return len(output_items[0])

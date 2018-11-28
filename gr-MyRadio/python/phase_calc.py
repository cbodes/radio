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


class phase_calc(gr.basic_block):
    """
    docstring for block freq_calc
    """

    def __init__(self, sample_rate):
        gr.basic_block.__init__(self,
                                name="freq_calc",
                                in_sig=[np.float32],
                                out_sig=[np.float32])
        self.tstep = 1. / sample_rate
        self.times = np.arange(0, self.tstep * 16384, self.tstep, dtype=np.float64)
        self.prevFreq = 0.
        self.prevPhase = 0.

    def forecast(self, noutput_items, ninput_items_required):
        # setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        in0 = input_items[0][:]
        freqdiff = np.subtract(np.insert(in0, 0, self.prevFreq, axis=0)[:-1], in0)
        phase = np.multiply(freqdiff, self.times[:len(in0)])
        phase[0] += self.prevPhase
        output_items[0][:] = np.cumsum(phase)[:len(output_items[0])]
        self.prevFreq = in0[len(output_items[0])-1]
        self.prevPhase = output_items[0][len(output_items[0])-1]
        self.consume(0, len(output_items[0]))
        curT = self.times[len(output_items[0])-1] + self.tstep
        self.times += curT - self.times[0]
        return len(output_items[0])

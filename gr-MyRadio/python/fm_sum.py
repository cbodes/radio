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


class fm_sum(gr.basic_block):
    """
    docstring for block fm_sum
    """

    def __init__(self, samples_per_symbol):
        gr.basic_block.__init__(self,
                                name="fm_sum",
                                in_sig=[np.float32, np.float32, np.float32, np.float32],
                                out_sig=[np.float32, np.float32, np.float32, np.float32])

        self.samples_per_symbol = samples_per_symbol
        self.curI = 0
        self.sum0a = 0
        self.sum0b = 0
        self.sum1a = 0
        self.sum1b = 0

    def forecast(self, noutput_items, ninput_items_required):
        # setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = int(noutput_items * self.samples_per_symbol)

    def general_work(self, input_items, output_items):

        self.sum1a += np.sum(input_items[0][:])
        self.sum1b += np.sum(input_items[1][:])
        self.sum0a += np.sum(input_items[2][:])
        self.sum0b += np.sum(input_items[3][:])
        self.curI += len(input_items[0])
        self.consume_each(len(input_items[0]))
        if (self.curI > self.samples_per_symbol):
            output_items[0][:] = self.sum1a
            output_items[1][:] = self.sum1b
            output_items[2][:] = self.sum0a
            output_items[3][:] = self.sum0b
            self.sum1a = 0
            self.sum1b = 0
            self.sum0a = 0
            self.sum0b = 0
            self.curI -= self.samples_per_symbol
            return 1
        return 0

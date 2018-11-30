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
                                in_sig=[(np.float32, samples_per_symbol)],
                                out_sig=[np.float32])

        self.samples_per_symbol = samples_per_symbol
        self.curI = self.samples_per_symbol
        self.sum = 0

    def forecast(self, noutput_items, ninput_items_required):
        # setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        output_items[0][:] = np.sum(input_items[0][:])
        self.consume(0, len(output_items[0]))
        return len(output_items[0])
        # nItems = len(input_items[0])
        # in0 = input_items[0]
        # if nItems >= self.curI:
        #     self.sum += np.sum(in0[:self.curI])
        #     output_items[0][:] = self.sum
        #     self.sum = np.sum(in0[self.curI:nItems])
        #     self.consume(0, nItems)
        #     self.curI = self.samples_per_symbol
        #     return 1
        # self.sum += np.sum(in0)
        # self.curI -= nItems
        # self.consume(0, nItems)
        # return 0

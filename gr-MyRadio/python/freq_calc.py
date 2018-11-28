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


class freq_calc(gr.basic_block):
    """
    docstring for block freq_calc
    """

    def __init__(self, sample_rate, f_bandwidth, f_carrier):
        gr.basic_block.__init__(self,
                                name="freq_calc",
                                in_sig=[np.float32],
                                out_sig=[np.float32])

        self.w_b = f_bandwidth * np.pi
        self.w_c = f_carrier * np.pi * 2

    def forecast(self, noutput_items, ninput_items_required):
        # setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        output_items[0][:] = input_items[0][:len(output_items[0])] * self.w_b + self.w_c
        self.consume(0, len(output_items[0]))
        return len(output_items[0])

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


class cdma_decode(gr.basic_block):
    """
    docstring for block cdma_decode
    """

    def __init__(self, cdma_code):
        gr.basic_block.__init__(self,
                                name="cdma_decode",
                                in_sig=[(np.int8, len(cdma_code))],
                                out_sig=[np.int8])
        self.cdma_code = cdma_code

    def forecast(self, noutput_items, ninput_items_required):
        # setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        output_items[0][:] = np.where(np.dot(input_items[0][:len(output_items[0])], self.cdma_code) > 0, 1, 0)
        #print input_items[0]
        self.consume(0, len(input_items[0]))
        # self.consume_each(len(input_items[0]))
        return len(output_items[0])

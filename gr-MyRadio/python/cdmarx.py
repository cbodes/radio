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


class cdmarx(gr.basic_block):
    """
    docstring for block cdmarx
    """
    data = []

    def __init__(self, packet_header, expected):
        gr.basic_block.__init__(self,
                                name="cdmarx",
                                in_sig=[np.int8],
                                out_sig=None)
        self.packet_header = packet_header
        self.printData = -1
        self.data = []
        self.messageData = []
        self.expected = expected

    def general_work(self, input_items, output_items):
        in0 = input_items[0][0]
        self.consume_each(1)
        self.data.append(in0)
        if self.printData >= 0 and self.printData <= 15:
            self.messageData.append(in0)
            self.printData += 1
            return 0
        
        if (self.data[-1 * len(self.packet_header):] == self.packet_header):
            print self.messageData
            self.messageData = []
            self.printData = 0
        return 0
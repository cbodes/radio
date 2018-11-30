# Copyright 2011 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
install(FILES
    MyRadio_rrc_filter.xml
    MyRadio_cpfsk.xml
    MyRadio_cdmarx.xml
    MyRadio_cdmagen.xml
    MyRadio_fm_demod.xml
    MyRadio_fm_sum.xml
    MyRadio_fm_square.xml
    MyRadio_fm_compare.xml
    MyRadio_cdma_decode.xml
    MyRadio_phase_calc.xml
    MyRadio_freq_calc.xml
    MyRadio_time_calc.xml
    MyRadio_fm_multiply.xml
    MyRadio_bitconv.xml DESTINATION share/gnuradio/grc/blocks
)

#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/cam/radio/gr-MyRadio/python
export PATH=/home/cam/radio/gr-MyRadio/build/python:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
export PYTHONPATH=/home/cam/radio/gr-MyRadio/build/swig:$PYTHONPATH
/usr/bin/python2 /home/cam/radio/gr-MyRadio/python/qa_fm_sum.py 

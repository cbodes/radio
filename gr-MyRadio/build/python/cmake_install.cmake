# Install script for directory: /home/cam/radio/gr-MyRadio/python

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages/MyRadio" TYPE FILE FILES
    "/home/cam/radio/gr-MyRadio/python/__init__.py"
    "/home/cam/radio/gr-MyRadio/python/rrc_filter.py"
    "/home/cam/radio/gr-MyRadio/python/cpfsk.py"
    "/home/cam/radio/gr-MyRadio/python/cdmarx.py"
    "/home/cam/radio/gr-MyRadio/python/cdmagen.py"
    "/home/cam/radio/gr-MyRadio/python/fm_demod.py"
    "/home/cam/radio/gr-MyRadio/python/fm_sum.py"
    "/home/cam/radio/gr-MyRadio/python/fm_square.py"
    "/home/cam/radio/gr-MyRadio/python/fm_compare.py"
    "/home/cam/radio/gr-MyRadio/python/cdma_decode.py"
    "/home/cam/radio/gr-MyRadio/python/phase_calc.py"
    "/home/cam/radio/gr-MyRadio/python/freq_calc.py"
    "/home/cam/radio/gr-MyRadio/python/time_calc.py"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages/MyRadio" TYPE FILE FILES
    "/home/cam/radio/gr-MyRadio/build/python/__init__.pyc"
    "/home/cam/radio/gr-MyRadio/build/python/rrc_filter.pyc"
    "/home/cam/radio/gr-MyRadio/build/python/cpfsk.pyc"
    "/home/cam/radio/gr-MyRadio/build/python/cdmarx.pyc"
    "/home/cam/radio/gr-MyRadio/build/python/cdmagen.pyc"
    "/home/cam/radio/gr-MyRadio/build/python/fm_demod.pyc"
    "/home/cam/radio/gr-MyRadio/build/python/fm_sum.pyc"
    "/home/cam/radio/gr-MyRadio/build/python/fm_square.pyc"
    "/home/cam/radio/gr-MyRadio/build/python/fm_compare.pyc"
    "/home/cam/radio/gr-MyRadio/build/python/cdma_decode.pyc"
    "/home/cam/radio/gr-MyRadio/build/python/phase_calc.pyc"
    "/home/cam/radio/gr-MyRadio/build/python/freq_calc.pyc"
    "/home/cam/radio/gr-MyRadio/build/python/time_calc.pyc"
    "/home/cam/radio/gr-MyRadio/build/python/__init__.pyo"
    "/home/cam/radio/gr-MyRadio/build/python/rrc_filter.pyo"
    "/home/cam/radio/gr-MyRadio/build/python/cpfsk.pyo"
    "/home/cam/radio/gr-MyRadio/build/python/cdmarx.pyo"
    "/home/cam/radio/gr-MyRadio/build/python/cdmagen.pyo"
    "/home/cam/radio/gr-MyRadio/build/python/fm_demod.pyo"
    "/home/cam/radio/gr-MyRadio/build/python/fm_sum.pyo"
    "/home/cam/radio/gr-MyRadio/build/python/fm_square.pyo"
    "/home/cam/radio/gr-MyRadio/build/python/fm_compare.pyo"
    "/home/cam/radio/gr-MyRadio/build/python/cdma_decode.pyo"
    "/home/cam/radio/gr-MyRadio/build/python/phase_calc.pyo"
    "/home/cam/radio/gr-MyRadio/build/python/freq_calc.pyo"
    "/home/cam/radio/gr-MyRadio/build/python/time_calc.pyo"
    )
endif()


INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_MYRADIO MyRadio)

FIND_PATH(
    MYRADIO_INCLUDE_DIRS
    NAMES MyRadio/api.h
    HINTS $ENV{MYRADIO_DIR}/include
        ${PC_MYRADIO_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    MYRADIO_LIBRARIES
    NAMES gnuradio-MyRadio
    HINTS $ENV{MYRADIO_DIR}/lib
        ${PC_MYRADIO_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(MYRADIO DEFAULT_MSG MYRADIO_LIBRARIES MYRADIO_INCLUDE_DIRS)
MARK_AS_ADVANCED(MYRADIO_LIBRARIES MYRADIO_INCLUDE_DIRS)


# Package version.
CONECTOR_VERSION_TUPLE = (0, 17, 0)
PACKAGE_VERSION = 1
PACKAGE_VERSION_EXTRA = None

VERSION_STR = '.'.join(map(
    str, CONECTOR_VERSION_TUPLE)) + '.{}'.format(PACKAGE_VERSION)
if PACKAGE_VERSION_EXTRA:
    VERSION_STR += PACKAGE_VERSION_EXTRA

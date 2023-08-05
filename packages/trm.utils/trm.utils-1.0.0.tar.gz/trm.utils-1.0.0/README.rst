trm.utils
=========

``trm.utils`` is a home for a few odds and ends that don't on their
own justify their own package but are quite often useful. For instance
``trm.utils.vec3`` is a sub-module that handles 3D Cartesian vectors,
while ``trm.utils.splfit`` is a method based on scipy routines that
carries out the commonly needed task of spline fitting with rejection
of bad data.


Installation
------------

``trm.utils`` makes use of numpy, scipy and astropy (listed in the
pyproject.tomol files as requirements), and requires Python 3.6+. One
routine ``mpl_style_axes`` only makes sense for matplotlib plots, but
if you don't use it, you don't need matplotlib to be installed.

Install ``trm.utils`` with::

 pip install trm.utils

to get via PyPI, or::

 pip install .

if you have cloned from github. If you don't have root access, append
``--user`` to the above commands to get a local install.

* Free software: BSD license

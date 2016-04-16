========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |codeship| |requires|
        | |coveralls| |codecov|
        | |landscape| |scrutinizer| |codacy| |codeclimate|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/py-mountebank/badge/?style=flat
    :target: https://readthedocs.org/projects/py-mountebank
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/kevinjqiu/py-mountebank.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/kevinjqiu/py-mountebank

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/kevinjqiu/py-mountebank?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/kevinjqiu/py-mountebank

.. |codeship| image:: https://codeship.com/projects/654c5080-e60a-0133-013c-060b11b22fb9/status?branch=master
    :alt Codeship Build Status
    :target: https://codeship.com/projects/146701
.. |requires| image:: https://requires.io/github/kevinjqiu/py-mountebank/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/kevinjqiu/py-mountebank/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/kevinjqiu/py-mountebank/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/kevinjqiu/py-mountebank

.. |codecov| image:: https://codecov.io/github/kevinjqiu/py-mountebank/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/kevinjqiu/py-mountebank

.. |landscape| image:: https://landscape.io/github/kevinjqiu/py-mountebank/master/landscape.svg?style=flat
    :target: https://landscape.io/github/kevinjqiu/py-mountebank/master
    :alt: Code Quality Status

.. |codacy| image:: https://img.shields.io/codacy/REPLACE_WITH_PROJECT_ID.svg?style=flat
    :target: https://www.codacy.com/app/kevinjqiu/py-mountebank
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/kevinjqiu/py-mountebank/badges/gpa.svg
   :target: https://codeclimate.com/github/kevinjqiu/py-mountebank
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/mountebank.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/mountebank

.. |downloads| image:: https://img.shields.io/pypi/dm/mountebank.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/mountebank

.. |wheel| image:: https://img.shields.io/pypi/wheel/mountebank.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/mountebank

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/mountebank.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/mountebank

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/mountebank.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/mountebank

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/kevinjqiu/py-mountebank/master.svg?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/kevinjqiu/py-mountebank/


.. end-badges

Mountebank for Python Developers

* Free software: BSD license

Installation
============

::

    pip install mountebank

Documentation
=============

https://py-mountebank.readthedocs.org/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

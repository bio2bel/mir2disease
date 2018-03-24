


# -*- coding: utf-8 -*-

"""Bio2BEL mir2disease is a package which allows the user to work with the miR2Disease Database.


Installation
------------
Get the Latest
~~~~~~~~~~~~~~~
Download the most recent code from `GitHub <https://github.com/bio2bel/hmdd>`_ with:

.. code-block:: sh

   $ python3 -m pip install git+https://github.com/bio2bel/hmdd.git

For Developers
~~~~~~~~~~~~~~
Clone the repository from `GitHub <https://github.com/bio2bel/hmdd>`_ and install in editable mode with:

.. code-block:: sh

   $ git clone https://github.com/bio2bel/hmdd.git
   $ cd hmdd
   $ python3 -m pip install -e .


Setup
-----
1. Create a :class:`bio2bel_hmdd.Manager` object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
>>> from bio2bel_mir2disease import Manager
>>> manager = Manager()

2. Populate the database
~~~~~~~~~~~~~~~~~~~~~~~~
This step will take sometime since the HMDD data needs to be downloaded, parsed, and fed into the database line
by line.

>>> manager.populate()

3. Get all associations to iterate and do magic

>>> associations = manager.get_relationships()
"""

from .manager import Manager

__version__ = '0.0.1-dev'

__title__ = 'bio2bel_mir2disease'
__description__ = "A package for converting the Human microRNA Disease Database (HMDD) to BEL."
__url__ = 'https://github.com/bio2bel/hmdd'

__author__ = 'Mehdi Ali, Dejan Dukic, and Charles Tapley Hoyt'
__email__ = 'charles.hoyt@scai.fraunhofer.de'

__license__ = 'MIT License'
__copyright__ = 'Copyright (c) 2018 Mehdi Ali, Dejan Dukic, and Charles Tapley Hoyt'

Python installation instructions for CLIDEsc
============================================

**Note**: you must be logged as an administrator (or root) on the
clidesc server machine in order to install the Anaconda python
distribution and configure clidesc to accept python as a climate
services development language.

The Anaconda python distribution, download and installation
-----------------------------------------------------------

The Anaconda scientific python distribution is a completely free
enterprise-ready Python distribution for large-scale data processing,
predictive analytics, and scientific computing. It includes the python
interpreter itself, the python standard library as well as a set of
packages exposing data structures and methods for data manipulation and
scientific computing and visualization. In particular it provides Numpy,
Scipy, Pandas, Matplotlib (+ basemap). The full list of packages is
available at:

`http://docs.continuum.io/anaconda/pkgs.html <http://docs.continuum.io/anaconda/pkgs.html>`_

The Anaconda python distribution must be downloaded from:

`http://continuum.io/downloads <http://continuum.io/downloads>`_

For the correct version of your linux system, to know whether CLIDEsc is
running on a 32 bits or 64 bits server, type

::

    $ uname –a 

in a terminal (the $ indicates the terminal prompt)

It will return either:

::

    x86_64 (64 bits kernel)

or:

::

    i686   (32 bits kernel)

Once copied over, make sure the anaconda installer is executable by
going in the right directory (with cd) and entering (example for
``version 2.0.1`` of Anaconda):

::

    $ chmod +x Anaconda-2.0.1-Linux-x86.sh

or:

::

    $ chmod +x Anaconda-2.0.1-Linux-x86_64.sh

then to launch the installer:

::

    $ ./Anaconda.2.0.1-Linux-x86.sh

or

::

    $ ./Anaconda.2.0.1-Linux-x86_64.sh

The installer will ask you a few questions, the most important is
related to the installation directory: The recommended installation
directory is ``/opt``: i.e the python executable will be contained in
``/opt/anaconda/bin``.

Once Anaconda is installed, you need to update conda (the python
‘package manager’ that comes with anaconda and allows the painless
installation and update of third party modules) by entering

::

    $ /opt/anaconda/bin/conda update conda

Then a good thing is to update the anaconda packages already installed

::

    $ /opt/anaconda/bin/conda update anaconda

You also need to install `pip <https://github.com/pypa/pip>`_ to install
packages from the `Python Package Index <http://pypi.python.org/pypi>`_.

::

    $ conda install pip 

Installation of additional libraries
------------------------------------

A few other libraries need to be installed in order to make the most of
the Python scientific stack:

-  `basemap <http://matplotlib.org/basemap/>`_: to create static maps
-  `vincent <http://vincent.readthedocs.org/en/latest/>`_: to create
   dynamic visualisations in the browser
-  `folium <https://github.com/wrobstory/folium>`_: to create dynamic
   maps in the browser
-  `seaborn <http://web.stanford.edu/~mwaskom/software/seaborn/>`_: to
   create sophisticated statistical visualisations

Basemap
~~~~~~~

`Basemap <http://matplotlib.org/basemap/>`_ is part of the Anaconda
Python distribution and can be installed by:

::

    $ /opt/anaconda/bin/conda install basemap 

Vincent
~~~~~~~

`vincent <http://vincent.readthedocs.org/en/latest/>`_ is to be
installed using `pip <https://github.com/pypa/pip>`_:

::

    $ /opt/anaconda/bin/pip install vincent 

Folium
~~~~~~

`folium <https://github.com/wrobstory/folium>`_, similarly install via
`pip <https://github.com/pypa/pip>`_:

::

    $ /opt/anaconda/bin/pip install folium 

Seaborn
~~~~~~~

`seaborn <http://web.stanford.edu/~mwaskom/software/seaborn/>`_ is also
to be installed via `pip <https://github.com/pypa/pip>`_:

::

    $ /opt/anaconda/bin/pip install seaborn 

psycopg2: interface to the `CLIDE <http://www.bom.gov.au/climate/pacific/about-clide.shtml>`_ database
------------------------------------------------------------------------------------------------------

The `psycopg2 <http://initd.org/psycopg/>`_ provides the interface to
the Clide `PostgreSQL <http://www.postgresql.org/>`_ database and needs
to be installed separately from sources, as it is not part of the
libraries available through the conda package manager.

One of the requirement is that ``pg_config`` should be in the system
PATH, i.e. if you type:

::

    $ pg_config --version 

in a terminal it should return the version of PostgreSQL. If something
goes wrong here, please refer to `the psycopg installation
documentation <http://initd.org/psycopg/docs/install.html#install-from-source>`_

``psycopg2`` can be installed in two ways:

1. The recommended way, using conda third party channels:

   conda install -c https://conda.binstar.org/dan\_blanchard psycopg2

2. Installing from sources:

If you want to install from sources, the psycopg2 archive (tar.gz) needs
to be downloaded from `The psycopg download
page <http://initd.org/psycopg/download/>`_

Once downloaded, cd where you downloaded the psycopg2-2.5.2.tar.gz
archive and enter:

::

    $ tar –zxvf psycopg2-2.5.2.tar.gz 

then:

::

    $ cd psycop2-2.5.2

then install the module:

::

    $ /opt/anaconda/bin/python setup.py build 
    $ /opt/anaconda/bin/python setup.py install


#Python installation instructions for CLIDEsc

**Note**: you must be logged as an administrator (or root) on the clidesc server machine in order to install the Anaconda python distribution and configure clidesc to accept python as a climate services development language.

##The Anaconda python distribution, download and installation

The Anaconda scientific python distribution is a completely free enterprise-ready Python distribution for large-scale data processing, predictive analytics, and scientific computing. It includes the python interpreter itself, the python standard library as well as a set of packages exposing data structures and methods for data manipulation and scientific computing and visualization. In particular it provides Numpy, Scipy, Pandas, Matplotlib (+ basemap). The full list of packages is available at:

[http://docs.continuum.io/anaconda/pkgs.html](http://docs.continuum.io/anaconda/pkgs.html)

The Anaconda python distribution must be downloaded from:

[http://continuum.io/downloads](http://continuum.io/downloads)

For the correct version of your linux system, to know whether CLIDEsc is running on a 32 bits or 64 bits server, type

```
$ uname –a
```

in a terminal (the $ indicates the terminal prompt)

It will return either:

    x86_64 (64 bits kernel)

or:

    i686   (32 bits kernel)

Once copied over, make sure the anaconda installer is executable by going in the right directory (with cd) and entering (example for ```version 2.0.1``` of Anaconda):

    $ chmod +x Anaconda-2.0.1-Linux-x86.sh

or:

    $ chmod +x Anaconda-2.0.1-Linux-x86_64.sh

then to launch the installer:

    $ ./Anaconda.2.0.1-Linux-x86.sh

or

    $ ./Anaconda.2.0.1-Linux-x86_64.sh

The installer will ask you a few questions, the most important is related to the installation directory: The recommended installation directory is ```/opt```: i.e the python executable will be contained in ```/opt/anaconda/bin```.

Once Anaconda is installed, you need to update conda (the python ‘package manager’ that comes with anaconda and allows the painless installation and update of third party modules) by entering

    $ /opt/anaconda/bin/conda update conda

Then a good thing is to update the anaconda packages already installed

    $ /opt/anaconda/bin/conda update anaconda

You also need to install [pip](https://github.com/pypa/pip) to install packages from the [Python Package Index](http://pypi.python.org/pypi).

    $ conda install pip

## Installation of additional libraries

A few other libraries need to be installed in order to make the most of the Python scientific stack:

+ [basemap](http://matplotlib.org/basemap/): to create static maps
+ [vincent](http://vincent.readthedocs.org/en/latest/): to create dynamic visualisations in the browser
+ [folium](https://github.com/wrobstory/folium): to create dynamic maps in the browser
+ [seaborn](http://web.stanford.edu/~mwaskom/software/seaborn/): to create sophisticated statistical visualisations

### Basemap

[Basemap](http://matplotlib.org/basemap/) is part of the Anaconda Python distribution and can be installed by:

    $ /opt/anaconda/bin/conda install basemap

### Vincent

[vincent](http://vincent.readthedocs.org/en/latest/) is to be installed using [pip](https://github.com/pypa/pip):

    $ /opt/anaconda/bin/pip install vincent

### Folium

[folium](https://github.com/wrobstory/folium), similarly install via [pip](https://github.com/pypa/pip):

    $ /opt/anaconda/bin/pip install folium

### Seaborn

[seaborn](http://web.stanford.edu/~mwaskom/software/seaborn/) is also to be installed via [pip](https://github.com/pypa/pip):

    $ /opt/anaconda/bin/pip install seaborn

## psycopg2: interface to the [CLIDE](http://www.bom.gov.au/climate/pacific/about-clide.shtml) database

The [psycopg2](http://initd.org/psycopg/) provides the interface to the Clide [PostgreSQL](http://www.postgresql.org/) database. It is not part of the libraries distributed with [anaconda](), but can be installed using [binstar](www.binstar.org) channel or from sources.

Before installing [psycopg2](http://initd.org/psycopg/), make sure that ```pg_config``` is in the system PATH, i.e. if you type:

    $ pg_config --version

in a terminal it should return the version of PostgreSQL. If something goes wrong here, please refer to [the psycopg installation documentation](http://initd.org/psycopg/docs/install.html#install-from-source)

`psycopg2` can be installed in two ways:

1. We can make use of [Dan Blanchard](http://dan-blanchard.github.io/)'s channel for psycopg2


    $ conda install -c https://conda.binstar.org/dan_blanchard psycopg2


2. Installing from sources:

If the above method fails, you need to install from sources, the psycopg2 archive (tar.gz) needs to be downloaded from [The psycopg download page](http://initd.org/psycopg/download/)

Once downloaded, cd where you downloaded the psycopg2 archive and enter:  

    $ tar –zxvf psycopg2-2.5.2.tar.gz (*! your version numbers might differ*)

then:

    $ cd psycop2-2.5.2

then install the module:

    $ /opt/anaconda/bin/python setup.py build
    $ /opt/anaconda/bin/python setup.py install

## Configuration of the clidesc application layer to accept the python language

In order to activate the Python language as an option for developing a climate service, one needs to modify the `config.yml` file that is located (usually) in `/var/www/clidesc/app/config`. On **line 8**, the parameter `script_lang.python` must point to the python binary installed by anaconda, example:

```
parameters:
    processing_path:
        python: "/opt/anaconda/bin/python"
        R: "/usr/bin/Rscript"
        R64: "/usr/bin/Rscript --arch=x86_64"
        php: "/usr/bin/php"
        perl: "/usr/bin/perl"
```

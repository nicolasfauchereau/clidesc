Python installation instructions for CLIDEsc
============================================

**Note**: you must be logged as an administrator (or root) on the clidesc server machine in order to install the Anaconda python distribution and configure clidesc to accept python as a climate services development language.

 The Anaconda python distribution, download and installation

The Anaconda scientific python distribution is a completely free enterprise-ready Python distribution for large-scale data processing, predictive analytics, and scientific computing. It includes the python interpreter itself, the python standard library as well as a set of packages exposing data structures and methods for data manipulation and scientific computing and visualization. In particular it provides Numpy, Scipy, Pandas, Matplotlib (+ basemap). The full list of packages is available at: 

http://docs.continuum.io/anaconda/pkgs.html

The Anaconda python distribution must be downloaded from: 

http://continuum.io/downloads

For the correct version of your linux system, to know whether CLIDEsc is running on a 32 bits or 64 bits server, type 

```
$ uname –a 
```

in a terminal (the $ indicates the terminal prompt)

It will return either::

    x86_64 (64 bits kernel)

or:: 

    i686   (32 bits kernel)

Once copied over, make sure the anaconda installer is executable by going in the right directory (with cd) and entering::

    $ chmod +x Anaconda-1.9.2-Linux-x86.sh

or:: 

    $ chmod +x Anaconda-1.9.2-Linux-x86_64.sh

then to launch the installer:: 


$ ./Anaconda.1.9.2-Linux-x86.sh

or:: 

$ ./Anaconda.1.9.2-Linux-x86_64.sh

The installer will ask you a few questions, the most important is related to the installation directory: The recommended installation directory is /opt: i.e the python executable will be contained in /opt/anaconda/bin. 

Once anaconda is installed, you need to update conda (the python ‘package manager’ that comes with anaconda and allows the painless installation and update of third party modules) by entering 

$ /opt/anaconda/bin/conda update conda

Then a good thing is to update the anaconda packages already installed 

$ /opt/anaconda/bin/conda update anaconda


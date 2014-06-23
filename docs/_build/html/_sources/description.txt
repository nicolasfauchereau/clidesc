CLImate Data for the Environment Services application Client (CLIDEsc)
======================================================================

**CliDEsc** is a web-based open source platform containing tools that
allow end users to request data and products to be generated from the
**CLIDE** (`CLImate Data for the
Environment <http://www.bom.gov.au/climate/pacific/about-clide.shtml>`_)
database.

`CLIDE <http://www.bom.gov.au/climate/pacific/about-clide.shtml>`_ is a
PostGRES database dedicated to the storage and management of
hydroclimatic data. CLIDE has been originally developed by the Bureau of
Meteorology.

Climate data analysis and visualisation tools ('services') in CliDEsc
are developed in R and Python. This repository contains the Python
component of CLIDEsc, including a module that provides the interface to
the CLIDE database, utilities function to perform common tasks (e.g.
calculate monthly statistics from daily or sub-daily data) and
self-contained example python scripts that implement climate services.

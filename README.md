# CLImate Data for the Environment Services Client (CLIDEsc)

**CliDEsc** is a web-based open source platform containing tools that allow end users to request data and products to be generated from the **CLIDE** ([CLImate Data for the Environment](http://www.bom.gov.au/climate/pacific/about-clide.shtml)) database.

[CLIDE](http://www.bom.gov.au/climate/pacific/about-clide.shtml) is a PostGRES database dedicated to the storage and management of hydroclimatic data. CLIDE has been originally developed by the [Australian Bureau of Meteorology](http://http://www.bom.gov.au/) and is used in many countries in the southwest Pacific region.

Climate data analysis and visualisation tools (**climate services**) in CliDEsc are developed in [R](http://www.r-project.org/) and [Python](www.python.org).
This repository contains the **Python component of CLIDEsc**, including a module (`clide.py`) that provides the interface to the CLIDE database, utilities functions
to perform common tasks (e.g. calculate monthly statistics from daily or sub-daily data) and self-contained example python scripts that implement
climate services.

The **INSTALLATION INSTRUCTIONS** are available from [here](https://github.com/nicolasfauchereau/clidesc/blob/master/INSTALL.md).


---
**NOTE**: This is very young project, with a structure and scope likely to undergo rapid changes, questions and comments should be addressed to [Nicolas Fauchereau](mailto:nicolas.fauchereau@niwa.co.nz)

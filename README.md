# sw_netcdf_air Repo

netcdf_air script is purposed to parse overall all NetCDF files air temperature by time with constant lat, long and level

## Who designed this

* [Danil Borchevkin](http://github.com/DanilBorchevkin)

* [Olga Borchevkina](https://github.com/olgaborchevkina)

## Licence

BSD-2 Clause. Please see LICENCE file

## What included

* ***/netcdf_air.py*** - Python 3.6 script

* ***/LICENCE*** - licence file

* ***/README.md*** - this file

## Dependencies

* [xarray](http://xarray.pydata.org/en/stable/)

## How to start the script

For run this script you need Python 3 dist.

For start the script please execute ```python netcdf_air.py```

## How to compile the script into a execute file

Tested compile with [pyinstaller](http://www.pyinstaller.org). For compile please run 

```
pyi-makespec --onefile netcdf_air.py
pyinstaller lidarStrobeParses.py
```

Afrer successful compiling you can start the script as standalone app. 

## Where you can get needed files for parsing

On this link - NCEP Reanalysis pressure - ftp://ftp.cdc.noaa.gov/Datasets/ncep.reanalysis/pressure/. ***This script works only with air.yyyy.nc files!***

## Scheme of the result data
For result file used CSV ASCII file (delimeter - "    " - 4x space). Columns writes as following:

1. Time in human readable format
2. Temp of air, degK
3. Level, mBar
4. Latitude, deg
5. Longitude, deg

## Feedback

Tech questions - [Danil Borchevkin](http://github.com/DanilBorchevkin)

Science questions - [Olga Borchevkina](https://github.com/olgaborchevkina)

Administrative questions - [Olga Borchevkina](https://github.com/olgaborchevkina)

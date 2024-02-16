

# AGN models

All models can be run from the command line by providing the following required parameters:
```
--grid_dir: the directory where the resulting grid should be stored
--config_file: a yaml file containing the grid axes 
```

## Broken power-law

A simple implementation of an AGN accretion disc is to assume it follows a broken power-law behaviour. One example of this implementation is [Feltre, Charlot, and Gutkin (2016)](https://ui.adsabs.harvard.edu/abs/2016MNRAS.456.3354F/abstract) who combined this model with photoionisation modelling using 'cloudy'. 

'install_broken_power_law.py' can be used to generate a grid of incident spectra assuming a three component broken power-law. The grid axes are set using the yaml configuration file.

## RELAGN

The RELAGN model is a fully relativistic treatment of BH accretion discs and is described in [Hagen and Done (2023)](https://ui.adsabs.harvard.edu/abs/2023MNRAS.525.3455H/abstract). RELAGN models the BH accretion disc using four parameters: BH mass, the accreate rate as a fraction of the Eddington rate, the cosine of the inclination, and the dimensionless spin (a). 

Generating the spectra using this model requires the use of the 'relagn' module available [here](https://github.com/scotthgn/RELAGN). Unfortunately this can not currently be installed directly, instead at present, we must clone the 'relagn' repository to this directory from where we can access the 'relagn' module. The 'relagn' module also requires a working installation of the ['xspec' package](https://heasarc.gsfc.nasa.gov/xanadu/xspec/).  

Like the Broken power-law model grids are generated by specifying a config file including the grid axes.

## AGNSED

For most purposes the 'relagn' model is probably not required since BH spins are either not available or sufficiently small to not make a difference. Instead we can use the AGNSED model described in [Kubota and Done (2018)](https://ui.adsabs.harvard.edu/abs/2018MNRAS.480.1247K/abstract). The AGNSED model is available in the 'relagn' module by simply setting the spin to be 0 and asking for the non-relativistic spectra.

Like the Broken power-law model grids are generated by specifying a config file including the grid axes.
import xarray as xr
import numpy
import matplotlib.pyplot as plt
import pdb



file1 = '/users/global/cornkle/CMIP/CMIP5_Africa/BC_0.5x0.5/MPI-ESM-LR/historical/tas_WFDEI_1979-2013_0.5x0.5_day_MPI-ESM-LR_west-africa_historical_r1i1p1_full.nc'
file2 =  '/users/global/cornkle/CMIP/CMIP5_Africa/BC_0.5x0.5/MPI-ESM-LR/rcp85/tas_WFDEI_1979-2013_0.5x0.5_day_MPI-ESM-LR_west-africa_rcp85_r1i1p1_full.nc'

hist = xr.open_dataset(file1)
future = xr.open_dataset(file2)

cut = [-6, 2.8, 9 ,15.5]

hist = hist.sel(lon=slice(cut[0], cut[1]), lat=slice(cut[2],cut[3]))
future = future.sel(lon=slice(cut[0], cut[1]), lat=slice(cut[2],cut[3]))
hist = hist['tas']
future = future['tas']

plt.figure()
hist[0,:,:].plot.contourf()

plt.figure()
future[0,:,:].plot.contourf()

hist = hist[(hist['time.month'] <= 9) & (hist['time.month'] <= 7)].median()
future = future[(future['time.month'] <= 9) & (future['time.month'] <= 7) & (future['time.year'] >= 2040) & (
    future['time.year'] <= 2059)].median()


print('Past', hist-273.15)
print('Future', future-273.15)
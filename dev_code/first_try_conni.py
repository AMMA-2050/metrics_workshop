### First attempt to compute percentiles, precip above threshold, dry spell over 6 days

import iris
import iris.coord_categorisation
import matplotlib.pyplot as plt
import iris.plot as iplt
import cartopy
import cartopy.crs as ccrs
import numpy as np

iris.FUTURE.netcdf_promote = True
    
def count_spells(data, threshold, axis, spell_length):
    """
    FROM IRIS DOCUMENTATION:
    Function to calculate the number of points in a sequence where the value
    has exceeded a threshold value for at least a certain number of timepoints.
    Generalised to operate on multiple time sequences arranged on a specific
    axis of a multidimensional array.

    Args:
    * data (array):
        raw data to be compared with value threshold.
    * threshold (float):
        threshold point for 'significant' datapoints.
    * axis (int):
        number of the array dimension mapping the time sequences.
        (Can also be negative, e.g. '-1' means last dimension)
    * spell_length (int):
        number of consecutive times at which value > threshold to "count".
    """

    if axis < 0:
        # just cope with negative axis numbers
        axis += data.ndim
    # Threshold the data to find the 'significant' points.
    data_hits = data < threshold
    # Make an array with data values "windowed" along the time axis.
    hit_windows = iris.util.rolling_window(data_hits, window=spell_length, axis=axis)
    # Find the windows "full of True-s" (along the added 'window axis').
    full_windows = np.all(hit_windows, axis=axis+1)
    # Count points fulfilling the condition (along the time axis).
    spell_point_counts = np.sum(full_windows, axis=axis, dtype=int)
    return spell_point_counts

def run():
    path = 'C://Users/cornkle/data/CEH/AMMA/workshop2016/amma2050.ipsl.upmc.fr/CMIP5_AFRICA/0.5x0.5/HadGEM2-ES/rcp85/'
    file = 'pr_day_HadGEM2-ES_africa_0.5x0.5_rcp85_r1i1p1_full.nc'

    cube = iris.load(path+file)

    WA_lat=iris.Constraint(latitude=lambda cell: 4 <= cell <= 25.0)
    WA_lon=iris.Constraint(longitude=lambda cell: -18 <= cell <= 25.0)

    # Extract West Africa
    pcp = cube[0]
    pcp = pcp.extract('precipitation_flux' & WA_lat & WA_lon)
    pcp.convert_units('kg m-2 day-1')

    # Add month coordinate
    iris.coord_categorisation.add_month_number(pcp, 'time', name='month')

    #Get monthly percentile per pixel
    perc = pcp.aggregated_by('month', iris.analysis.PERCENTILE, percent=95)

    # Get number of days above 10mm day-1 rainfall threshold
    thresh = pcp.collapsed('time', iris.analysis.COUNT, function = lambda values: values > 10 )

    #Start computation of dry spell
    # Make an aggregator from dry spell count
    count = iris.analysis.Aggregator('spell_count',count_spells,
                                 units_func=lambda units: 1)

    # Define the parameters
    thresh_rain = 1
    spell_days = 6

    # Calculate the statistic
    dry_spell = pcp.collapsed('time', count,threshold=thresh_rain,
                                      spell_length=spell_days)
    dry_spell.rename('Number of days with rain < 1mm day-1 over 6 consecutive days')


    # Quick mean temperature
    iris.coord_categorisation.add_year(pcp, 'time', name='year')
    p_mean = pcp.aggregated_by(['year'], iris.analysis.MEAN)
    pmean = p_mean.collapsed(['latitude', 'longitude'], iris.analysis.MEAN)

    #plot
    fig = plt.figure()
    ax = fig.add_subplot(2, 2, 1, projection=ccrs.PlateCarree())
    iplt.contourf(perc[7], cmap='viridis')
    plt.title('95th percentile per pixel in August')
    ax.coastlines()
    # Gridlines
    xl = ax.gridlines(draw_labels=True);
    xl.xlabels_top = False
    xl.ylabels_right = False
    # Countries
    ax.add_feature(cartopy.feature.BORDERS, linestyle='--');
    plt.colorbar()

    ax = fig.add_subplot(2, 2, 2, projection=ccrs.PlateCarree())
    iplt.contourf(thresh, cmap='viridis')
    plt.title('Nb of days with precip > 10mm day-1 ')
    ax.coastlines()
    # Gridlines
    xl = ax.gridlines(draw_labels=True);
    xl.xlabels_top = False
    xl.ylabels_right = False
    # Countries
    ax.add_feature(cartopy.feature.BORDERS, linestyle='--');
    plt.colorbar()

    ax = fig.add_subplot(2, 2, 3, projection=ccrs.PlateCarree())
    iplt.contourf(dry_spell, cmap='viridis')
    plt.title('Nb of days with precip < 1mm day-1 over 6 consecutive days')
    ax.coastlines()
    # Gridlines
    xl = ax.gridlines(draw_labels=True);
    xl.xlabels_top = False
    xl.ylabels_right = False
    # Countries
    ax.add_feature(cartopy.feature.BORDERS, linestyle='--');
    plt.colorbar()

    ax = fig.add_subplot(2, 2, 4)
    iplt.plot(pmean)

    plt.show()

if __name__ == '__main__':
    run()

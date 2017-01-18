import iris
import numpy as np
import scipy as sci
import matplotlib.pyplot as plt
import iris.coord_categorisation
import ipdb



def variable_setter(string):
	if string == 'var':
		string = 'pr'
	if string =='seas':
		string = 'jas'
	if string =='plot_type':
		string = 'barplot_year'
	return string

if "__name__" == "__variable_setter__":
    variable_setter(string)


def getSeasConstr(name):
    sncon = {'ann': iris.Constraint(month_number=lambda cell: 1 <= cell <= 12),
             'mj': iris.Constraint(month_number=lambda cell: 5 <= cell <= 6),
             'jj': iris.Constraint(month_number=lambda cell: 6 <= cell <= 7),
             'ja': iris.Constraint(month_number=lambda cell: 7 <= cell <= 8),
             'as': iris.Constraint(month_number=lambda cell: 8 <= cell <= 9),
             'so': iris.Constraint(month_number=lambda cell: 9 <= cell <= 10),
             'jan': iris.Constraint(month_number=lambda cell: cell == 1),
             'feb': iris.Constraint(month_number=lambda cell: cell == 2),
             'mar': iris.Constraint(month_number=lambda cell: cell == 3),
             'apr': iris.Constraint(month_number=lambda cell: cell == 4),
             'may': iris.Constraint(month_number=lambda cell: cell == 5),
             'jun': iris.Constraint(month_number=lambda cell: cell == 6),
             'jul': iris.Constraint(month_number=lambda cell: cell == 7),
             'aug': iris.Constraint(month_number=lambda cell: cell == 8),
             'sep': iris.Constraint(month_number=lambda cell: cell == 9),
             'oct': iris.Constraint(month_number=lambda cell: cell == 10),
             'nov': iris.Constraint(month_number=lambda cell: cell == 11),
             'dec': iris.Constraint(month_number=lambda cell: cell == 12),
             'djf': iris.Constraint(month_number=lambda cell: (cell == 12) | (1 <= cell <= 2)),
             'mam': iris.Constraint(month_number=lambda cell: 3 <= cell <= 5),
             'jja': iris.Constraint(month_number=lambda cell: 6 <= cell <= 8),
             'jas': iris.Constraint(month_number=lambda cell: 7 <= cell <= 9),
             'jjas': iris.Constraint(month_number=lambda cell: 6 <= cell <= 9),
             'mjjas': iris.Constraint(month_number=lambda cell: 5 <= cell <= 9),
             'son': iris.Constraint(month_number=lambda cell: 9 <= cell <= 11)
             }

    return (sncon[name])


if __name__ == "__getSeasConstr__":
    getSeasConstr(season)

############################################

def main(incube,season,ncfile):

    print 'This is the calc script'

    iris.coord_categorisation.add_month_number(incube, 'time', name='month_number')
    iris.coord_categorisation.add_year(incube, 'time', name='year')
    slicer = getSeasConstr(season)

    incube = incube.extract(slicer)
    #iris.coord_categorisation.add_season_year(incube, 'time', name='season_year', seasons=(season))

    c_monthly = incube.aggregated_by(['year'], iris.analysis.MEAN)
    c_monthly.convert_units('kg m-2 day-1')

    # This is the monthly climatology (mean and std deviation)

    std = c_monthly.collapsed('year', iris.analysis.STD_DEV)
    mean = c_monthly.collapsed('year', iris.analysis.MEAN)

    # We need to change the shape of the monthly climatologies to match the shape of the timeseries (in the cube c_monthly)

    mean = mean.data
    std = std.data

    clim_mean_data = np.repeat(mean.reshape(1,mean.shape[0], mean.shape[1]), c_monthly.shape[0], axis=0)#np.tile(mean.data, (c_monthly.shape[0] / mean.shape[0], 1, 1))
    clim_std_data = np.repeat(std.reshape(1,std.shape[0], std.shape[1]), c_monthly.shape[0], axis=0) #np.tile(std.data, (c_monthly.shape[0] / std.shape[0], 1, 1))

    clim_mean_cube = c_monthly.copy(clim_mean_data)
    clim_std_cube = c_monthly.copy(clim_std_data)

    spi = (c_monthly - clim_mean_cube) / clim_std_cube

    spi = spi.collapsed(['longitude', 'latitude'], iris.analysis.MEAN)
    #spi = spi.collapsed('latitude', iris.analysis.MEAN)

    iris.save(spi,ncfile)

if __name__ == "__main__":
	main(incube,season,ncfile)

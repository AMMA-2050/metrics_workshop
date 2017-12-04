import xarray as xr
import os
import glob


# available FTYPES: ['0.5x0.5', 'BC_0.5x0.5', 'BC_mdlgrid', 'mdlgrid']

def loop_folders(cmip_path, ftype, out, lon, lat):
    """
    Loops through CMIP5 model folders and calls the point extraction routine.
    Saves to csv files

    :param cmip_path: path to CMIP5 main folder
    :param ftype: the file type of CMIP5 to be looped through
    :param out: the folder where .csv should be saved
    :param lon: longitude of the point that should be extracted
    :param lat: latitude of the point that should be extracted
    :return: .csv files of all CMIP5 models for the chosen file type
    """

    ftype_path = cmip_path + os.sep + ftype

    # find all precip *.nc files in the chosen CMIP5 folder
    f_list = glob.glob(ftype_path + os.sep + '*' + os.sep + '*' + os.sep + 'pr*.nc')

    if f_list == []:
        print('No files found, check your paths')

    for f in f_list:
        file(f, out, lon, lat)


def file(fpath, out, lon, lat):
    """
    Extracts a single-point time series and save it as .csv file.
    The point is chosen via nearest neighbour

    :param fpath: path to single CMIP5 netCDF file
    :param out: path to out-directory where .csv files should be saved
    :param lon: longitude of point
    :param lat: latitude of point
    :return: .csv file
    """

    ds = xr.open_dataset(fpath)
    fname = os.path.basename(fpath)
    fname = fname.replace('.nc', '.csv')

    precip = ds['pr'] * 86400  # mm s-1 to mm day-1

    pbox = precip.sel(lon=lon, lat=lat, method='nearest', tolerance=1.5)
    pbox = pbox.to_pandas()
    pbox.to_csv(out + os.sep + fname)
    print('Saved ' + out + os.sep + fname)


if __name__ == "__main__":

    my_path = '/users/global/cornkle/CMIP/CMIP5_Africa'
    my_out = '/users/global/cornkle/test'
    my_ftype = 'BC_0.5x0.5'
    my_lon = -1.5
    my_lat = 12.4

    loop_folders(my_path, my_ftype, my_out, my_lon, my_lat)

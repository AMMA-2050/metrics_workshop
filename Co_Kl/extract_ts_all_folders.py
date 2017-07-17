import xarray as xr
import os
import pdb
import subprocess
import glob

#available FTYPES: ['0.5x0.5', 'BC_0.5x0.5', 'BC_mdlgrid', 'mdlgrid']

def loop_folders(cmip_path, ftype, out, lon, lat):

    ftype_path = cmip_path + os.sep + ftype

    #create folder structure from CMIP5 path ftype
    #os.system('rsync -a -f"+ */" -f"- *" '+ftype_path+os.sep+' '+out+os.sep)

    #find all precip *.nc files in the chosen CMIP5 folder
    f_list = glob.glob(ftype_path+os.sep+'*'+os.sep+'*'+os.sep+'pr*.nc')

    if f_list == []:
        print('No files found, check your paths')

    for f in f_list:

        # fsplit = f.split(os.sep)
        # fout = out + os.sep + fsplit[-3] + os.sep + fsplit[-2]

        file(f, out, -1.5, 12.4 )

def file(fpath, out, lon, lat):

    ds = xr.open_dataset(fpath)
    fname = os.path.basename(fpath)
    fname = fname.replace('.nc', '.csv')

    precip = ds['pr'] * 86400  # mm s-1 to mm day-1

    pbox = precip.sel(lon=lon, lat=lat, method='nearest', tolerance=1.5)
    pbox = pbox.to_pandas()
    pbox.to_csv(out+os.sep+fname)
    print('Saved '+out+os.sep+fname)


if __name__ == "__main__":

    my_path = '/users/global/cornkle/CMIP/CMIP5_Africa'
    my_out = '/users/global/cornkle/test'
    my_ftype = 'BC_0.5x0.5'
    my_lon = -1.5
    my_lat = 12.4

    loop_folders(my_path, my_ftype, my_out, my_lon, my_lat)



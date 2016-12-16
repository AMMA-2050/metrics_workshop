'''
master.py
'''
import load_file_name
import load_data
import calcSPI
import spi_plot
import iris

def master(variable,scenario,bc_and_resolution,outpath,region):
    
    #cdivoire_coords = [-2,9,4,12]
    plotpath='mypath'
   
    files_good, modelID = load_file_name.load_file_name(variable,scenario,bc_and_resolution)
    #print files_good[:]
    #print modelID
    # Loop through file names
    for fle in files_good:
        print fle
        cubeout = load_data.load_data(fle,region[0],region[1],region[2],region[3])
        for nme in modelID:
             if nme in fle:   
                 print 'Doing '+nme             
                 nc_file = outpath+'/'+str(nme)+'_SPI-1month.nc'
                 try: 
                    cubeout = iris.load_cube(nc_file) 
                 except IOError: 
                     spi = calcSPI.calcSPI(cubeout, 1, nc_file)
                     iris.save(spi, nc_file)
                                                                                 
                 spi_plot.timeseries(spi, cdivoire_coords, plotpath, nme)
                 spi_plot.map(spi, cdivoire_coords, plotpath, nme)
        
if __name__ == "__main__":
    variable='pr'
    scenario='historical'
    bc_and_resolution='BC_0.5x0.5'
    outpath='/nfs/a266/earv056/SPI'
    region=[-30,10,-10,35]
    master(variable,scenario,bc_and_resolution,outpath,region)

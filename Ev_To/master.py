'''
master.py
'''
import load_file_names
import cal_seasonal
import load_data
import calc_hovmoller_precip
import pdb
import iris
import plotCode

def master(variable,scenario,bc_and_resolution,outpath,season,region):
    #variable = 'pr'
    #scenario = 'historical''
    #bc_and_resolution = 'BC_0.5x0.5'
    
    files_good,modelID = load_file_names.load_file_names(variable,scenario,bc_and_resolution)
    #print files_good[:]
    #print modelID

    for fle in files_good:        
        for nme in modelID:
            if nme in fle: 
                print 'current model:', nme
                nc_file1 = outpath+'/'+str(nme)+'_'+str(region)+'.timeseries.nc'
                nc_file2 = outpath+'/'+str(nme)+'_'+str(region)+'.climatology.nc'   
                try:
                    cube2plot = iris.load_cube(nc_file1)                         
                    cube2plot2 = iris.load_cube(nc_file2) 
                except IOError:
                    print 'IOError, creating nc files!'
        
                    cubeout=load_data.load_data(fle,-18,15,-5,25)
           
                    cube2plot, cube2plot2 = cal_seasonal.cal_seasonal(cubeout,nc_file1,nc_file2)
                print cube2plot
                print cube2plot2                            
                plotCode.plotCode(cube2plot, cube2plot2, nme)
        #return(files_good,modelID)
        
if __name__ == "__main__":
    master()  
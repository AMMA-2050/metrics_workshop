'''
master.py

on the commandline do: master.master('pr','historical','BC_0.5x0.5')
'''
import load_file_names
import load_data
import calc_CDD
import pdb

def master(variable,scenario,bc_and_resolution, outpath, season, region):
    
    #Get all filenames
    files_good, modelID=load_file_names.load_file_names(variable,scenario,bc_and_resolution)  
    print files_good[:]
    print modelID
    
    for file in files_good:
        #pdb.set_trace()
        cubeout = load_data.load_data(file,-5,10,-10,10)
        
        i = files_good.index(file)
        nc_file=outpath+'/'+str(modelID[i])+'_'+str(season)+'_'+str(region)+'.nc'
   
        mwetdays,swetdays = calc_CDD.calc_CDD(cubeout,nc_file)
        
        #plot(mwetdays)
        

if __name__ == '__main__':
    variable='pr'
    scenario='historical'
    bc_and_resolution='BC_0.5x0.5'
    outpath='/nfs/a266/earv060/drydays/'
    season='jja'
    region='WA'
    master(variable,scenario,bc_and_resolution, outpath, season, region)
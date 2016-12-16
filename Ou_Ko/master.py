'''
master.py
'''
import load_file_names
import load_data
import Calc_CDD

def master(variable,scenario,bc_and_resolution, outpath,season, region):
    file_good =[]
    file_good, modelID = load_file_names.load_file_names(variable,scenario,bc_and_resolution)
    print file_good[:]
#    print modelID
    for fle in file_good:
        print fle
        cubeout =load_data.load_data(fle,-5,25,-10,10)
        for nme in modelID:
            if nme in fle: nc_file = outpath+'/'+str(nme)+'_'+str(season)+'_'+str(region)+'.nc'            
                   
        Calc_CDD.calcDryDays(cubeout,nc_file)
        
if __name__ == "__main__": 
    variable = 'pr'
    scenario = 'historical'
    bc_and_resolution = 'BC_0.5x0.5'
    outpath = '/nfs/see-fs-01_teaching/earv054/metrics_workshop/Ou_Ko'
    season = 'jja'
    region = 'wafrica'
    master(variable,scenario,bc_and_resolution, outpath,season, region) 
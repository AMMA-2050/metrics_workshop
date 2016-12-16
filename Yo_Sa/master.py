'''
master.py
'''
import load_file_names
import load_data
import calc_numberdays30mm

def master(variable,scenario,bc_and_resolution,outpath,season,region):
   # files_good = load_file_names.load_file_names(variable,scenario,bc_and_resolution)
    files_good, modelID = load_file_names.load_file_names(variable,scenario,bc_and_resolution)
    print files_good[:]
    print modelID
    for fle in files_good:
        cubeout = load_data.load_data(fle,-5,25,-10,10)
        for nme in modelID:
             if nme in fle: nc_file = outpath+'/'+str(nme)+'_'+str(season)+'_'+str(region)+'.nc' 
           
        calc_numberdays30mm.calc_numberdays30mm(cubeout,'full_year',nc_file)
        
if __name__ == "__main__":
    master(variable,scenario,bc_and_resolution)
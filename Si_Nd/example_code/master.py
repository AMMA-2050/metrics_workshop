'''
master.py
'''
import iris
import load_file_names
import load_data
#import calc_mean_temp 
#import plot_Func #to plot map
import plot_1D
import compute_times_series
import low_pass_weights
import plot_Tfilter

def master():
    variable = 'tas'
    scenario = 'historical'
    bc_and_resolution= 'BC_0.5x0.5'
    season = 'full_year'
    region = 'SAHEL'
    outpath= '/nfs/see-fs-01_teaching/earv053/metrics_workshop/plots'
    files_good, modelID = load_file_names.load_file_names(variable,scenario,bc_and_resolution )
    print files_good[:]
    print modelID
    
    for file in files_good:
        
        cubeout = load_data.load_data(file,-20,20,8,20)
        for nme in modelID:
            if nme in file:
                ncfile= outpath+'/'+ str(scenario)+'_'+ str(variable)+'_'+ str(bc_and_resolution)+'_'+ str(nme)+'_'+str(season)+'_'+str(region)+'.nc'
                figpath=outpath+'/'+ str(scenario)+'_'+ str(variable)+'_'+ str(bc_and_resolution)+'_'+ str(nme)+'_'+str(season)+'_'+str(region)+'/'
                    
            
            
        try:
            iris.load(ncfile)
        except IOError:
            
            
            #cube2plot = calc_hovmuller_precip(cube_out)
            #ncfile = ''
            #cube2plot = calc_mean_temp.calc_mean_temp(cubeout, 'month',ncfile)
            cube1plot = compute_times_series.compute_times_series(cubeout,ncfile)

            window = 121
            # Construct 2-year (24-month) and 7-year (84-month) low pass filters
           # for the Tas data which is monthly.
            wgts24 = low_pass_weights.low_pass_weights(window, 1. / 24.)  #
            wgts84 = low_pass_weights.low_pass_weights(window, 1. / 84.)
            cube1plot24 = cube1plot.rolling_window('time',
                               iris.analysis.MEAN,
                               len(wgts24),
                               weights=wgts24)    
            
            cube1plot84 = cube1plot.rolling_window('time',
                               iris.analysis.SUM,
                               len(wgts84),
                               weights=wgts84)   
            plot_Tfilter.plot_Tfilter(cube1plot,cube1plot24,cube1plot84,figpath)                     
            #cube1plot = compute_times_series.compute_times_series(cubeout,ncfile)
            plot_1D.plot_1D(cube1plot,figpath)
           # example plot one mnonth
#        for mnth in range(0,12):
#            cube2plot_mon = cube2plot[mnth]
#            title_name='monthly climatology'+' '+str(mnth)+' '+str(scenario)+' '+ str(variable)+' '+str(bc_and_resolution)+' '+str(nme)
            #print 
            #plot_Func.plot_Func(cube2plot_mon,outpath,mnth,10, xstart=-20,xend=20, ystart=8,yend=20,title_name)
#            plot_Func.plot_Func(cube2plot_mon,figpath,mnth,10, -20,20, 8,20,title_name)

            #cube2plot_seas = calc_mean_temp.calc_mean_temp(cubeout, 'season',ncfile)
            #plotFunc(cube2plot_seas, figdir)
            #plotFunc(cube2plot, figdir)
if __name__ == "__main__":
    master()

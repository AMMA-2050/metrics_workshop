'''
this is a code to calculate Cumulative  dry  day from CMIP5 data
Autor: Oumar  KONTE, December 2016

'''
import os
import iris 
import iris.coord_categorisation
import iris.quickplot as qplt
import numpy as np
import matplotlib.pyplot as plt

def main():
    
    figpath = '/nfs/see-fs-01_teaching/earv054/metrics_workshop/Ou_Ko/plot'    
     
    precip = iris.load_cube('/nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/IPSL-CM5A-LR/historical/pr_WFDEI_1979-2013_0.5x0.5_day_IPSL-CM5A-LR_africa_historical_r1i1p1_full.nc')
    print precip
    prcp = precip.intersection(latitude=(4.0,25.0), longitude=(-10, 10.0))
    print prcp
    iris.coord_categorisation.add_month(prcp, 'time', name='month')
    dry = iris.Constraint(month = lambda cell: 5<= cell <= 7)
    prcp.extract(dry)
   
    cube2plot =  prcp.aggregated_by('season',iris.analysis.MEAN)  
    
    
    
    
    
    
    



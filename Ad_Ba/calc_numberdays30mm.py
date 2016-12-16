'''
calc_numberdays30mm.py
'''

import iris
import numpy as np
import scipy as sci
import iris.coord_categorisation

def calc_numberdays30mm(precip,season,ncfile):
    
    print "This is the calc script"
    iris.coord_categorisation.add_month_number(precip, 'time', name='month')
    print(precip)
    val=30.0
    bigger = precip.aggregated_by('month', iris.analysis.COUNT, function = lambda values: values > val )
    monthcount = precip.aggregated_by('month', iris.analysis.COUNT, function = lambda values: values > -5000)
    monthcount.data = monthcount.data.astype(float)
    print bigger
    print monthcount.data
    aug = bigger/monthcount
    print ncfile
    iris.save(aug,ncfile)

if __name__ == "__main__":
    calc_numberdays30mm(precip,season,ncfile)

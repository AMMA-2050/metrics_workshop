#########################################
#
# calc_CDD
#
#########################################
import numpy as np
import matplotlib.pyplot as plt
import iris
import iris.coord_categorisation

def calc_CDD(incube,outfile):
    iris.coord_categorisation.add_day_of_month(incube, 'time', name='day_of_month')
    iris.coord_categorisation.add_year(incube, 'time', name='year')
    incube.convert_units('kg m-2 day-1')
    #year0 = incube.coord('year').points[0]
    # creates a cube for putting data into
    outcube = incube.aggregated_by('year', iris.analysis.MEAN)
    #the rainfall threshold
    total = 1.0
    # first bring in the data
    # this code will need to know the starting day of the data
    for yr in incube.coord('year').points:
        #pdb.set_trace()
        incube_yr = incube.extract(iris.Constraint(year=yr))
        
        strt_day = incube_yr.coord('day_of_month').points[0]   
        yeardata = incube_yr.data
        dtes = []
        duration = []
        pltdtes = np.zeros((yeardata.shape[1],yeardata.shape[2]),dtype = int)
        pltdur = np.zeros((yeardata.shape[1],yeardata.shape[2]),dtype = int)
        for x in range(0,yeardata.shape[2]):
            for y in range(0,yeardata.shape[1]):
                current_max = 0
                current_dte = 0
                dte = 0
                duratn = 0   
                for t in range(0,yeardata.shape[0]):
                    if yeardata[t,y,x] <= float(total):
                        dte = t
                        print dte, yeardata[t,y,x]
                        for t1 in xrange(t,yeardata.shape[0]): 
                            if yeardata[t1,y,x] <= float(total):
                                continue
                            else:
                                duratn = t1 - t
                                if duratn > current_max:
                                    current_dte = dte + strt_day
                                    current_max = duratn
                            break
            dtes.extend([current_dte])
            duration.extend([current_max])
            pltdtes[y,x] = current_dte
            pltdur[y,x] = current_max
                  
  
        #                else:
        #                  continue
        #                break                            
        #print np.max(duration[:])
        #print np.max(dtes[:])                  
        #   plt.clf()
        #plt.scatter(duration[:],dtes[:])
        #plt.show()    
        #ax1 = plt.figure(figsize = (12,12))
        plt.subplot(2,1,1)
        plt.contourf(pltdtes[:])
        #cb2.set_label('Date of longest dry spell (after onset)')

        plt.subplot(2,1,2)
        plt.contourf(pltdur[:])
        #plt2_ax = ax1.gca()     
        #cb2.set_label('Duration of first dry spell')
        plt.subplots_adjust(hspace = 0.5)
        # plt.savefig('TRMM_CDD_'+str(yyyy)+'_limit'+str(total)+'mm_per_day.png')
        plt.show()
        #outcube[year,:].data = dtes[:]
        outcube[yr,:,:].data = duration
        
        #   np.savetxt('CDD_date_'+str(yyyy)+'.csv', pltdtes[:], delimiter = ',') 
        #   np.savetxt('CDD_duration_'+str(yyyy)+'.csv', pltdur[:], delimiter = ',')       
        return(pltdtes,pltdur)
        
    iris.save(outcube,outfile)        
if "__name__" == "__calc_CDD__":
    total = 1.0
    calc_CDD(incube,outfile)    
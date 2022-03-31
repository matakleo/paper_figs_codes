import csv
from tokenize import Ignore
from all_functions import Extract_the_shit2,Extract_by_name,Extract_Track_Data,list_csv_files_0, calculate_distance_error,calculate_intensity_error,calculate_intensity_error_slp
import matplotlib.gridspec as gridspec
import os
import numpy as np
import matplotlib.pyplot as plt

def gimme_errors_tribars_lvls(PBL):
    Input_Dir = '/Users/lmatak/Desktop/leo_simulations/WRF_Output_PBLHS/diff_hpbls'
    Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'
    HNS = ['Maria','Lorenzo','Iota','Dorian','Igor']
    GSS = ['8km']
    TM = 'NoTurb'
    PBLS = PBL
    CLS = ['lvl_3','lvl_5','1.0','lvl_7']
    list_of_slp_errors=[]
    slp_percentile=[]
    wind_percentile_20 = []
    wind_percentile_80 = []
    track_percentile_20 = []
    track_percentile_80 = []
    slp_percentile_20 = []
    slp_percentile_80 = []
    list_of_wind_errors=[]
    wind_percentile=[]
    track_percentile=[]
    list_of_track_errors=[]
    for GS in GSS:
        all_hurs_track_error_list=[]
        all_hurs_wind_intensity_error_list=[]
        all_hurs_min_slp_error_list=[]
        List_for_CSV_files=[]
        for CL in CLS:
            List_for_CSV_files.append(PBL+'_hpbl_'+CL)

        for HN in HNS:

            Hurricane_Dir =Input_Dir + '/' + HN + '/' + GS + '/' + TM +'/Standard/'  
            Real_Hurricane_Data = Real_data_dir+'/Real_Data_'+HN+'.csv'

            Real_Lats = []
            Real_Longs = []
            Real_Lats = Extract_Track_Data (Real_data_dir, Real_Lats, 'Lat',HN)
            Real_Longs = Extract_Track_Data (Real_data_dir, Real_Longs, 'Lon',HN)

            Real_slp=[]
            Real_slp = Extract_by_name(Real_Hurricane_Data,Real_slp,'Pressure (mb) ')

            Real_Winds=[]
            Real_Winds = Extract_by_name(Real_Hurricane_Data,Real_Winds,'Wind Speed(kt)')

            csv_files=list_csv_files_0(Hurricane_Dir,List_for_CSV_files)
            
            error_list_track=[]
            error_list_wind_intensity=[]
            error_list_min_slp=[]
            for csv_file in csv_files:

                Eye_Lats=[]
                Eye_Longs=[]
                simulated_wind_intensities=[]
                simulated_min_slp=[]

                Eye_Lats=Extract_by_name(csv_file,Eye_Lats,'min_lat')
                Eye_Longs=Extract_by_name(csv_file,Eye_Longs,'min_long')
                simulated_wind_intensities=Extract_by_name(csv_file,simulated_wind_intensities,'All_Max_WND_SPD_10')
                simulated_min_slp=Extract_by_name(csv_file,simulated_min_slp,'min_slp')

                number = (int((len(Eye_Lats)-1)/(len(Real_Lats)-1)))
                if number == 0:
                    number =1
                Eye_Lats2=[]
                Eye_Longs2=[]
                simulated_wind_intensities2=[]
                simulated_min_slp2=[]
                for i in range(len(Eye_Lats)):


                    Eye_Lats2.append(Eye_Lats[i*number])
                    Eye_Longs2.append(Eye_Longs[i*number])
                    simulated_wind_intensities2.append(simulated_wind_intensities[i*number])
                    simulated_min_slp2.append(simulated_min_slp[i*number])



                error_list_track.append(calculate_distance_error(Eye_Lats2, Eye_Longs2, Real_Lats[0:len(Eye_Lats2)], Real_Longs[0:len(Eye_Lats2)]))
        
                error_list_wind_intensity.append(calculate_intensity_error(simulated_wind_intensities2,Real_Winds))
                error_list_min_slp.append(calculate_intensity_error_slp(simulated_min_slp2,Real_slp))
            # print('error_list_track:',error_list_track)
            all_hurs_track_error_list.append(error_list_track)
            all_hurs_wind_intensity_error_list.append(error_list_wind_intensity)
            all_hurs_min_slp_error_list.append(error_list_min_slp)
            # print(all_hurs_min_slp_error_list)
        
        all_hurs_min_slp_error_list=np.array(all_hurs_min_slp_error_list)       
        # print(all_hurs_min_slp_error_list)
        all_hurs_wind_intensity_error_list=np.array(all_hurs_wind_intensity_error_list)
        all_hurs_track_error_list=np.array(all_hurs_track_error_list)
        # print(all_hurs_wind_intensity_error_list)
        #PERCENTILE ERRORS
        for i in range(len(CLS)):
            wind_percentile_20.append(np.percentile(all_hurs_wind_intensity_error_list[:,i],20))
            wind_percentile_80.append(np.percentile(all_hurs_wind_intensity_error_list[:,i],80))
            track_percentile_20.append(np.percentile(all_hurs_track_error_list[:,i],20))
            track_percentile_80.append(np.percentile(all_hurs_track_error_list[:,i],80))
            slp_percentile_80.append(np.percentile(all_hurs_min_slp_error_list[:,i],80))
            slp_percentile_20.append(np.percentile(all_hurs_min_slp_error_list[:,i],20))
        
        
        # print('yay')
        # print(all_hurs_track_error_list)

        #plotting#

        avg_track=[]
        avg_wind=[]
        avg_slp=[]

        for i in range(len(error_list_track)):
            # print('i=',i)
            avg_track.append(np.average(all_hurs_track_error_list[:,i]))
            avg_wind.append(np.average(all_hurs_wind_intensity_error_list[:,i]))
            avg_slp.append(np.average(all_hurs_min_slp_error_list[:,i]))

        list_of_wind_errors.append(avg_wind)
        list_of_track_errors.append(avg_track)
        list_of_slp_errors.append(avg_slp)
        

        wind_percentile = []
        track_percentile = []
        slp_percentile = []
        print('list of errors track',list_of_track_errors)
        print('list of track perc 20: ', track_percentile_20)
        for i in range(len(wind_percentile_20)):
            wind_percentile.append([[float(list_of_wind_errors[0][i]-wind_percentile_20[i])],[float(wind_percentile_80[i]-list_of_wind_errors[0][i])]])
            track_percentile.append([[float(list_of_track_errors[0][i]-track_percentile_20[i])],[float(track_percentile_80[i]-list_of_track_errors[0][i])]])
            slp_percentile.append([[float(list_of_slp_errors[0][i]-slp_percentile_20[i])],[float(slp_percentile_80[i]-list_of_slp_errors[0][i])]])
            # slp_percentile.append([[float(list_of_track_errors[i]-track_percentile_20[i])],[float(track_percentile_80[i]-list_of_track_errors[i])]])
        print(PBL+' track percentil 80: ',track_percentile_80)
        print(PBL+' track percentil 20: ',track_percentile_20)
        print('track_percentile for grafs',track_percentile)
        # print('track 80',track_percentile)
    return(list_of_wind_errors,list_of_track_errors,list_of_slp_errors,wind_percentile,track_percentile,slp_percentile)

# gimme_errors_tribars_lvls('YSU')


def gimme_errors_tribars_xkzm(PBL):
    Input_Dir = '/Users/lmatak/Desktop/leo_simulations/WRF_Output_PBLHS/diff_hpbls'
    Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'
    HNS = ['Maria','Lorenzo','Iota','Dorian','Igor']
    GSS = ['8km']
    TM = 'NoTurb'
    PBLS = PBL
    CLS = ['xkzm_0.20','1.0','xkzm_5.0']
    if PBL=='MYJ':
        CLS = ['km_0.20','1.0','km_5.0']
    list_of_slp_errors=[]
    slp_percentile=[]
    wind_percentile_20 = []
    wind_percentile_80 = []
    track_percentile_20 = []
    track_percentile_80 = []
    slp_percentile_20 = []
    slp_percentile_80 = []
    list_of_wind_errors=[]
    wind_percentile=[]
    track_percentile=[]
    list_of_track_errors=[]
    for GS in GSS:
        all_hurs_track_error_list=[]
        all_hurs_wind_intensity_error_list=[]
        all_hurs_min_slp_error_list=[]
        List_for_CSV_files=[]
        for CL in CLS:
            List_for_CSV_files.append(PBL+'_hpbl_'+CL)

        for HN in HNS:

            Hurricane_Dir =Input_Dir + '/' + HN + '/' + GS + '/' + TM +'/Standard/'  
            Real_Hurricane_Data = Real_data_dir+'/Real_Data_'+HN+'.csv'

            Real_Lats = []
            Real_Longs = []
            Real_Lats = Extract_Track_Data (Real_data_dir, Real_Lats, 'Lat',HN)
            Real_Longs = Extract_Track_Data (Real_data_dir, Real_Longs, 'Lon',HN)

            Real_slp=[]
            Real_slp = Extract_by_name(Real_Hurricane_Data,Real_slp,'Pressure (mb) ')

            Real_Winds=[]
            Real_Winds = Extract_by_name(Real_Hurricane_Data,Real_Winds,'Wind Speed(kt)')

            csv_files=list_csv_files_0(Hurricane_Dir,List_for_CSV_files)
            
            error_list_track=[]
            error_list_wind_intensity=[]
            error_list_min_slp=[]
            for csv_file in csv_files:

                Eye_Lats=[]
                Eye_Longs=[]
                simulated_wind_intensities=[]
                simulated_min_slp=[]

                Eye_Lats=Extract_by_name(csv_file,Eye_Lats,'min_lat')
                Eye_Longs=Extract_by_name(csv_file,Eye_Longs,'min_long')
                simulated_wind_intensities=Extract_by_name(csv_file,simulated_wind_intensities,'All_Max_WND_SPD_10')
                simulated_min_slp=Extract_by_name(csv_file,simulated_min_slp,'min_slp')

                number = (int((len(Eye_Lats)-1)/(len(Real_Lats)-1)))
                if number == 0:
                    number =1
                Eye_Lats2=[]
                Eye_Longs2=[]
                simulated_wind_intensities2=[]
                simulated_min_slp2=[]
                for i in range(len(Eye_Lats)):


                    Eye_Lats2.append(Eye_Lats[i*number])
                    Eye_Longs2.append(Eye_Longs[i*number])
                    simulated_wind_intensities2.append(simulated_wind_intensities[i*number])
                    simulated_min_slp2.append(simulated_min_slp[i*number])



                error_list_track.append(calculate_distance_error(Eye_Lats2, Eye_Longs2, Real_Lats[0:len(Eye_Lats2)], Real_Longs[0:len(Eye_Lats2)]))
        
                error_list_wind_intensity.append(calculate_intensity_error(simulated_wind_intensities2,Real_Winds))
                error_list_min_slp.append(calculate_intensity_error_slp(simulated_min_slp2,Real_slp))
            # print('error_list_track:',error_list_track)
            all_hurs_track_error_list.append(error_list_track)
            all_hurs_wind_intensity_error_list.append(error_list_wind_intensity)
            all_hurs_min_slp_error_list.append(error_list_min_slp)

        all_hurs_min_slp_error_list=np.array(all_hurs_min_slp_error_list)       
        all_hurs_wind_intensity_error_list=np.array(all_hurs_wind_intensity_error_list)
        all_hurs_track_error_list=np.array(all_hurs_track_error_list)
        
        #PERCENTILE ERRORS
        for i in range(len(CLS)):
            wind_percentile_20.append(np.percentile(all_hurs_wind_intensity_error_list[:,i],20))
            wind_percentile_80.append(np.percentile(all_hurs_wind_intensity_error_list[:,i],80))
            track_percentile_20.append(np.percentile(all_hurs_track_error_list[:,i],20))
            track_percentile_80.append(np.percentile(all_hurs_track_error_list[:,i],80))
            slp_percentile_80.append(np.percentile(all_hurs_min_slp_error_list[:,i],80))
            slp_percentile_20.append(np.percentile(all_hurs_min_slp_error_list[:,i],20))
        
        # print('yay')
        # print(all_hurs_track_error_list)

        #plotting#

        avg_track=[]
        avg_wind=[]
        avg_slp=[]

        for i in range(len(error_list_track)):
            # print('i=',i)
            avg_track.append(np.average(all_hurs_track_error_list[:,i]))
            avg_wind.append(np.average(all_hurs_wind_intensity_error_list[:,i]))
            avg_slp.append(np.average(all_hurs_min_slp_error_list[:,i]))

        list_of_wind_errors.append(avg_wind)
        list_of_track_errors.append(avg_track)
        list_of_slp_errors.append(avg_slp)
        # print(list_of_wind_errors)
        wind_percentile = []
        track_percentile = []
        slp_percentile = []
        print('list of errors track',list_of_track_errors)
        print('list of track perc 20: ', track_percentile_20)
        for i in range(len(wind_percentile_20)):
            wind_percentile.append([[float(list_of_wind_errors[0][i]-wind_percentile_20[i])],[float(wind_percentile_80[i]-list_of_wind_errors[0][i])]])
            track_percentile.append([[float(list_of_track_errors[0][i]-track_percentile_20[i])],[float(track_percentile_80[i]-list_of_track_errors[0][i])]])
            slp_percentile.append([[float(list_of_slp_errors[0][i]-slp_percentile_20[i])],[float(slp_percentile_80[i]-list_of_slp_errors[0][i])]])
            # slp_percentile.append([[float(list_of_track_errors[i]-track_percentile_20[i])],[float(track_percentile_80[i]-list_of_track_errors[i])]])
        print(PBL+' track percentil 80: ',track_percentile_80)
        print(PBL+' track percentil 20: ',track_percentile_20)
        print('track_percentile for grafs',track_percentile)
        # print('track 80',track_percentile)

    return(list_of_wind_errors,list_of_track_errors,list_of_slp_errors,wind_percentile,track_percentile,slp_percentile)




def radius_of_max_wind_lvls(PBL):
    Input_Dir = '/Users/lmatak/Desktop/leo_simulations/WRF_Output_PBLHS/diff_hpbls'
    Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'
    HNS = ['Teddy','Maria','Lorenzo','Iota','Dorian','Igor']
    GS = '8km'
    TM = 'NoTurb'
    percentile=[]
    PBLS = PBL
    final_out_list=[]
    CLS = ['lvl_3','lvl_5','1.0','lvl_7']
    # CLS= ['xkzm_0.25_lvl_2',]
    all_hurs_max_wind_rads=[]
    for HN in HNS :

        Input_Dir_1 = Input_Dir + '/' + HN + '/' + GS + '/' + TM + '/WSPD_R/'
        Real_Hurricane_Data = Real_data_dir+'/Real_Data_'+HN+'.csv'

        list_of_max_wind_radius =[]
    
        for CL in CLS:

                #by hurricane setting you define the name of the csv file e.g. /Irma_32km_NoTurb_YSU_hpbl_250.csv/
                Hurricane_Setting = HN + '_' + GS + '_' + TM + '_' + PBL +'_hpbl_'+CL +'.csv'		




                # print(Hurricane_Setting)
                csv_file = (Input_Dir_1+Hurricane_Setting)
                
                # you define empty lists which will contain the extracted data from the csv file, and plot them immediatle
                WSPD = []
                rads=[]

                rads=Extract_the_shit2(csv_file, rads,'Radiuses')
                WSPD=Extract_the_shit2(csv_file, WSPD,' Average_WSPD')

                list_of_max_wind_radius.append(rads[np.where(WSPD == np.max(WSPD))[0][0]])
                # print(np.max(WSPD))
        all_hurs_max_wind_rads.append(list_of_max_wind_radius)
    all_hurs_max_wind_rads=np.array(all_hurs_max_wind_rads)
    percentile_20=[]
    percentile_80=[]
    for i in range(len(CLS)):
        # print('mean is: ', np.average(all_hurs_max_wind_rads[:,i]),' and 80th perc is: ',np.percentile(all_hurs_max_wind_rads[:,i],80))
        percentile_80.append([np.percentile(all_hurs_max_wind_rads[:,i],80)-np.average(all_hurs_max_wind_rads[:,i])])
        percentile_20.append([np.average(all_hurs_max_wind_rads[:,i])-np.percentile(all_hurs_max_wind_rads[:,i],20)])
        percentile.append([percentile_20[i],percentile_80[i]])
        
        # percentile_20.append([[all_hurs_max_wind_rads[:,i]-np.percentile(all_hurs_max_wind_rads[:,i],20)],[np.percentile(all_hurs_max_wind_rads[:,i],80)-all_hurs_max_wind_rads[:,i]]])

        final_out_list.append(np.average(all_hurs_max_wind_rads[:,i]))
    # print(percentile)
    # print(percentile_20)
    print(percentile)

    return(final_out_list,percentile)

# radius_of_max_wind('YSU')
# gimme_errors_tribars_lvls('YSU')

def radius_of_max_wind_xkzm(PBL):
    Input_Dir = '/Users/lmatak/Desktop/leo_simulations/WRF_Output_PBLHS/diff_hpbls'
    Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'
    HNS = ['Teddy','Maria','Lorenzo','Iota','Dorian','Igor']
    GS = '8km'
    TM = 'NoTurb'
    percentile=[]
    PBLS = PBL
    final_out_list=[]
    CLS= ['xkzm_0.125','1.0_xkzm','xkzm_8.0']
    if PBL == 'MYJ':
        CLS = ['km_0.25_lvl_2','1.0_xkzm','km_4.0_lvl_2']
    
    all_hurs_max_wind_rads=[]
    for HN in HNS :

        Input_Dir_1 = Input_Dir + '/' + HN + '/' + GS + '/' + TM + '/WSPD_R/'
        Real_Hurricane_Data = Real_data_dir+'/Real_Data_'+HN+'.csv'

        list_of_max_wind_radius =[]
    
        for CL in CLS:

                #by hurricane setting you define the name of the csv file e.g. /Irma_32km_NoTurb_YSU_hpbl_250.csv/
                Hurricane_Setting = HN + '_' + GS + '_' + TM + '_' + PBL +'_hpbl_'+CL +'.csv'		




                # print(Hurricane_Setting)
                csv_file = (Input_Dir_1+Hurricane_Setting)
                
                # you define empty lists which will contain the extracted data from the csv file, and plot them immediatle
                WSPD = []
                rads=[]

                rads=Extract_the_shit2(csv_file, rads,'Radiuses')
                WSPD=Extract_the_shit2(csv_file, WSPD,' Average_WSPD')

                list_of_max_wind_radius.append(rads[np.where(WSPD == np.max(WSPD))[0][0]])
                # print(np.max(WSPD))
        all_hurs_max_wind_rads.append(list_of_max_wind_radius)
    all_hurs_max_wind_rads=np.array(all_hurs_max_wind_rads)
    percentile_20=[]
    percentile_80=[]
    for i in range(len(CLS)):
        # print('mean is: ', np.average(all_hurs_max_wind_rads[:,i]),' and 80th perc is: ',np.percentile(all_hurs_max_wind_rads[:,i],80))
        percentile_80.append([np.percentile(all_hurs_max_wind_rads[:,i],80)-np.average(all_hurs_max_wind_rads[:,i])])
        percentile_20.append([np.average(all_hurs_max_wind_rads[:,i])-np.percentile(all_hurs_max_wind_rads[:,i],20)])
        percentile.append([percentile_20[i],percentile_80[i]])
        
        # percentile_20.append([[all_hurs_max_wind_rads[:,i]-np.percentile(all_hurs_max_wind_rads[:,i],20)],[np.percentile(all_hurs_max_wind_rads[:,i],80)-all_hurs_max_wind_rads[:,i]]])

        final_out_list.append(np.average(all_hurs_max_wind_rads[:,i]))
    # print(percentile)
    # print(percentile_20)
    print(percentile)

    return(final_out_list,percentile)



def gimme_errors_tribars_fixes_HBLS(PBL):
    Input_Dir = '/Users/lmatak/Desktop/leo_simulations/WRF_Output_PBLHS/diff_hpbls'
    Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'
    HNS = ['Teddy','Maria','Lorenzo','Iota','Dorian','Igor']
    GSS = ['8km']
    TM = 'NoTurb'
    PBLS = PBL
    CLS = ['250','1.0','2000']
    list_of_slp_errors=[]
    slp_percentile=[]
    wind_percentile_20 = []
    wind_percentile_80 = []
    track_percentile_20 = []
    track_percentile_80 = []
    slp_percentile_20 = []
    slp_percentile_80 = []
    list_of_wind_errors=[]
    wind_percentile=[]
    track_percentile=[]
    list_of_track_errors=[]
    for GS in GSS:
        all_hurs_track_error_list=[]
        all_hurs_wind_intensity_error_list=[]
        all_hurs_min_slp_error_list=[]
        List_for_CSV_files=[]
        for CL in CLS:
            List_for_CSV_files.append(PBL+'_hpbl_'+CL)

        for HN in HNS:

            Hurricane_Dir =Input_Dir + '/' + HN + '/' + GS + '/' + TM +'/Standard/'  
            Real_Hurricane_Data = Real_data_dir+'/Real_Data_'+HN+'.csv'

            Real_Lats = []
            Real_Longs = []
            Real_Lats = Extract_Track_Data (Real_data_dir, Real_Lats, 'Lat',HN)
            Real_Longs = Extract_Track_Data (Real_data_dir, Real_Longs, 'Lon',HN)

            Real_slp=[]
            Real_slp = Extract_by_name(Real_Hurricane_Data,Real_slp,'Pressure (mb) ')

            Real_Winds=[]
            Real_Winds = Extract_by_name(Real_Hurricane_Data,Real_Winds,'Wind Speed(kt)')

            csv_files=list_csv_files_0(Hurricane_Dir,List_for_CSV_files)
            
            error_list_track=[]
            error_list_wind_intensity=[]
            error_list_min_slp=[]
            for csv_file in csv_files:

                Eye_Lats=[]
                Eye_Longs=[]
                simulated_wind_intensities=[]
                simulated_min_slp=[]

                Eye_Lats=Extract_by_name(csv_file,Eye_Lats,'min_lat')
                Eye_Longs=Extract_by_name(csv_file,Eye_Longs,'min_long')
                simulated_wind_intensities=Extract_by_name(csv_file,simulated_wind_intensities,'All_Max_WND_SPD_10')
                simulated_min_slp=Extract_by_name(csv_file,simulated_min_slp,'min_slp')

                number = (int((len(Eye_Lats)-1)/(len(Real_Lats)-1)))
                if number == 0:
                    number =1
                Eye_Lats2=[]
                Eye_Longs2=[]
                simulated_wind_intensities2=[]
                simulated_min_slp2=[]
                for i in range(len(Eye_Lats)):


                    Eye_Lats2.append(Eye_Lats[i*number])
                    Eye_Longs2.append(Eye_Longs[i*number])
                    simulated_wind_intensities2.append(simulated_wind_intensities[i*number])
                    simulated_min_slp2.append(simulated_min_slp[i*number])



                error_list_track.append(calculate_distance_error(Eye_Lats2, Eye_Longs2, Real_Lats[0:len(Eye_Lats2)], Real_Longs[0:len(Eye_Lats2)]))
        
                error_list_wind_intensity.append(calculate_intensity_error(simulated_wind_intensities2,Real_Winds))
                error_list_min_slp.append(calculate_intensity_error_slp(simulated_min_slp2,Real_slp))
            # print('error_list_track:',error_list_track)
            all_hurs_track_error_list.append(error_list_track)
            all_hurs_wind_intensity_error_list.append(error_list_wind_intensity)
            all_hurs_min_slp_error_list.append(error_list_min_slp)
            # print(all_hurs_min_slp_error_list)
        
        all_hurs_min_slp_error_list=np.array(all_hurs_min_slp_error_list)       
        # print(all_hurs_min_slp_error_list)
        all_hurs_wind_intensity_error_list=np.array(all_hurs_wind_intensity_error_list)
        all_hurs_track_error_list=np.array(all_hurs_track_error_list)
        # print(all_hurs_wind_intensity_error_list)
        #PERCENTILE ERRORS
        for i in range(len(CLS)):
            wind_percentile_20.append(np.percentile(all_hurs_wind_intensity_error_list[:,i],20))
            wind_percentile_80.append(np.percentile(all_hurs_wind_intensity_error_list[:,i],80))
            track_percentile_20.append(np.percentile(all_hurs_track_error_list[:,i],20))
            track_percentile_80.append(np.percentile(all_hurs_track_error_list[:,i],80))
            slp_percentile_80.append(np.percentile(all_hurs_min_slp_error_list[:,i],80))
            slp_percentile_20.append(np.percentile(all_hurs_min_slp_error_list[:,i],20))
        
        
        # print('yay')
        # print(all_hurs_track_error_list)

        #plotting#

        avg_track=[]
        avg_wind=[]
        avg_slp=[]

        for i in range(len(error_list_track)):
            # print('i=',i)
            avg_track.append(np.average(all_hurs_track_error_list[:,i]))
            avg_wind.append(np.average(all_hurs_wind_intensity_error_list[:,i]))
            avg_slp.append(np.average(all_hurs_min_slp_error_list[:,i]))

        list_of_wind_errors.append(avg_wind)
        list_of_track_errors.append(avg_track)
        list_of_slp_errors.append(avg_slp)
        

        wind_percentile = []
        track_percentile = []
        slp_percentile = []
        print('list of errors track',list_of_track_errors)
        print('list of track perc 20: ', track_percentile_20)
        for i in range(len(wind_percentile_20)):
            wind_percentile.append([[float(list_of_wind_errors[0][i]-wind_percentile_20[i])],[float(wind_percentile_80[i]-list_of_wind_errors[0][i])]])
            track_percentile.append([[float(list_of_track_errors[0][i]-track_percentile_20[i])],[float(track_percentile_80[i]-list_of_track_errors[0][i])]])
            slp_percentile.append([[float(list_of_slp_errors[0][i]-slp_percentile_20[i])],[float(slp_percentile_80[i]-list_of_slp_errors[0][i])]])
            # slp_percentile.append([[float(list_of_track_errors[i]-track_percentile_20[i])],[float(track_percentile_80[i]-list_of_track_errors[i])]])
        print(PBL+' track percentil 80: ',track_percentile_80)
        print(PBL+' track percentil 20: ',track_percentile_20)
        print('track_percentile for grafs',track_percentile)
        # print('track 80',track_percentile)
    return(list_of_wind_errors,list_of_track_errors,list_of_slp_errors,wind_percentile,track_percentile,slp_percentile)



def max_windsp_lvls(PBL):
    Input_Dir = '/Users/lmatak/Desktop/leo_simulations/WRF_Output_PBLHS/diff_hpbls'
    Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'
    HNS = ['Teddy','Maria','Lorenzo','Iota','Dorian','Igor']
    GS = '8km'
    TM = 'NoTurb'
    percentile=[]
    PBLS = PBL
    final_out_list=[]
    CLS= ['lvl_3','lvl_5','1.0','lvl_7']
    # if PBL == 'MYJ':
    #     CLS = ['km_0.25_lvl_2','1.0','km_4.0_lvl_2']
    
    all_hurs_max_wind_rads=[]
    for HN in HNS :

        Input_Dir_1 = Input_Dir + '/' + HN + '/' + GS + '/' + TM + '/WSPD_R/'
        Real_Hurricane_Data = Real_data_dir+'/Real_Data_'+HN+'.csv'

        list_of_max_wind_radius =[]
    
        for CL in CLS:

                #by hurricane setting you define the name of the csv file e.g. /Irma_32km_NoTurb_YSU_hpbl_250.csv/
                Hurricane_Setting = HN + '_' + GS + '_' + TM + '_' + PBL +'_hpbl_'+CL +'.csv'		




                # print(Hurricane_Setting)
                csv_file = (Input_Dir_1+Hurricane_Setting)
                
                # you define empty lists which will contain the extracted data from the csv file, and plot them immediatle
                WSPD = []
                rads=[]

                rads=Extract_the_shit2(csv_file, rads,'Radiuses')
                WSPD=Extract_the_shit2(csv_file, WSPD,' Average_WSPD')

                list_of_max_wind_radius.append(np.max(WSPD))
                # print(np.max(WSPD))
        all_hurs_max_wind_rads.append(list_of_max_wind_radius)
    all_hurs_max_wind_rads=np.array(all_hurs_max_wind_rads)
    percentile_20=[]
    percentile_80=[]
    for i in range(len(CLS)):
        # print('mean is: ', np.average(all_hurs_max_wind_rads[:,i]),' and 80th perc is: ',np.percentile(all_hurs_max_wind_rads[:,i],80))
        percentile_80.append([np.percentile(all_hurs_max_wind_rads[:,i],80)-np.average(all_hurs_max_wind_rads[:,i])])
        percentile_20.append([np.average(all_hurs_max_wind_rads[:,i])-np.percentile(all_hurs_max_wind_rads[:,i],20)])
        percentile.append([percentile_20[i],percentile_80[i]])
        
        # percentile_20.append([[all_hurs_max_wind_rads[:,i]-np.percentile(all_hurs_max_wind_rads[:,i],20)],[np.percentile(all_hurs_max_wind_rads[:,i],80)-all_hurs_max_wind_rads[:,i]]])

        final_out_list.append(np.average(all_hurs_max_wind_rads[:,i]))
    # print(percentile)
    print(final_out_list)
    print(percentile)

    return(final_out_list,percentile)



def max_windsp_xkzm(PBL):
    Input_Dir = '/Users/lmatak/Desktop/leo_simulations/WRF_Output_PBLHS/diff_hpbls'
    Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'
    HNS = ['Teddy','Maria','Lorenzo','Iota','Dorian','Igor']
    GS = '8km'
    TM = 'NoTurb'
    percentile=[]
    PBLS = PBL
    final_out_list=[]
    CLS= ['xkzm_0.25_lvl_2','1.0','xkzm_4.0_lvl_2']
    if PBL == 'MYJ':
        CLS = ['km_0.25_lvl_2','1.0','km_4.0_lvl_2']
    
    all_hurs_max_wind_rads=[]
    for HN in HNS :

        Input_Dir_1 = Input_Dir + '/' + HN + '/' + GS + '/' + TM + '/WSPD_R/'
        Real_Hurricane_Data = Real_data_dir+'/Real_Data_'+HN+'.csv'

        list_of_max_wind_radius =[]
    
        for CL in CLS:

                #by hurricane setting you define the name of the csv file e.g. /Irma_32km_NoTurb_YSU_hpbl_250.csv/
                Hurricane_Setting = HN + '_' + GS + '_' + TM + '_' + PBL +'_hpbl_'+CL +'.csv'		




                # print(Hurricane_Setting)
                csv_file = (Input_Dir_1+Hurricane_Setting)
                
                # you define empty lists which will contain the extracted data from the csv file, and plot them immediatle
                WSPD = []
                rads=[]

                rads=Extract_the_shit2(csv_file, rads,'Radiuses')
                WSPD=Extract_the_shit2(csv_file, WSPD,' Average_WSPD')

                list_of_max_wind_radius.append(np.max(WSPD))
                # print(np.max(WSPD))
        all_hurs_max_wind_rads.append(list_of_max_wind_radius)
    all_hurs_max_wind_rads=np.array(all_hurs_max_wind_rads)
    percentile_20=[]
    percentile_80=[]
    for i in range(len(CLS)):
        # print('mean is: ', np.average(all_hurs_max_wind_rads[:,i]),' and 80th perc is: ',np.percentile(all_hurs_max_wind_rads[:,i],80))
        percentile_80.append([np.percentile(all_hurs_max_wind_rads[:,i],80)-np.average(all_hurs_max_wind_rads[:,i])])
        percentile_20.append([np.average(all_hurs_max_wind_rads[:,i])-np.percentile(all_hurs_max_wind_rads[:,i],20)])
        percentile.append([percentile_20[i],percentile_80[i]])
        
        # percentile_20.append([[all_hurs_max_wind_rads[:,i]-np.percentile(all_hurs_max_wind_rads[:,i],20)],[np.percentile(all_hurs_max_wind_rads[:,i],80)-all_hurs_max_wind_rads[:,i]]])

        final_out_list.append(np.average(all_hurs_max_wind_rads[:,i]))
    # print(percentile)
    print(final_out_list)
    print(percentile)

    return(final_out_list,percentile)

def min_SLP_lvls(PBL):
    Input_Dir = '/Users/lmatak/Desktop/leo_simulations/WRF_Output_PBLHS/diff_hpbls'
    Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'
    HNS = ['Maria','Lorenzo','Iota','Dorian','Igor','Teddy']
    GS = '8km'
    TM = 'NoTurb'
    percentile=[]
    PBLS = PBL
    final_out_list=[]
    CLS= ['lvl_3','lvl_5','1.0','lvl_7']

    
    all_hurs_max_wind_rads=[]
    for HN in HNS :

        Input_Dir_1 = Input_Dir + '/' + HN + '/' + GS + '/' + TM + '/WSPD_SLP/'
        Real_Hurricane_Data = Real_data_dir+'/Real_Data_'+HN+'.csv'

        list_of_max_wind_radius =[]
    
        for CL in CLS:

                #by hurricane setting you define the name of the csv file e.g. /Irma_32km_NoTurb_YSU_hpbl_250.csv/
                Hurricane_Setting = HN + '_' + GS + '_' + TM + '_' + PBL +'_hpbl_'+CL +'.csv'		




                # print(Hurricane_Setting)
                csv_file = (Input_Dir_1+Hurricane_Setting)
                print('csv is ' ,csv_file)
                # you define empty lists which will contain the extracted data from the csv file, and plot them immediatle
                min_slps = []


                min_slps=Extract_the_shit2(csv_file, min_slps,'SLPS')
                print(min_slps)


                list_of_max_wind_radius.append(np.min(min_slps))
                # print(np.max(WSPD))
        all_hurs_max_wind_rads.append(list_of_max_wind_radius)
    all_hurs_max_wind_rads=np.array(all_hurs_max_wind_rads)
    percentile_20=[]
    percentile_80=[]
    for i in range(len(CLS)):
        # print('mean is: ', np.average(all_hurs_max_wind_rads[:,i]),' and 80th perc is: ',np.percentile(all_hurs_max_wind_rads[:,i],80))
        percentile_80.append([np.percentile(all_hurs_max_wind_rads[:,i],80)-np.average(all_hurs_max_wind_rads[:,i])])
        percentile_20.append([np.average(all_hurs_max_wind_rads[:,i])-np.percentile(all_hurs_max_wind_rads[:,i],20)])
        percentile.append([percentile_20[i],percentile_80[i]])
        
        # percentile_20.append([[all_hurs_max_wind_rads[:,i]-np.percentile(all_hurs_max_wind_rads[:,i],20)],[np.percentile(all_hurs_max_wind_rads[:,i],80)-all_hurs_max_wind_rads[:,i]]])

        final_out_list.append(np.average(all_hurs_max_wind_rads[:,i]))
    # print(percentile)
    print(final_out_list)
    print(percentile)

    return(final_out_list,percentile)


def min_SLP_xkzm(PBL):
    Input_Dir = '/Users/lmatak/Desktop/leo_simulations/WRF_Output_PBLHS/diff_hpbls'
    Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'
    HNS = ['Maria','Lorenzo','Iota','Dorian','Igor','Teddy']
    GS = '8km'
    TM = 'NoTurb'
    percentile=[]
    PBLS = PBL
    final_out_list=[]
    CLS= ['xkzm_0.25_lvl_2','1.0','xkzm_4.0_lvl_2']
    if PBL == 'MYJ':
        CLS = ['km_0.25_lvl_2','1.0','km_4.0_lvl_2']
    
    all_hurs_max_wind_rads=[]
    for HN in HNS :

        Input_Dir_1 = Input_Dir + '/' + HN + '/' + GS + '/' + TM + '/WSPD_SLP/'
        Real_Hurricane_Data = Real_data_dir+'/Real_Data_'+HN+'.csv'

        list_of_max_wind_radius =[]
    
        for CL in CLS:

                #by hurricane setting you define the name of the csv file e.g. /Irma_32km_NoTurb_YSU_hpbl_250.csv/
                Hurricane_Setting = HN + '_' + GS + '_' + TM + '_' + PBL +'_hpbl_'+CL +'.csv'		




                # print(Hurricane_Setting)
                csv_file = (Input_Dir_1+Hurricane_Setting)
                print('csv is ' ,csv_file)
                # you define empty lists which will contain the extracted data from the csv file, and plot them immediatle
                min_slps = []


                min_slps=Extract_the_shit2(csv_file, min_slps,'SLPS')
                print(min_slps)


                list_of_max_wind_radius.append(np.min(min_slps))
                # print(np.max(WSPD))
        all_hurs_max_wind_rads.append(list_of_max_wind_radius)
    all_hurs_max_wind_rads=np.array(all_hurs_max_wind_rads)
    percentile_20=[]
    percentile_80=[]
    for i in range(len(CLS)):
        # print('mean is: ', np.average(all_hurs_max_wind_rads[:,i]),' and 80th perc is: ',np.percentile(all_hurs_max_wind_rads[:,i],80))
        percentile_80.append([np.percentile(all_hurs_max_wind_rads[:,i],80)-np.average(all_hurs_max_wind_rads[:,i])])
        percentile_20.append([np.average(all_hurs_max_wind_rads[:,i])-np.percentile(all_hurs_max_wind_rads[:,i],20)])
        percentile.append([percentile_20[i],percentile_80[i]])
        
        # percentile_20.append([[all_hurs_max_wind_rads[:,i]-np.percentile(all_hurs_max_wind_rads[:,i],20)],[np.percentile(all_hurs_max_wind_rads[:,i],80)-all_hurs_max_wind_rads[:,i]]])

        final_out_list.append(np.average(all_hurs_max_wind_rads[:,i]))
    # print(percentile)
    print(final_out_list)
    print(percentile)

    return(final_out_list,percentile)
# min_SLP_xkzm('YSU')
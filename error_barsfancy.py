

from tokenize import Ignore
from all_functions import Extract_by_name,Extract_Track_Data,list_csv_files_0, calculate_distance_error,calculate_intensity_error,calculate_intensity_error_slp
import matplotlib.gridspec as gridspec
import os
import numpy as np
import matplotlib.pyplot as plt


Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'
os.chdir(Real_data_dir)
Input_Dir = '/Users/lmatak/Desktop/leo_simulations/WRF_Output_PBLHS/diff_hpbls'
# Choose between : 'Igor,'Dorian','Teddy','Lorenzo','Maria','Iota']
HNS = ['Lorenzo','Iota','Igor','Dorian','Teddy','Maria']
# Choose between : '2km', '4km', '8km', '16km', '32km'
GSS = ['8km']
# Choose between : 'NoTurb', 'Smag2D', 'TKE2D'
TM = 'NoTurb'
# Choose between : 'YSU_wrf_42',YSU_lin_63'
PBLS = ['YSU']

# CLS = ['lvl_3','lvl_5','1.0','lvl_7'] 
CLS = ['xkzm_0.125','xkzm_0.20','xkzm_0.25_lvl_2','1.0','xkzm_4.0_lvl_2','xkzm_5.0','xkzm_8.0']
# CLS_MYJ =['1.0','KH_0.25','KH_2.0','KH_4.0','KH_6.0','KH_8.0']
# CLS = ['km_0.125','km_0.20','km_0.25_lvl_2','1.0','km_4.0_lvl_2','km_5.0','km_8.0']
# colors = ['blue', 'orange', 'red', 'green', 'purple', 'magenta','yellow']
colors = ['darkblue', 'lightblue','darkgreen', 'lightgreen', 'magenta','yellow','blue']
colors_per_CLS=['blue','green','black','red','cyan','magenta','grey']
fig = plt.figure(figsize=(16, 8), tight_layout=True)
gs = gridspec.GridSpec(1,3,figure=fig,wspace=0.2,top=0.8)

# number_of_points=

List_Of_Hurricanes=[]
Average_List_Of_Hurricanes=[]

x_indexes=np.arange(len(CLS))
BarWidth=0

Time_Idx = 0
ax1 = fig.add_subplot(gs[0,0])
ax2 =fig.add_subplot(gs[0,1])
ax3 =fig.add_subplot(gs[0,2])
color_counter=0
axxess=(ax1,ax2,ax3)
for PBL in PBLS:
    for GS in GSS:
        all_hurs_track_error_list=[]
        all_hurs_wind_intensity_error_list=[]
        all_hurs_min_slp_error_list=[]
        List_for_CSV_files=[]
        for CL in CLS:
            List_for_CSV_files.append(PBL+'_hpbl_'+CL)
        print(List_for_CSV_files)

        for HN in HNS:
            print(HN)

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
            print("I'm out!")

            # if HN =='Maria':
            #     Real_Lats=Real_Lats[:number_of_points]
            #     Real_Longs=Real_Longs[:number_of_points]
            #     Real_slp=Real_slp[:number_of_points]
            #     Real_Winds=Real_Winds[:number_of_points]
            



            
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

                # if HN =='Maria' :
                #     Eye_Lats=Eye_Lats[:number_of_points]
                #     Eye_Longs=Eye_Longs[:number_of_points]
                #     simulated_wind_intensities=simulated_wind_intensities[:number_of_points]
                #     simulated_min_slp=simulated_min_slp[:number_of_points]

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




        ##### HERE SET THE LABEL FOR WHAT YOU WANT IN ELGEND BEFORE RUNS #### AND ALSO WIDTH!!!!
        for i in range(len(avg_wind)):
            print(avg_wind[i])
            ax1.bar(i+BarWidth,avg_track[i],width=0.1, edgecolor='black', color=colors_per_CLS[color_counter],label=CLS[color_counter])
            ax2.bar(i+BarWidth,avg_wind[i],width=0.1, edgecolor='black',color=colors_per_CLS[color_counter],label=CLS[color_counter])
            ax3.bar(i+BarWidth,avg_slp[i],width=0.1,edgecolor='black',color=colors_per_CLS[color_counter],label=CLS[color_counter])
            color_counter+=1
        BarWidth+=0.1
        
x_ticks=[]
for i in range(len(CLS)):
    x_ticks.append(len(GSS)/10-0.1+i)

##### HERE SET THE XTICKS

ax1.set_xticks(x_ticks)
ax1.set_title('Track error')
ax1.set_ylabel('[km]')

ax2.set_xticks(x_ticks)
ax2.set_title('Wind intensity error')
ax2.set_ylabel('%')

ax3.set_xticks(x_ticks)
ax3.set_title('Min slp error')
ax3.set_ylabel('[mb]')


ax1.set_xticklabels(CLS)
ax2.set_xticklabels(CLS)
ax3.set_xticklabels(CLS)
# ax1.set_xlabel('hpbl [m]', fontsize=12)
# ax2.set_xlabel('hpbl [m]', fontsize=12)
# ax3.set_xlabel('hpbl [m]', fontsize=12)
fig.suptitle(', '.join(HNS)+' -- '+', '.join(PBLS)+' --  '+', '.join(GSS), fontsize=16)


handles, labels = fig.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
# print(by_label)


fig.legend(by_label.values(), by_label.keys(), loc = 'upper center',ncol = 5, bbox_to_anchor=(0.65, 0.92, -0.3, 0),frameon = True)



# #ax[0].legend()
# #ax[0].set_title('The average error of all hurricane versus the grid size for each turbulent model')
ax1.yaxis.grid(True)
ax2.yaxis.grid(True)
ax3.yaxis.grid(True)
plt.show()




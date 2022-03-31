from numpy.core.function_base import linspace
from all_functions import Extract_by_name,Extract_Coordinates_2,Extract_Track_Data, Extract_the_shit2
import cartopy.feature as cfeature
import matplotlib.gridspec as gridspec
#from Func_Map_Setting import map_setting
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter,LatitudeLocator
import numpy as np





Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'

Input_Dir = '/Users/lmatak/Desktop/leo_simulations/WRF_Output_PBLHS/diff_hpbls'

# for MYJ 'Maria','Dorian','Iota','Teddy','Lorenzo , Igor
HNS = ['Dorian','Iota','Maria','Lorenzo','Igor']
# Choose between : '2km', '4km', '8km', '16km', '32km'
GS = '8km'
# Choose between : 'NoTurb', 'Smag2D', 'TKE2D'
TM = 'NoTurb'
# Choose between : 'YSU_wrf_42',YSU_lin_63'
PBLS = ['MYJ']


Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'

Time_idx = '0'

fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(10.8,5.8))
# fig.tight_layout()
fig.subplots_adjust(hspace=0.3)

# show = 'xkzm'
show = 'lvls'

CLS = ['1.0','lvl_3','lvl_5','lvl_7']
fig_name='_lvls_'
colors = ['black','blue', 'green', 'red']
legend_names=['Default Case','HBL - lvl_3_'+PBLS[0],'HBL - lvl_5_'+PBLS[0],'HBL - lvl_7_'+PBLS[0]]
if show == 'xkzm':
    fig_name='_xkzm_'
    colors = ['black','blue',  'red']
    CLS=['1.0_xkzm','km_0.2','km_5.0']
    legend_names=['Default Case','cl_km_0.2_'+PBLS[0],'cl_km_5.0_'+PBLS[0]]
    if PBLS[0]=='YSU':
        CLS = ['1.0_xkzm','xkzm_0.2','xkzm_5.0'] 
Times = [0,6, 12, 18, 24, 30, 36, 42, 48,54,60,66,72,80]
Real_Winds=[]
row_count=0
col_count=0

for HN in HNS :

    Input_Dir_1 = Input_Dir + '/' + HN + '/' + GS + '/' + TM + '/WSPD_R/'
    Real_Hurricane_Data = Real_data_dir+'/Real_Data_'+HN+'.csv'


    for PBL in PBLS:
        cls_counter=0
        for CL in CLS:

                #by hurricane setting you define the name of the csv file e.g. /Irma_32km_NoTurb_YSU_hpbl_250.csv/
                Hurricane_Setting = HN + '_' + GS + '_' + TM + '_' + PBL +'_hpbl_'+CL +'.csv'		




                # print(Hurricane_Setting)
                csv_file = (Input_Dir_1+Hurricane_Setting)
                # print('csv file is ::::: ',csv_file)
                # you define empty lists which will contain the extracted data from the csv file, and plot them immediatle
                WSPD = []
                rads=[]
                rads=Extract_the_shit2(csv_file, rads,'Radiuses')
                WSPD=Extract_the_shit2(csv_file, WSPD,' Average_WSPD')

                ax[row_count,col_count].plot(rads[0:80], WSPD[0:80], color=colors[cls_counter],  linestyle='-',
                marker='x', markersize='0',  
                    linewidth='2', label= CL)

                print('for '+HN+' - '+CL+' max wspd is: ',np.amax(WSPD))
                
                
                cls_counter+=1
        # xticks=linspace(0,rads[-1],15)
        # print(xticks)
        ax[row_count,col_count].set_title(HN,size=13)
        ax[row_count,col_count].tick_params(axis='both', labelsize=12)
        # ax[row_count,col_count].set_xticklabels(xticks)
        # ax[row_count,col_count].set_yticks(wind_intensities[0:number_of_lvls])
    col_count+=1
    if col_count == 3:
        col_count =0
        row_count = 1
ax[0,0].set_ylabel('Average WSPD [m/s]', size=12)
ax[1,0].set_ylabel('Average WSPD [m/s]',size=12)
ax[1,0].set_xlabel('Radius',size=12)
ax[1,1].set_xlabel('Radius',size=12)
ax[1,2].set_xlabel('Radius',size=12)
h, l = ax[1,1].get_legend_handles_labels()
plt.rc('legend',fontsize=14)
ax[1,2].axis("off")
ax[1,2].legend(h, legend_names,ncol=1,frameon=False)
# plt.show()

print('saved as: fig9_wspd_r_boxes'+fig_name+PBLS[0]+'.eps')
plt.savefig('/Users/lmatak/Desktop/leo_python_scripts/Paper_Figs/figs_saved/fig9_wspd_r_boxes'+fig_name+PBLS[0]+'.eps',bbox_inches='tight')
# print('saved as: figure8_WSPD_R'+name_text+PBLS[0]+'.eps')
# plt.savefig('/Users/lmatak/Desktop/leo_python_scripts/Paper_Figs/figs_saved/figure8_WSPD_R'+name_text+PBLS[0]+'.eps',bbox_inches='tight')
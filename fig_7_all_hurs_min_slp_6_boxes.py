from numpy.core.function_base import linspace
from all_functions import Extract_by_name,Extract_Coordinates_2,Extract_Track_Data, Extract_the_shit2
import cartopy.feature as cfeature
import matplotlib.gridspec as gridspec
#from Func_Map_Setting import map_setting
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter,LatitudeLocator





Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'

Input_Dir = '/Users/lmatak/Desktop/leo_simulations/WRF_Output_PBLHS/diff_hpbls'

# for MYJ 'Maria','Dorian','Iota','Teddy','Lorenzo , Igor
HNS = ['Iota','Maria','Dorian','Teddy','Lorenzo','Igor']
# Choose between : '2km', '4km', '8km', '16km', '32km'
GS = '8km'
# Choose between : 'NoTurb', 'Smag2D', 'TKE2D'
TM = 'NoTurb'
# Choose between : 'YSU_wrf_42',YSU_lin_63'
PBLS = ['YSU']
# PBLS = ['YSU_additional_changs']

CLS = ['1.0','lvl_3','lvl_5','lvl_7'] 
# CLS=['1.0','xkzm_0.25_lvl_2','xkzm_4.0_lvl_2']
# CLS = ['1.0','km_0.25_lvl_2','km_4.0_lvl_2']
Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'

Time_idx = '0'

fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(10.8,5.8))
fig.subplots_adjust(hspace=0.25)
# fig.tight_layout()
if CLS[1] == 'lvl_3':
    name_text='_lvls_'
    colors = ['grey','blue',  'green', 'red', 'purple', 'magenta','yellow']
else:
    name_text='_xkzm_'
    colors = ['grey','blue',  'red', 'green', 'purple', 'magenta','yellow']
Times = [0,6, 12, 18, 24, 30, 36, 42, 48,54,60,66,72,80]
Real_Winds=[]
row_count=0
col_count=0

for HN in HNS :

    Input_Dir_1 = Input_Dir + '/' + HN + '/' + GS + '/' + TM + '/Standard/'
    Real_Hurricane_Data = Real_data_dir+'/Real_Data_'+HN+'.csv'

    Real_SLP = []

    Real_SLP = Extract_by_name(Real_Hurricane_Data,Real_SLP,'Pressure (mb) ')
    print(Real_SLP)
    ax[row_count,col_count].plot(Times[0:len(Real_SLP)], Real_SLP, color='k', linestyle='-',
                marker='.', linewidth='2', markersize='9', label='Real min SLP')
    for PBL in PBLS:
        cls_counter=0
        for CL in CLS:

                #by hurricane setting you define the name of the csv file e.g. /Irma_32km_NoTurb_YSU_hpbl_250.csv/
                Hurricane_Setting = HN + '_' + GS + '_' + TM + '_' + PBL +'_hpbl_'+CL +'.csv'		




                # print(Hurricane_Setting)
                csv_file = (Input_Dir_1+Hurricane_Setting)

                #you define empty lists which will contain the extracted data from the csv file, and plot them immediatle
                min_slps = []

           

                min_slps=Extract_by_name(csv_file, min_slps,'min_slp')
                # print(min_slps)

                ax[row_count,col_count].plot(Times[0:len(min_slps)], min_slps, color=colors[cls_counter], linestyle='--',
                marker='.', markersize='9',  
                    linewidth='2', label= (CLS[cls_counter]))
                
                cls_counter+=1
        ax[row_count,col_count].set_title(HN)
        ax[row_count,col_count].set_xticks(Times[0:len(min_slps)])
        # ax[row_count,col_count].set_yticks(wind_intensities[0:number_of_lvls])
    col_count+=1
    if col_count == 3:
        col_count =0
        row_count = 1
ax[0,0].set_ylabel('min SLP [mb]')
ax[1,0].set_ylabel('min SLP [mb]')
ax[1,0].set_xlabel('Time')
ax[1,1].set_xlabel('Time')
ax[1,2].set_xlabel('Time')
handles, labels = fig.gca().get_legend_handles_labels()

by_label = dict(zip(labels, handles))
plt.rc('legend',fontsize=12)
if CLS[1]!='lvl_3':
    legend_names=['Real Data','Default Case','cl_km_0.25_'+PBLS[0],'cl_km_4.0_'+PBLS[0]]
    
else:
    legend_names=['Real Data','Default Case','HBL - lvl_3_'+PBLS[0],'HBL - lvl_5_'+PBLS[0],'HBL - lvl_7_'+PBLS[0]]
lgnd = fig.legend(by_label.values(),legend_names ,loc = 'upper center',ncol = 5,frameon = False)

plt.show()
# plt.savefig('/Users/lmatak/Desktop/leo_python_scripts/Paper_Figs/figure7_min_slp_lvls_'+PBLS[0]+'.eps',bbox_inches='tight')
# plt.show()
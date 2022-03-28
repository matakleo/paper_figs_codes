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
HNS = ['Dorian','Iota','Maria','Teddy','Lorenzo','Igor']
# Choose between : '2km', '4km', '8km', '16km', '32km'
GS = '8km'
# Choose between : 'NoTurb', 'Smag2D', 'TKE2D'
TM = 'NoTurb'
# Choose between : 'YSU_wrf_42',YSU_lin_63'
PBLS = ['YSU']

# CLS = ['km_0.25_lvl_2','1.0','km_4.0_lvl_2']
CLS = ['lvl_3','lvl_5','1.0','lvl_7'] 
# CLS = ['xkzm_0.125','1.0_xkzm','xkzm_8.0']

Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'

Time_idx = '0'

fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(10.8,5.8))
# fig.tight_layout()
fig.subplots_adjust(hspace=0.3)

if CLS[0] == 'lvl_3':
    name_text='_lvls_'
    colors = [ 'blue', 'green','black', 'red', 'purple', 'magenta','yellow']
    CLS_names=['HBL - lvl_3_'+PBLS[0],'HBL - lvl_5_'+PBLS[0],'Default Case '+PBLS[0],'HBL - lvl_7_'+PBLS[0]]
else:
    name_text='_xkzm_'
    colors = ['blue','black',  'red', 'green', 'purple', 'magenta','yellow']
    CLS_names=['cl_km_0.125_'+PBLS[0],'Default Case '+PBLS[0],'cl_km_8.0_'+PBLS[0]]
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
                print('csv file is ::::: ',csv_file)
                # you define empty lists which will contain the extracted data from the csv file, and plot them immediatle
                WSPD = []
                rads=[]
                rads=Extract_the_shit2(csv_file, rads,'Radiuses')
                WSPD=Extract_the_shit2(csv_file, WSPD,' Average_WSPD')

                ax[row_count,col_count].plot(rads[0:80], WSPD[0:80], color=colors[cls_counter],  linestyle='-',
                marker='x', markersize='0',  
                    linewidth='2', label= CL)
                
                
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
handles, labels = fig.gca().get_legend_handles_labels()

by_label = dict(zip(labels, handles))
plt.rc('legend',fontsize=12)

lgnd = fig.legend(by_label.values(),CLS_names ,loc = 'upper center',ncol = 5,frameon = False)

plt.show()
# plt.savefig('/Users/lmatak/Desktop/leo_python_scripts/Paper_Figs/figs_saved/figure8_WSPD_R'+name_text+PBLS[0]+'.eps',bbox_inches='tight')
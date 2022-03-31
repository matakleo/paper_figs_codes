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
HNS = ['Iota','Maria','Dorian','Lorenzo','Igor']
# Choose between : '2km', '4km', '8km', '16km', '32km'
GS = '8km'
# Choose between : 'NoTurb', 'Smag2D', 'TKE2D'
TM = 'NoTurb'
# Choose between : 'YSU_wrf_42',YSU_lin_63'
PBLS = ['MYJ']

plt.rc('font', family='serif')
plt.rc('font', size=10)

Time_idx = '0'

fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(10.8,5.8))
fig.subplots_adjust(hspace=0.25,wspace=0.2)

show = 'xkzm'
# show = 'lvls'

CLS = ['1.0','lvl_3','lvl_5','lvl_7']
fig_name='_lvls_'
colors = ['black','blue', 'green', 'red']
legend_names=['Default Case','HBL - lvl_3_'+PBLS[0],'HBL - lvl_5_'+PBLS[0],'HBL - lvl_7_'+PBLS[0]]
if show == 'xkzm':
    fig_name='_xkzm_'
    colors = ['black','blue',  'red']
    CLS=['1.0','km_0.20','km_5.0']
    legend_names=['Default Case','cl_km_0.2_'+PBLS[0],'cl_km_5.0_'+PBLS[0]]
    if PBLS[0]=='YSU':
        CLS = ['1.0','xkzm_0.20','xkzm_5.0'] 
row_count=0
col_count=0

for HN in HNS :

    Input_Dir_1 = Input_Dir + '/' + HN + '/' + GS + '/' + TM + '/Standard/'
    
    for PBL in PBLS:
        cls_counter=0
        for CL in CLS:

                #by hurricane setting you define the name of the csv file e.g. /Irma_32km_NoTurb_YSU_hpbl_250.csv/
                Hurricane_Setting = HN + '_' + GS + '_' + TM + '_' + PBL +'_hpbl_'+CL +'.csv'		
                # print(Hurricane_Setting)
                csv_file = (Input_Dir_1+Hurricane_Setting)

                #you define empty lists which will contain the extracted data from the csv file, and plot them immediatle
                momentum_exchange = []

           
                lvl_heights=[]
                lvl_heights = Extract_by_name(csv_file, lvl_heights, 'lvl_heights')
                momentum_exchange=Extract_by_name(csv_file, momentum_exchange,'avg_vert_exch_momentum')

                number_of_lvls=9
                ax[row_count,col_count].plot(momentum_exchange[0:number_of_lvls], lvl_heights[0:number_of_lvls], color=colors[cls_counter],  marker='.', 
                    linewidth='2',markersize='9', label= (CLS[cls_counter]))
                
                cls_counter+=1
        ax[row_count,col_count].set_title(HN,fontsize=12)
        # ax[row_count,col_count].yaxis.grid(True)
        ax[row_count,col_count].set_yticks(lvl_heights[0:number_of_lvls])
    col_count+=1
    if col_count == 3:
        col_count =0
        row_count = 1
ax[0,0].set_ylabel('Height [m]',fontsize=12)
ax[1,0].set_ylabel('Height [m]',fontsize=12)
ax[1,0].set_xlabel('Km',fontsize=12)
ax[1,1].set_xlabel('Km',fontsize=12)
ax[1,2].set_xlabel('Km',fontsize=12)
h, l = ax[1,1].get_legend_handles_labels()
plt.rc('legend',fontsize=14)
ax[1,2].axis("off")
ax[1,2].legend(h, legend_names,ncol=1,frameon=False)
# plt.show()

print('saved as: fig4_momentum_boxes'+fig_name+PBLS[0]+'.eps')
plt.savefig('/Users/lmatak/Desktop/leo_python_scripts/Paper_Figs/figs_saved/fig4_momentum_boxes'+fig_name+PBLS[0]+'.eps',bbox_inches='tight')
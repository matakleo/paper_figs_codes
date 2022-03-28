from numpy.core.function_base import linspace
from all_functions import Extract_by_name,Extract_Coordinates_2,Extract_Track_Data
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
HNS = ['Iota','Teddy','Dorian','Maria','Igor','Lorenzo']
# Choose between : '2km', '4km', '8km', '16km', '32km'
GS = '8km'
# Choose between : 'NoTurb', 'Smag2D', 'TKE2D'
TM = 'NoTurb'

PBLS = ['YSU']

show = 'xkzm'
# show = 'lvls'

CLS = ['lvl_3','lvl_5','1.0','lvl_7']
colors = ['grey', 'blue','green', 'red']
legend_names=['Real Track','Default Case','HBL - lvl_3_'+PBLS[0],'HBL - lvl_5_'+PBLS[0],'HBL - lvl_7_'+PBLS[0]]
if show == 'xkzm':
    colors = ['grey', 'blue', 'red']
    CLS=['km_0.25_lvl_2','1.0','km_4.0_lvl_2']
    legend_names=['Real Track','Default Case','cl_km_0.25_'+PBLS[0],'cl_km_4.0_'+PBLS[0]]
    if PBLS[0]=='YSU':
        CLS = ['xkzm_0.25_lvl_2','1.0','xkzm_4.0_lvl_2'] 

        


print(CLS)

Time_idx = '0'

fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(10.8,5.8),subplot_kw={'projection': ccrs.PlateCarree()})
fig.subplots_adjust(hspace=0.005,wspace=0.25)


row_count=0
col_count=0

for HN in HNS :

    Input_Dir_1 = Input_Dir + '/' + HN + '/' + GS + '/' + TM + '/Standard/'

    Real_Lats = []
    Real_Longs = []
    Real_Lats = Extract_Track_Data (Real_data_dir, Real_Lats, 'Lat',HN)
    Real_Longs = Extract_Track_Data (Real_data_dir, Real_Longs, 'Lon',HN)


    lat_cor_first = Real_Lats[0]
    lat_cor_last = Real_Lats[-1]
    lon_cor_first = Real_Longs[0]
    lon_cor_last = Real_Longs[-1]

    ax[row_count,col_count].stock_img()
    ax[row_count,col_count].set_extent([lon_cor_last-1.5,lon_cor_first+1.5, lat_cor_first-1.5 , lat_cor_last+1.5])

    gl = ax[row_count,col_count].gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                linewidth=5, color='gray', alpha=0, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    # ax[row_count,col_count].xlabel_style = {'size': 0.2}
    # ax[row_count,col_count].xlabel_style = {'color': 'black'}
    ax[row_count,col_count].add_feature(cfeature.COASTLINE)
    ax[row_count,col_count].coastlines('50m', linewidth=0.8)

    ax[row_count,col_count].plot(Real_Longs, Real_Lats, color='k', linestyle='--',
                marker='*', linewidth='2', markersize='9',transform=ccrs.PlateCarree(), label='Real Track')
    ax[row_count,col_count].set_title(HN)


    
    for PBL in PBLS:
        cls_counter=0
        for CL in CLS:

                #by hurricane setting you define the name of the csv file e.g. /Irma_32km_NoTurb_YSU_hpbl_250.csv/
                Hurricane_Setting = HN + '_' + GS + '_' + TM + '_' + PBL +'_hpbl_'+CL +'.csv'		
                # print(Hurricane_Setting)
                csv_file = (Input_Dir_1+Hurricane_Setting)

                #you define empty lists which will contain the extracted data from the csv file, and plot them immediatle
                Eye_Lats = []
                Eye_Longs = []

                (Eye_Lats, Eye_Longs) = Extract_Coordinates_2 (Input_Dir_1, Hurricane_Setting,'min_lat', 'min_long')


                ax[row_count,col_count].plot(Eye_Longs[0:len(Eye_Lats)], Eye_Lats[0:len(Eye_Lats)], color=colors[cls_counter],  marker='.', 
                    linewidth='1.7',markersize='8', transform=ccrs.PlateCarree(), label= (CLS[cls_counter]+PBL))
                ax[row_count,col_count].tick_params(axis='x', labelsize=16, length=10, direction = 'in', width = 2)
                ax[row_count,col_count].tick_params(axis='y', labelsize=16, length=10, direction = 'in', width = 2)
                
                cls_counter+=1
    col_count+=1
    if col_count == 3:
        col_count =0
        row_count = 1

handles, labels = fig.gca().get_legend_handles_labels()

by_label = dict(zip(labels, handles))
plt.rc('legend',fontsize=12)
lgnd = fig.legend(by_label.values(),legend_names,loc = 'upper center',ncol = 5,frameon = False)

# plt.show()
plt.savefig('/Users/lmatak/Desktop/leo_python_scripts/Paper_Figs/fig3_tracks_cl_km_YSU.png',bbox_inches='tight')
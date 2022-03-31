from turtle import right
from typing import Counter
from wrf import (getvar, interplevel, smooth2d, to_np, latlon_coords, get_cartopy, cartopy_xlim, cartopy_ylim)
from all_functions import Extract_Track_Data,list_ncfiles
from cartopy.mpl.gridliner import LongitudeFormatter, LATITUDE_FORMATTER
from cartopy.feature import NaturalEarthFeature
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage
from netCDF4 import Dataset
import cartopy.crs as crs
import numpy as np
import math
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os


Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'
Input_Dir = '/Users/lmatak/Desktop/some_wrfout_files/'
# Choose between : 'Gustav', 'Irma', 'Katrina', 'Maria'
HNS = ['Maria','Lorenzo','Dorian','Iota','Igor']
# Choose between : '2km', '4km', '8km', '16km', '32km'
GSS = ['8km']
# Choose between : 'NoTurb', 'Smag2D', 'TKE2D'
TMS = ['NoTurb']
# Choose between : 'cLh0p2', 'cLh0p5', 'cLh1p0', 'cLh1p5'
PBLS=['MYJ']



CLS = ['lvl_3','lvl_5','1.0']
# CLS = ['xkzm_0.2','1.0','xkzm_5.0']
name_word='_lvls'

if CLS[0]=='xkzm_0.2':
    name_word='_xkzm'
    Input_Dir='/Users/lmatak/Desktop/some_wrfout_files/new_ones/'


def some_fun(Alt,HN,PBL,CLS,Input_Dir):
    Time_idx=0
    max_wspds=[]
    Input_Dir = Input_Dir
    for CL in CLS[0:-1]:
        
        # for CL in CLS:
        ncfiles = []                    
        Hurricane_Setting = HN + '_8km_NoTurb_' + PBL +'_hpbl_'+CL
        Input_Dir_1 = Input_Dir +  Hurricane_Setting
        os.chdir(Input_Dir_1)

        ncfiles = list_ncfiles(Input_Dir_1, ncfiles)
        Data = Dataset(ncfiles[0])  
        print('is something happening?')
        z = getvar(Data, "z", timeidx = Time_idx)
        wspd = getvar(Data, "wspd", timeidx = Time_idx)
        wspd_500 = interplevel(wspd, z, Alt)
        max_wspds.append(float(np.max(wspd_500)))
        print('max spd',max_wspds)
    return(max_wspds[0])



# Choose between: '0', '1', '2', '3', '4', '5'
Time_idx = 0
row=0
col=0
# Choose the altitude:
Alt = 500
max_wspd=0
nbins=7
cmap_name='my_colors'
#coolwarm is the red-blue one
# cmap=plt.get_cmap(
#     'plasma')
cmap=plt.get_cmap(
    'twilight_shifted')
# Create a figure
fig, ax = plt.subplots(nrows=5, ncols=3, figsize=(8.5,10.7),subplot_kw={'projection': crs.PlateCarree()})
fig.subplots_adjust(wspace=0.000005)
# colors=['lightyellow','indigo','lightgreen','lightblue','blue','yellow','red','black']
# cm = LinearSegmentedColormap.from_list(
#         cmap_name, colors, N=nbins)
for HN in HNS:
    for GS in GSS:
        for TM in TMS:
            i = 0
            for PBL in PBLS:
                for CL in CLS: 


                    ncfiles = []                    
                    Hurricane_Setting = HN + '_' + GS + '_' + TM + '_' + PBL +'_hpbl_'+CL
                    Input_Dir_1 = Input_Dir +  Hurricane_Setting
                    # Set the working space.
                    os.chdir(Input_Dir_1)

                    ncfiles = list_ncfiles(Input_Dir_1, ncfiles)
                    Data = Dataset(ncfiles[0])  
                

                    
                    # Open the NetCDF file
                    

                    #Extract the necessary data to plot the contour map.
                    slp = getvar(Data, "slp", timeidx = Time_idx)
                    z = getvar(Data, "z", timeidx = Time_idx)
                    wspd = getvar(Data, "wspd", timeidx = Time_idx)

                    print('row = ',row)
                    print('col = ',col)
                    ax[row,col].stock_img()
                    ax[row,col].coastlines('50m', linewidth=0.8)
                    
                    gl = ax[row,col].gridlines(crs=crs.PlateCarree(), draw_labels=True,
                        linewidth=0.2, color='black', alpha=0.2, linestyle='--')
                    gl.top_labels = False
                    gl.right_labels = False
                    gl.xlabel_style= {'size': 9, 'color': 'black'}  
                    gl.ylabel_style= {'size': 9, 'color': 'black'}
                    # if (row == 0 and col == 2):
                    #     lon_formatter = LongitudeFormatter(zero_direction_label=True)
                    #     ax[row,col].xaxis.set_major_formatter(lon_formatter)

                    #     gl.left_labels = False
                    #     gl.bottom_labels = False
                    #     ax[row,col].set_xticks([-60.5, -61.3, -62])
                    #     ax[row,col].tick_params(axis='x', labelsize=9, pad=5, length=0, direction = 'in', width = 2)
                    
                    if col != 0:
                        gl.left_labels = False
                    
                    # ax[row,col].tick_params(axis='y', labelsize=8, length=0, direction = 'in', width = 2)
                    

                    # Interpolate geopotential height, u, and v winds to 500 hPa
                    wspd_500 = interplevel(wspd, z, Alt)
                    # print(CL+' max wspd = ',np.max(wspd))

                    # Get the latitude and longitude points
                    lats, lons = latlon_coords(wspd_500)
                    
                    lat_min_slp=np.where(slp == np.amin(slp))[0]
                    lon_min_slp=np.where(slp == np.amin(slp))[1]
                    print(lat_min_slp,lon_min_slp)

                    slp_coord_lat= float(lats[lat_min_slp][0][0])

                    slp_coord_long=float(lons[0][lon_min_slp])
                    # Get the cartopy mapping object
                    cart_proj = get_cartopy(wspd_500)

                    if col==0:
                        
                        w_max=some_fun(Alt,HN,PBL,CLS,Input_Dir)
                        if HN == 'Igor' and CL =='xkzm_0.2' :

                            w_max=w_max+7
                        if PBL == 'MYJ':
                            w_max=w_max+7
                        print('wmax=',w_max)
                        w_min=0
                    
                    im_cbar = ax[row,col].contourf(to_np(lons), to_np(lats), to_np(wspd_500), 255, vmin=w_min, vmax =w_max, 
                        transform=crs.PlateCarree(), 
                        cmap=cmap)
                    # cmap.set_over('red')
                    # cmap.set_under('blue')
                    # if col == 0:
                        
                    #     cbar_ax = fig.add_axes([0.85, 0.75-row/6.3, 0.025, 0.15])
                    if col==2:
                    #     divider = make_axes_locatable(ax)
                    
                    # # creating new axes on the right
                    # # side of current axes(ax).
                    # # The width of cax will be 5% of ax
                    # # and the padding between cax and ax
                    # # will be fixed at 0.05 inch.
                    # colorbar_axes = divider.append_axes("right",
                    #                                     size="10%",
                    #                                     pad=0.1)
                    
                        # ax = plt.gca()
                        # im,fraction=0.046, pad=0.04
                        # divider = make_axes_locatable(ax)
                        # cax = divider.append_axes("right", size="5%", pad=0.05)
                        # bounds = [10,20,30,40,50,60]
                        # if w_max > 60 :
                        #     bounds = [20, 30, 40, 50, 60, 70]
                        # if w_max > 70 :
                        #     bounds = [30, 40, 50, 60, 70, 80]
                        # if w_max > 80 :
                        #     bounds = [40, 50, 60, 70, 80,90]  

                        # norm = mpl.colors.BoundaryNorm( cmap.N, extend='both')
                        norm = mpl.colors.Normalize(vmin=w_min, vmax=w_max)
                        # cbar= fig.colorbar(im_cbar, pad=0.04,ax=ax[row,2],aspect=10)
                        # cbar.ax.tick_params(labelsize=8)
                        fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                        ax=ax[row,2], orientation='vertical', aspect=10, extend='both',
                        label="Wind speed (m/s)")
                        

                    CS = ax[row,col].contour(to_np(lons), to_np(lats), to_np(slp), 6, colors="black", alpha=1,
                        transform=crs.PlateCarree(), linewidths = 1)

                    ax[row,col].set_extent([slp_coord_long+0.8,slp_coord_long-0.8,slp_coord_lat-0.65,slp_coord_lat+0.65])

                    
                        
                    ax[row,col].clabel(CS, CS.levels, inline=True, fontsize=8, inline_spacing=8,  use_clabeltext=True)
                    
                    col+=1
                    if col==3:
                        row+=1
                        col =0





if CLS[0] == 'xkzm_0.2':

    ax[0,0].set_title('cl_km_0.2_'+PBLS[0], size=12)
    ax[0,1].set_title('Default Case '+PBLS[0],size=12)
    ax[0,2].set_title('cl_km_5.0_'+PBLS[0],size=12)
else:   
    ax[0,0].set_title('HBL - lvl_3_'+PBLS[0], size=12)
    ax[0,1].set_title('HBL - lvl_5_'+PBLS[0] ,size=12)
    ax[0,2].set_title('Default Case - '+PBLS[0],size=12)


        

for i in range(len(HNS)):
    if (HNS[i] == 'Dorian' or HNS[i] == 'Lorenzo'):
        ax[i,0].annotate(HNS[i], xy=(-0.35, 0.85), xycoords='axes fraction',
                xytext=(0, 0), textcoords='offset points',
                ha="right", va="top",size=12,
                rotation = 90
                )
    else:
        ax[i,0].annotate(HNS[i], xy=(-0.35, 0.75), xycoords='axes fraction',
                    xytext=(0, 0), textcoords='offset points',
                    ha="right", va="top",size=12,
                    rotation = 90
                    )

                    #x axis


# plt.show()
print('saved fig as: fig5_CONTOURS_'+PBLS[0]+name_word+'.png')
plt.savefig('/Users/lmatak/Desktop/leo_python_scripts/Paper_Figs/figs_saved/fig5_CONTOURS_'+PBLS[0]+name_word+'.png',bbox_inches='tight')


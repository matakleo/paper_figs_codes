
from all_functions import Extract_by_name,Extract_Track_Data,list_csv_files_0, calculate_distance_error,calculate_intensity_error,calculate_intensity_error_slp
import matplotlib.gridspec as gridspec
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from error_function_bars import gimme_errors

fig = plt.figure(figsize=(10.8, 4.3))
gs = gridspec.GridSpec(1,4,figure=fig,wspace=0.5,hspace=0.6)
ax1= fig.add_subplot(gs[:,0:2])
ax2= fig.add_subplot(gs[:,2:4])
plt.rc('font', family='serif')


ysu_intensities,ysu_track,wind_percentile_ysu,track_percentile_ysu = gimme_errors('YSU')
myj_intensities,myj_track,wind_percentile_myj,track_percentile_myj = gimme_errors('MYJ')



BarWidth=0.3
GSS=['2km','8km','32km']
ysu_color=['royalblue']
myj_color=['coral']
colors = ['royalblue', 'grey', 'coral', 'green', 'orange', 'magenta','yellow']

for i in range(len(ysu_intensities)):
    if i ==0:
        ax1.bar(i,ysu_intensities[i],width=0.3,edgecolor='black',color=ysu_color,yerr=wind_percentile_ysu[i],capsize=5,label='YSU')
        ax1.bar(i+BarWidth,myj_intensities[i],width=0.3,edgecolor='black',hatch='..',color=myj_color,yerr=wind_percentile_myj[i],capsize=5,label='MYJ')
    else:
        ax1.bar(i,ysu_intensities[i],width=0.3,edgecolor='black',color=ysu_color,yerr=wind_percentile_ysu[i],capsize=5)
        ax1.bar(i+BarWidth,myj_intensities[i],width=0.3,edgecolor='black',hatch='..',color=myj_color,yerr=wind_percentile_myj[i],capsize=5)

    ax2.bar(i,ysu_track[i],width=0.3,edgecolor='black',color=ysu_color,yerr=track_percentile_ysu[i],capsize=5)
    ax2.bar(i+BarWidth,myj_track[i],width=0.3,edgecolor='black',hatch='..',color=myj_color,yerr=track_percentile_myj[i],capsize=5)
    ax2.set_ylim(0)
ax1.set_ylabel(r'$MAPE_{intensity}$ (%)',fontsize=12)
ax2.set_ylabel(r'$MAE_{track}$ (km)',fontsize=12)

xticks=[0.15,1.15,2.15]
ax1.set_xticks(xticks)
ax2.set_xticks(xticks)
ax1.set_xticklabels(GSS)
ax2.set_xticklabels(GSS)

ax1.yaxis.grid(True)
ax2.yaxis.grid(True)

ax1.tick_params(axis='x', labelsize=12, length=8, direction = 'out', width = 1.5)
ax1.tick_params(axis='y', labelsize=12, length=8, direction = 'out', width = 1.5)
ax2.tick_params(axis='x', labelsize=12, length=8, direction = 'out', width = 1.5)
ax2.tick_params(axis='y', labelsize=12, length=8, direction = 'out', width = 1.5)

circ1 = mpatches.Patch(alpha=0,hatch='xx',label='YSU')
circ2= mpatches.Patch(alpha=0,hatch='..',label='MYJ')
plt.rc('legend',fontsize=12)
lgnd = fig.legend(loc = 'upper center',ncol = 2,frameon = False)



# plt.show()
plt.savefig('/Users/lmatak/Desktop/leo_python_scripts/Paper_Figs/figs_saved/figure2_grid_sensitivity.eps',bbox_inches='tight')

from all_functions import Extract_by_name,Extract_Coordinates_2,Extract_Track_Data
import cartopy.feature as cfeature
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mticker
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter,LatitudeLocator

import matplotlib.pyplot as plt
import cartopy.crs as ccrs

plt.rc('font', family='serif')

Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'
Real_data_dir_long='/Users/lmatak/Desktop/leo_simulations/Real_Data_long'

fig = plt.figure(figsize=(12.3, 7.3))
ax1= fig.add_subplot(1,1,1,projection=ccrs.PlateCarree())
ax1.stock_img()
ax1.set_extent([-15,-90, 0 , 35])

colors = ['blue', 'black', 'red', 'green', 'orange', 'magenta','yellow']

Hurricanes = ['Dorian','Igor','Iota','Lorenzo','Maria']



states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='10m',
        facecolor='none')

i=0
for HN in Hurricanes:
    Real_Lats = []
    Real_Longs = []
    Real_Lats = Extract_Track_Data (Real_data_dir_long, Real_Lats, 'Lat',HN)
    print(HN+str(Real_Lats))
    Real_Longs = Extract_Track_Data (Real_data_dir_long, Real_Longs, 'Lon',HN)
    ax1.plot(Real_Longs,Real_Lats,transform=ccrs.PlateCarree(),label=(HN+"'s observed track"), marker='o', 
			markersize='3',
			linewidth='1.5',linestyle='dotted', color=colors[i])
    i+=1
i=0
for HN in Hurricanes:
    Real_Lats = []
    Real_Longs = []
    Real_Lats = Extract_Track_Data (Real_data_dir, Real_Lats, 'Lat',HN)
    print(HN+str(Real_Lats))
    Real_Longs = Extract_Track_Data (Real_data_dir, Real_Longs, 'Lon',HN)
    ax1.plot(Real_Longs,Real_Lats,transform=ccrs.PlateCarree(),label=(HN+"'s simulated track"), color=colors[i],
			linewidth='3')
    i+=1



ax1.add_feature(cfeature.LAND)
ax1.add_feature(cfeature.COASTLINE)
ax1.add_feature(cfeature.OCEAN)
ax1.add_feature(cfeature.BORDERS)
ax1.add_feature(states_provinces, edgecolor='black')

ax1.set_xticks([-30, -40, -50, -60, -70, -80,], crs=ccrs.PlateCarree())
ax1.set_yticks([10, 15, 20, 25, 30,], crs=ccrs.PlateCarree())

lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
ax1.xaxis.set_major_formatter(lon_formatter)
ax1.yaxis.set_major_formatter(lat_formatter)
ax1.tick_params(axis='x', labelsize=16, length=10, direction = 'in', width = 2)
ax1.tick_params(axis='y', labelsize=16, length=10, direction = 'in', width = 2)


plt.rc('legend',fontsize=11)
plt.legend(loc='upper right')
# plt.savefig('figure1.png',bbox_inches='tight')
# plt.show()
plt.savefig('/Users/lmatak/Desktop/leo_python_scripts/Paper_Figs/figs_saved/figure1.png',bbox_inches='tight')
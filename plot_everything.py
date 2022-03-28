from numpy.core.function_base import linspace
from all_functions import Extract_by_name,Extract_Coordinates_2,Extract_Track_Data
import cartopy.feature as cfeature
import matplotlib.gridspec as gridspec
#from Func_Map_Setting import map_setting
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs






Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'

Input_Dir = '/Users/lmatak/Desktop/leo_simulations/WRF_Output_PBLHS/diff_hpbls'
# Choose between : 'Dorian','Iota','Irma','Laura','Lorenzo','Maria','Matthew','Michael'
# for MYJ 'Maria','Dorian','Iota','Teddy','Lorenzo , Igor
HN = 'Maria'
# Choose between : '2km', '4km', '8km', '16km', '32km'
GS = '8km'
# Choose between : 'NoTurb', 'Smag2D', 'TKE2D'
TM = 'NoTurb'
# Choose between : 'YSU_wrf_42',YSU_lin_63'
PBLS = ['YSU']
# CLS = ['xkzm_0.125','1.0','xkzm_8.0']
CLS=['xkzm_0.125','xkzm_0.25_lvl_2','1.0','xkzm_4.0_lvl_2','xkzm_8.0']
# CLS = ['km_0.125','km_0.25_lvl_2','1.0','km_4.0_lvl_2','km_8.0']

# number_of_points=0

Time_idx = '0'

fig = plt.figure(figsize=(18, 9))
# fig.tight_layout()


gs = gridspec.GridSpec(4,6,figure=fig,wspace=0.3,hspace=0.6)
#normaln ones
ax1 = fig.add_subplot(gs[:2,:2],projection=ccrs.PlateCarree())
ax2 =fig.add_subplot(gs[:2,2:4])
ax3 =fig.add_subplot(gs[:2,-2:])
ax11=fig.add_subplot(gs[-2:,-4:-2])
ax12 =fig.add_subplot(gs[-2:,-2:])
ax13=fig.add_subplot(gs[-2:,:2])







colors = ['grey', 'blue', 'green', 'red', 'magenta','yellow']
line_stylez= ['-','--','-.']
c=0

Input_Dir_1 = Input_Dir + '/' + HN + '/' + GS + '/' + TM + '/Standard/'
# os.chdir(Input_Dir_1)
print('Input dir: ',Input_Dir_1)

Times = [0,6, 12, 18, 24, 30, 36, 42, 48,54,60,66,72,80]
csv_files=[]
dummy_list=[]
# # # #REAL DATA FOR HURRICANE TRACK#
Real_Lats = []
Real_Longs = []
Real_Lats = Extract_Track_Data (Real_data_dir, Real_Lats, 'Lat',HN)
Real_Longs = Extract_Track_Data (Real_data_dir, Real_Longs, 'Lon',HN)



# # # #for setting the extent of the track img
lat_cor_first = Real_Lats[0]
lat_cor_last = Real_Lats[-1]
lon_cor_first = Real_Longs[0]
lon_cor_last = Real_Longs[-1]
ax1.stock_img()
ax1.set_extent([lon_cor_last-3,lon_cor_first+3, lat_cor_first-3 , lat_cor_last+3])
# if HN =='Michael'
gl = ax1.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
			linewidth=5, color='gray', alpha=0, linestyle='--')
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': 0.2}
gl.xlabel_style = {'color': 'black'}
ax1.add_feature(cfeature.COASTLINE)
ax1.coastlines('50m', linewidth=0.8)


os.chdir(Real_data_dir)
Real_Hurricane_Data = Real_data_dir+'/Real_Data_'+HN+'.csv'

#real data for slps
Real_slp=[]
Real_slp = Extract_by_name(Real_Hurricane_Data,Real_slp,'Pressure (mb) ')




Real_Winds=[]

Real_Winds = Extract_by_name(Real_Hurricane_Data,Real_Winds,'Wind Speed(kt)')
# if HN=='Maria':
# 	Real_Winds=Real_Winds[:len(Real_Winds)-number_of_points]
# 	Real_Longs=Real_Longs[:len(Real_Winds)-number_of_points]
# 	Real_Lats=Real_Lats[:len(Real_Winds)-number_of_points]
# 	Real_slp=Real_slp[:len(Real_Winds)-number_of_points]


#TRACK
ax1.plot(Real_Longs, Real_Lats, color='k', linestyle='-',
			marker='.', linewidth='1', markersize='7',transform=ccrs.PlateCarree(), label='Real Track')
#SLP
ax2.plot(Times[0:len(Real_slp)], Real_slp, color = 'black' , linestyle='-',
	 linewidth='2', marker='.', markersize='10',label=('real data'))

#WIND INTENSITIES
ax12.plot(Times[0:len(Real_slp)], Real_Winds[0:len(Real_slp)], color = 'black' , linestyle='-',
	 linewidth='2', marker='.', markersize='10',label=('real data'))



PBL_counter=0
for PBL in PBLS:
	cls_counter=0
	for CL in CLS:

		#by hurricane setting you define the name of the csv file e.g. /Irma_32km_NoTurb_YSU_hpbl_250.csv/
		Hurricane_Setting = HN + '_' + GS + '_' + TM + '_' + PBL +'_hpbl_'+CL +'.csv'		
		# print(Hurricane_Setting)
		csv_file = (Input_Dir_1+Hurricane_Setting)
		lvl_heights=[]
		lvl_heights = Extract_by_name(csv_file, lvl_heights, 'lvl_heights')

		#you define empty lists which will contain the extracted data from the csv file, and plot them immediatle
		Eye_Lats = []
		Eye_Longs = []

		(Eye_Lats, Eye_Longs) = Extract_Coordinates_2 (Input_Dir_1, Hurricane_Setting,'min_lat', 'min_long')
		Times = [0,6, 12, 18, 24, 30, 36, 42, 48,54,60,66,72,80]
		# Times=linspace(0,Times[len(Real_slp)-1],num=len(Eye_Lats))


		


		min_slp_simulation=[]
		min_slp_simulation = Extract_by_name (csv_file, min_slp_simulation, 'min_slp')
		# min_slp_simulation=flatten_the_curve(min_slp_simulation)
		
							

		PBLHS = []
		PBLHS = Extract_by_name (csv_file, PBLHS, 'PBLH')

		



		

		if PBL=='ACM2' or PBL=='ACM2_additional_changs':
			number=10
		else: number=10
		exch_list=[]
		exch=Extract_by_name(csv_file,exch_list,'avg_vert_exch_scalar')

		

		exch_list=[]
		exch=Extract_by_name(csv_file,exch_list,'avg_vert_exch_momentum')
		

		


		Wind_Speed = []
		# Wind_Speed_simulation = flatten_the_curve(Extract_by_name (csv_file, Wind_Speed, 'All_Max_WND_SPD_10'))
		Wind_Speed_simulation = Extract_by_name (csv_file, Wind_Speed, 'All_Max_WND_SPD_10')

		# if HN=='Maria':
		# 	Eye_Longs=Eye_Longs[:len(Real_Winds)-number_of_points]
		# 	Eye_Lats=Eye_Lats[:len(Real_Winds)-number_of_points]
			



		# TRACK
		ax1.plot(Eye_Longs[0:len(Eye_Lats)], Eye_Lats[0:len(Eye_Lats)], color=colors[c], linestyle=line_stylez[PBL_counter], marker='.', 
			linewidth='1',markersize='7', transform=ccrs.PlateCarree(), label= (PBL+'-'+CLS[cls_counter]))
		ax1.set_title('Track')
		# MIN SLP
		ax2.plot(Times[0:len(Eye_Lats)], min_slp_simulation[0:len(Eye_Lats)], color = colors[c] , linestyle=line_stylez[PBL_counter],
		linewidth='2', marker='.', markersize='10',label=(PBL+' hpbl - '+CLS[cls_counter]))
		ax2.set_xlabel('Times')
		# ax2.set_ylabel('[mb]')
		ax2.set_title('min SLP [mb]')
		#PBLHS
		ax3.plot(Times[0:len(Eye_Lats)], PBLHS[0:len(Eye_Lats)], color = colors[c] , linestyle=line_stylez[PBL_counter],
		linewidth='2', marker='.', markersize='10',label=(PBL+' hpbl - '+CLS[cls_counter]))
		ax3.set_xlabel('Times')
		# ax3.set_ylabel('[m]')
		ax3.set_title('HBL [m]')
		#SCALAR EXCHANGE
		ax11.plot(exch[0:number],lvl_heights[0:number], color = colors[c] , linestyle=line_stylez[PBL_counter],
		linewidth='2', marker='.', markersize='10',label=(PBL+' hpbl - '+CLS[cls_counter]))
		ax11.set_label('exch')
		ax11.set_yticks(lvl_heights[0:number])
		ax11.set_title('scalar exch [m/s]')
		#WIND INTENSITY
		ax12.plot(Times[0:len(Eye_Lats)], Wind_Speed_simulation[0:len(Eye_Lats)], color = colors[c] , linestyle=line_stylez[PBL_counter],
		linewidth='2', marker='.', markersize='10',label=(PBL+' hpbl - '+CLS[cls_counter]))
		ax12.set_xlabel('Times')
		ax12.set_title('Wind intensity [m/s]')
		#MOMENTUM EXCHANGE
		ax13.plot(exch[0:number],lvl_heights[0:number], color = colors[c] , linestyle=line_stylez[PBL_counter],
		linewidth='2', marker='.', markersize='10',label=(PBL+' hpbl - '+CLS[cls_counter]))
		ax13.set_xlabel('exch')
		ax13.set_yticks(lvl_heights[0:number])
		ax13.set_title('momentum exch [m/s]')

		cls_counter+=1
		c+=1
	PBL_counter+=1
xticks=[]
for i in range(len(Real_Lats)):
	time_idx=i*6
	xticks.append(time_idx)

handles, labels = fig.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax2.set_xticks(xticks)
ax3.set_xticks(xticks)
ax12.set_xticks(xticks)


fig.legend(by_label.values(), CLS, loc = 'upper center', mode='expand',
			 ncol = 3, bbox_to_anchor=(0.65, 0.96, -0.3, 0),frameon = False)
fig.suptitle(HN+' - '+GS+' - '+TM+' - '+PBL, fontsize=18)
plt.show()
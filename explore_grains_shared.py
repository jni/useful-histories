import numpy as np
import matplotlib.pyplot as plt

# Load quat, ebsd and hrdic packages from defdap package
from defdap import quat
from defdap import ebsd
from defdap import hrdic

from defdap.plotting import MapPlot
import os

from scipy.signal import medfilt, find_peaks_cwt, find_peaks
from scipy import signal
from skimage.transform import radon, rescale, resize,frt2
from matplotlib import gridspec
from skimage.transform import (hough_line, hough_line_peaks)

from defdap.plotting import Plot, GrainPlot
from scipy import ndimage

import warnings
warnings.filterwarnings('ignore')

import csv

def get_slipsystem_info(grainID,DicMap):
    
    #Load the slip systems for the current phase
    ssGroup = DicMap[grainID].ebsdGrain.phase.slipSystems

    #Calculate the schmid factor of each slip system
    SchmidFactor = DicMap[grainID].ebsdGrain.averageSchmidFactors

    #Calculate the slip trace angles
    DicMap[grainID].ebsdGrain.calcSlipTraces()
    ST_Angle=np.rad2deg(DicMap[grainID].ebsdGrain.slipTraceAngles)

    # print the slip plane of each trace, the max Schmid factor of it and its angle (by degree)

    info_frame = []
    for i in range(0,4):
        
        info_frame.append([])
        info_frame[i].append('Slip plane {0}:'.format(i+1))
        info_frame[i].append(ssGroup[i][0].slipPlaneLabel)
        info_frame[i].append('| SF:')
        SF_round = round(max(SchmidFactor[i]),3)
        info_frame[i].append(SF_round)
        info_frame[i].append('| Angle:')
        angle_round = round(ST_Angle[i],3)
        info_frame[i].append(angle_round)
        #print('Slip plane {0}:'.format(i+1),ssGroup[i][0].slipPlaneLabel,'| SF:',max(SchmidFactor[i]),'| Angle:',ST_Angle[i])
    #print(info_frame)
    
    ###
    ###
    ###
    
    #Order the slip planes by the Schmid Factor
    info_frame = sorted(info_frame, reverse=True, key = lambda x: (x[3]))
    #print(info_frame)
    
    theo_angle = []
    SF_list = []
    #print(len(info_frame))
    for i in range(0,len(info_frame)):
        theo_angle.append(info_frame[i][5])
        SF_list.append(info_frame[i][3])
    return theo_angle,SF_list

# Extract the Grain data (eMaxShear)
def take_shear_data(grainID,DicMap):
    
    X0 = DicMap[grainID].extremeCoords[0]
    Y0 = DicMap[grainID].extremeCoords[1]
    Xmax = DicMap[grainID].extremeCoords[2]
    Ymax = DicMap[grainID].extremeCoords[3]

    xCentre = round((Xmax + X0) / 2)
    yCentre = round((Ymax + Y0) / 2)

    xCentre -= X0
    yCentre -= Y0

    bg = np.nan
    fg = 0
    outline = np.full((Ymax - Y0 + 1, Xmax - X0 + 1), bg, dtype=int)
    for coord in DicMap[grainID].coordList:
        outline[coord[1] - Y0, coord[0] - X0] = fg

    grainMapData = np.full((Ymax - Y0 + 1, Xmax - X0 + 1), np.nan,
                           dtype=type(DicMap[grainID].maxShearList[0]))

    for coord, data in zip(DicMap[grainID].coordList, DicMap[grainID].maxShearList):
        grainMapData[coord[1] - Y0, coord[0] - X0] = data
    
    return grainMapData

def signaltonoise(a,axis=0,ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m/sd)

def sb_angle(shear_map,threshold=None,median_filter=None):
    if threshold != None:
        shear_map_filt=shear_map>threshold
        strain_title='Threshold: {:2.3f}'.format(threshold)
    else:
        shear_map_filt=shear_map
        strain_title='Shear strain: no threshold'
    
    if median_filter !=None:    
        shear_map_filt=ndimage.median_filter(shear_map_filt, size=median_filter)
    
    sin_map = radon(shear_map_filt)
    profile_filt=np.max(sin_map,axis=0)
    
    plt.figure(figsize=(13,5))
    gs = gridspec.GridSpec(1, 3) 
    ax0=plt.subplot(gs[0])
    ax1=plt.subplot(gs[1])
    ax2=plt.subplot(gs[2])
    ax0.imshow(shear_map_filt,cmap='viridis')
    
    ax0.set_title(strain_title)
    ax1.imshow(sin_map,cmap='viridis')
    ax1.set_title('Sinogram')
    #angles_index = signal.find_peaks_cwt(profile_filt,np.arange(1,10))
    angles_index = signal.find_peaks(profile_filt,prominence=5)
    
    #print('angles =',angles_index)
    ax2.plot(profile_filt)
    #print(profile_filt)
    ax2.set_title('Band angle distribution')
    ax2.set_xlabel(r'Angle in degrees')
    ax2.set_ylabel(r'Intensity')
    return profile_filt.tolist(),angles_index

def detect_angle(list1,Index):   
    values = []
    #print(list1)
    #print(index[0])
    for i in Index[0]:
        #print(i)
        values.append(list1[i])
    #print(values)
    if values != []:
        detected_angle = Index[0][values.index(max(values))]
    else:
        detected_angle = 'None'
    return detected_angle

#Save all the angles detected 
def save_detected_angles(list1,Index):
    angle_value = []
    for i in range(0,len(Index[0])):
        #print(i)
        angle_value.append([])
        #print(Index[0][i])
        angle_value[i].append(Index[0][i])
        angle_value[i].append(round(list1[Index[0][i]],3))
    #sort the list by the values 
    angle_value = sorted(angle_value, reverse= True,key = lambda x: (x[1]))
    bottom = min(list1)
    return angle_value,bottom

#Check if there is a second peak
def bi_slip_check(SDA, bottom):
    if len(SDA) > 1:
        if (SDA[0][1]-bottom)*0.5 < (SDA[1][1]-bottom):
            bi_slip = 'Two'
            detected_angle2 = SDA[1][0]
        else:
            bi_slip = 'None'
            detected_angle2 = 'None'
    else:
        bi_slip = 'None'
        detected_angle2 = 'None'
    return bi_slip,detected_angle2

def get_slipsystem_info2(grainID,DicMap):
    
    #Load the slip systems for the current phase
    ssGroup = DicMap[grainID].ebsdGrain.phase.slipSystems

    #Calculate the schmid factor of each slip system
    SchmidFactor = DicMap[grainID].ebsdGrain.averageSchmidFactors

    #Calculate the slip trace angles
    DicMap[grainID].ebsdGrain.calcSlipTraces()
    ST_Angle=np.rad2deg(DicMap[grainID].ebsdGrain.slipTraceAngles)

    # print the slip plane of each trace, the max Schmid factor of it and its angle (by degree)

    info_frame = []
    for i in range(0,4):
        info_frame.append([])
        info_frame[i].append('Slip plane {0}:'.format(i+1))
        info_frame[i].append(ssGroup[i][0].slipPlaneLabel)
        info_frame[i].append('| SF:')
        info_frame[i].append(max(SchmidFactor[i]).round(3))
        info_frame[i].append('| Angle:')
        info_frame[i].append(ST_Angle[i].round(2))
    
    #Order the slip planes by the Schmid Factor
    info_frame = sorted(info_frame, reverse=True, key = lambda x: (x[3]))
    
    #print(info_frame)
    return info_frame

def Plotsliptrace(k,DicMap):
    fig = plt.figure(figsize=(13,4))
    gs = gridspec.GridSpec(1, 3) 
    ax0=plt.subplot(gs[0])
    ax1=plt.subplot(gs[1])
    ax2=plt.subplot(gs[2])

    slipPlot = GrainPlot(fig=fig, callingGrain=DicMap[k], ax=ax0)
    slipPlot.addSlipTraces(topOnly=True)
    info_frame = get_slipsystem_info2(k,DicMap =DicMap)
    
    for i in range(0,len(info_frame)):
        if info_frame[i][0] == 'Slip plane 1:':
            Color = 'blue'
        elif info_frame[i][0] == 'Slip plane 2:':
            Color = 'green'
        elif info_frame[i][0] == 'Slip plane 3:':
            Color = 'red'
        elif info_frame[i][0] == 'Slip plane 4:':
            Color = 'purple'
        ax1.text(0,1-0.2*i,'{}'.format(info_frame[i]),color = Color)

    grainMapData = take_shear_data(k,DicMap=DicMap)
    im = ax2.imshow(grainMapData,vmin=0,vmax=0.1,interpolation='bilinear',cmap='viridis')
    ax0.axis('off')
    ax1.axis('off')
    ax2.axis('off')
    
def matching(detected_angle,theo_angle):
    if detected_angle != 'None':
        diff_exp_theo = []
        for t_angle in theo_angle:
            diff_exp_theo.append(abs(detected_angle-t_angle))
            
        ordered_diff = sorted(diff_exp_theo)
        #print(ordered_diff)
        if ordered_diff[0] < 7:
            best_match_index = diff_exp_theo.index(ordered_diff[0])
            MT = best_match_index + 1
            if ordered_diff[1] < 7:
                MT = str(MT) + ' or '+ str(diff_exp_theo.index(ordered_diff[1]) + 1)
        else:
            MT = 'None' 
    else:
        MT = 'None'
    return MT 

def check_all(k,angle_list,theo_angle,angle_index,shear_map,threshold,DicMap,Noise_lim):
    ###
    #   Functions required: 1. GrainPlot 2. get_slipsystem_info2 3. signaltonoise
    #   4. bi_slip_check 5. detect_angle 6. save_detected_angles 7. matching
    ###
    
    ### 
    ###     Calculate the variables needed     ###
    ### 
    
    detected_angle = detect_angle(angle_list,angle_index)
    SDA,bottom = save_detected_angles(angle_list,angle_index)
    
    BiSlip, Detected_Angle2 = bi_slip_check(SDA,bottom)
    SNR = signaltonoise(angle_list)
    #SNR = np.array(1)

    if Detected_Angle2 != 'None':
        MT = []
        MT.append(matching(detected_angle,theo_angle))
        MT.append(matching(Detected_Angle2,theo_angle))
        
    else:
        MT = matching(detected_angle,theo_angle)
    
    
    fig = plt.figure(figsize=(14,9))
    gs = gridspec.GridSpec(2, 3) 
    
    ax0=plt.subplot(gs[0])
    ax1=plt.subplot(gs[1])
    ax2=plt.subplot(gs[2])
    ax3=plt.subplot(gs[3])
    ax4=plt.subplot(gs[4])
    ax5=plt.subplot(gs[5])

    slipPlot = GrainPlot(fig=fig, callingGrain=DicMap[k], ax=ax0)
    slipPlot.addSlipTraces(topOnly=True)
    #traces = slipPlot.addSlipTraces()
    info_frame = get_slipsystem_info2(k,DicMap =DicMap)

    #print the slip plane information 
    
    for i in range(0,len(info_frame)):
        if info_frame[i][0] == 'Slip plane 1:':
            Color = 'blue'
        elif info_frame[i][0] == 'Slip plane 2:':
            Color = 'green'
        elif info_frame[i][0] == 'Slip plane 3:':
            Color = 'red'
        elif info_frame[i][0] == 'Slip plane 4:':
            Color = 'purple'
        ax1.text(0,1-0.2*i,'{}'.format(info_frame[i]),color = Color)
        
    ax1.text(0,0.2,'Angle detected (Strain Map) = {}'.format(detected_angle),color = 'black',weight='bold')

    grainMapData = take_shear_data(k,DicMap =DicMap)
    #grain = DicMap[k].plotMaxShear(plotColourBar=True, plotScaleBar=True, vmin=0, vmax=0.1)
    im = ax2.imshow(grainMapData,vmin=0,vmax=0.1,interpolation='bilinear',cmap='viridis')
    
    ax3.plot(angle_list)
    ax3.set_title('Band angle distribution')
    ax3.set_xlabel(r'Angle in degrees')
    ax3.set_ylabel(r'Intensity')
    
    #Matching status

    ax4.text(0,1,'Signal to Noise: {}'.format(SNR.round(3)),color='green',weight='bold',fontsize=12)
    if SNR != 0:
        if SNR<Noise_lim:
            if detected_angle != 'None':
                ax4.text(0,1.2,'Slip bands detected',color='red',weight='bold',fontsize=12)
                Sb_dected = 'True'
            else:
                ax4.text(0,0.8,'No slip bands detected',color='red',weight='bold',fontsize=12)
                MT = 'None'
                Sb_dected = 'False'
        else:
            ax4.text(0,0.8,'No slip bands detected',color='red',weight='bold',fontsize=12)
            MT = 'None'
            Sb_dected = 'False'
    else:
        ax4.text(0,0.8,'No slip band detected',color='red',weight='bold',fontsize=12)
        MT = 'None'
        Sb_dected = 'False'
    
    if MT != 'None':
        ax4.text(0,0.5,'Matched ={}'.format(MT),color='black',weight='bold',fontsize=12)
    else:
        ax4.text(0,0.5,'Matched:{}'.format(MT),color='red',weight='bold',fontsize=20)
        
    if MT == 1:
        ax4.text(0.2,0.8,'Agreed'.format(MT),color='red',weight='bold',fontsize=30)
    elif type(MT) == list:
        if MT[0] == 1 or MT[1] == 1:
            ax4.text(0.1,0.8,'Agreed with one band'.format(MT),color='red',weight='bold',fontsize=20)
    
    ax4.text(0.2,0.4,'{}'.format(SDA),color='black',fontsize=10)

    
    if SNR<Noise_lim:
        if BiSlip != 'None':
            ax4.text(0.6,1.2,':{}'.format(BiSlip),color='red',fontsize=12)
            ax4.text(0.1,1.1,'1: {0}   2: {1}'.format(detected_angle,Detected_Angle2),color='black',fontsize=12)
    
    #Plot the filtered map
    #shear_map = grainMapData
    #threshold = detect_threshold
    
    median_filter=3
    
    if threshold != None:
        shear_map_filt=shear_map>threshold
        strain_title='Threshold: {:2.3f}'.format(threshold)
    else:
        shear_map_filt=shear_map
        strain_title='Shear strain: no threshold'
    
    if median_filter !=None:    
        shear_map_filt=ndimage.median_filter(shear_map_filt, size=median_filter)
    
    ax5.imshow(shear_map_filt,cmap='viridis')
    ax5.set_title(strain_title) 

    ax0.axis('off')
    ax1.axis('off')
    ax2.axis('off')
    ax4.axis('off')
    ax5.axis('off')
    return Sb_dected, MT, detected_angle, Detected_Angle2

###
#    Function required: 1. get_slipsystem_info 2. sb_angle 3. check_all
###

def grain_explorer_traces(n,DicMap,folder_name='None',Noise_lim='None',Grain_filter=2500):
    if folder_name is None:
        folder_name = 'Slip Trace analysis2'
    if Noise_lim is None:
        Noise_lim = 100

    # Create a folder for current step
    dir = os.path.join(folder_name)
    if not os.path.exists(dir):
        os.mkdir(dir)

    dir = os.path.join(folder_name + '/Step {}'.format(n))
    if not os.path.exists(dir):
        os.mkdir(dir)
        
    dir = os.path.join(folder_name + '/Step {}/Check'.format(n))
    if not os.path.exists(dir):
        os.mkdir(dir)

    # Create a csv to save the information
    header = ['Grain IDs','Theo Angle','Exp Angle','Matched','Band Detected','SF1','SF2','SF3','SF4','Trace observed']
    with open(folder_name + '/information {}.csv'.format(n),'w',newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
    csvfile.close()
    
    #for k in range(0,100): ## for testing, only run a small number of grains
    for k in range(0,len(DicMap.grainList)): 
        grainMapData = take_shear_data(k,DicMap =DicMap)
        if  len(DicMap[k].maxShearList) > Grain_filter:
            print('Grain: ',k)
            dir = os.path.join(folder_name + '/Step {0}/Grain {1}'.format(n,k))
            if not os.path.exists(dir):
                os.mkdir(dir)
            
            DicMap[k].plotMaxShear(plotColourBar=True, plotScaleBar=True, vmin=0, vmax=0.1)
            plt.savefig(folder_name + '/Step {0}/Grain {1}/Grain profile'.format(n,k),dpi = 300)
            plt.close()
            
            Plotsliptrace(k,DicMap =DicMap)
            plt.savefig(folder_name + '/Step {0}/Grain {1}/4 Slip traces'.format(n,k),dpi = 300)
            plt.close()
            
            # gert the mean max shear strain of the grain
            mean_shear_strain = np.mean(DicMap[k].maxShearList)
            detect_threshold = max(1.6 * mean_shear_strain,0.013)
        
            # get the theo angle
            theo_angle,SF_list = get_slipsystem_info(k,DicMap=DicMap)

            # get the experimental angle
            angle_list,angle_index = sb_angle(grainMapData,threshold=detect_threshold,median_filter=3)
            
            plt.savefig(folder_name + '/Step {0}/Grain {1}/Radon'.format(n,k),dpi = 300)
            plt.close()

            #detected_angle = detect_angle(angle_list,angle_index)
            #SDA,bottom = save_detected_angles(angle_list,angle_index)
            #MT = matching(detected_angle,theo_angle)
            
            Sb_dected, MT, detected_angle, detected_angle2 = check_all(k,angle_list=angle_list,theo_angle=theo_angle,angle_index=angle_index,shear_map=grainMapData,threshold=detect_threshold,DicMap=DicMap,Noise_lim=Noise_lim)
            
            plt.savefig(folder_name + '/Step {0}/Check/Grain {1}'.format(n,k),dpi = 300)
            plt.close()

            if detected_angle2 != 'None':
                detected_angles = []
                detected_angles.append(detected_angle)
                detected_angles.append(detected_angle2)
                data_rows = [[k, theo_angle[0], detected_angles, MT, Sb_dected,SF_list[0],SF_list[1],SF_list[2],SF_list[3]]]
            else:
                data_rows = [[k, theo_angle[0], detected_angle, MT, Sb_dected,SF_list[0],SF_list[1],SF_list[2],SF_list[3]]]

            with open(folder_name + '/information {}.csv'.format(n),'a',newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data_rows)
            csvfile.close()
    print('Step:',n)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load quat, ebsd and hrdic packages from defdap package
from defdap import quat
from defdap import ebsd
from defdap import hrdic

from defdap.plotting import MapPlot
import os

from scipy.signal import medfilt, find_peaks_cwt, find_peaks
from scipy import signal
from skimage.transform import radon, rescale, resize, frt2
from matplotlib import gridspec
from skimage.transform import (hough_line, hough_line_peaks)
from skimage import measure

from defdap.plotting import Plot, GrainPlot
from scipy import ndimage
from tqdm import tqdm

import warnings

warnings.filterwarnings('ignore')

import csv


def get_slipsystem_info(grainID, DicMap):
    """Grab slip system for a specific grain.

    Parameters
    ----------
    grainID : int
        The ID of the grain to examine.
    DicMap : defdap.hrdic.Map object
        The DIC map.

    Returns
    -------
    theo_angle : list of float
        Theoretical angles computed from EBSD data.
    SF_list : list of float
        Schmid Factor list.
    """

    #Load the slip systems for the current phase
    ssGroup = DicMap[grainID].ebsdGrain.phase.slipSystems

    #Calculate the schmid factor of each slip system
    SchmidFactor = DicMap[grainID].ebsdGrain.averageSchmidFactors

    #Calculate the slip trace angles
    DicMap[grainID].ebsdGrain.calcSlipTraces()
    ST_Angle = np.rad2deg(DicMap[grainID].ebsdGrain.slipTraceAngles)

    # print the slip plane of each trace, the max Schmid factor of it and its angle (by degree)

    info_frame = []
    for i in range(0, 4):

        info_frame.append([])
        info_frame[i].append('Slip plane {0}:'.format(i + 1))
        info_frame[i].append(ssGroup[i][0].slipPlaneLabel)
        info_frame[i].append('| SF:')
        SF_round = round(max(SchmidFactor[i]), 3)
        info_frame[i].append(SF_round)
        info_frame[i].append('| Angle:')
        angle_round = round(ST_Angle[i], 3)
        info_frame[i].append(angle_round)
        #print('Slip plane {0}:'.format(i+1),ssGroup[i][0].slipPlaneLabel,'| SF:',max(SchmidFactor[i]),'| Angle:',ST_Angle[i])
    #print(info_frame)

    ###
    ###
    ###

    #Order the slip planes by the Schmid Factor
    info_frame = sorted(info_frame, reverse=True, key=lambda x: (x[3]))
    #print(info_frame)

    theo_angle = []
    SF_list = []
    #print(len(info_frame))
    for i in range(0, len(info_frame)):
        theo_angle.append(info_frame[i][5])
        SF_list.append(info_frame[i][3])
    return theo_angle, SF_list


# Extract the Grain data (eMaxShear)
def take_shear_data(grainID, DicMap):
    """Find e_max_shear for specific grain.

    Parameters
    ----------
    grainID : int
        ID of the grain.
    DicMap : defdap.hrdic.Map object
        The DIC map.

    Returns
    -------
    grainMapData : numpy ndarray, shape (M, N)
        The max shear over the full grain, shape large enough to contain the
        grain bounding box.
    """

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

    grainMapData = np.full((Ymax - Y0 + 1, Xmax - X0 + 1),
                           np.nan,
                           dtype=type(DicMap[grainID].maxShearList[0]))

    coord_array = np.array(DicMap[grainID].coordList)[:, [1, 0]]
    data_array = np.array(DicMap[grainID].maxShearList)
    grainMapData[tuple(np.transpose(coord_array - [Y0, X0]))] = data_array

    # lines replaced by NumPy assignment above 👆
    # for coord, data in zip(DicMap[grainID].coordList,
    #                        DicMap[grainID].maxShearList):
    #     grainMapData[coord[1] - Y0, coord[0] - X0] = data

    return grainMapData


def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m / sd)


def sb_angle(shear_map, threshold=None, median_filter=None):
    """Compute slip band angles based on shear map.

    Uses a threshold to reduce noise, optionally followed by a median filter,
    then a radon transform to find the angles.

    Parameters
    ----------
    shear_map : numpy ndarray, shape (M, N)
        The input shear map.
    threshold : float
        Threshold value for the array.
    median_filter : int or None
        The size of the median filter to apply for denoising. None means no
        median filter is applied.

    Returns
    -------
    profile_filt : list of float
        Maximum intensity of radon transform at that angle.
    angles_index : tuple[array of int, properties dict]
        Positions of peaks in the profile as found by scipy.signal.find_peaks.
    """
    if threshold != None:
        shear_map_filt = shear_map > threshold
        strain_title = 'Threshold: {:2.3f}'.format(threshold)
    else:
        shear_map_filt = shear_map
        strain_title = 'Shear strain: no threshold'

    if median_filter != None:
        shear_map_filt = ndimage.median_filter(shear_map_filt,
                                               size=median_filter)

    sin_map = radon(shear_map_filt)
    profile_filt = np.max(sin_map, axis=0)

    plt.figure(figsize=(13, 5))
    gs = gridspec.GridSpec(1, 3)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])
    ax2 = plt.subplot(gs[2])
    ax0.imshow(shear_map_filt, cmap='viridis')

    ax0.set_title(strain_title)
    ax1.imshow(sin_map, cmap='viridis')
    ax1.set_title('Sinogram')
    #angles_index = signal.find_peaks_cwt(profile_filt,np.arange(1,10))
    angles_index = signal.find_peaks(profile_filt, prominence=5)

    #print('angles =',angles_index)
    ax2.plot(profile_filt)
    #print(profile_filt)
    ax2.set_title('Band angle distribution')
    ax2.set_xlabel(r'Angle in degrees')
    ax2.set_ylabel(r'Intensity')
    return profile_filt.tolist(), angles_index


def detect_angle(list1, Index):
    """Grab highest peak based on indices given by scipy.signal.

    Parameters
    ----------
    list1 : list of float
        Radon transform intensities.
    Index : tuple[array of int, properties dict]
        Indices of highest peaks as returned by scipy.signal.

    Returns
    -------
    detected_angle : int
        Index of the highest peak in list1. List1 has positions 0-179, so this
        will be an angle in degrees.
    """
    values = []
    #print(list1)
    #print(index[0])
    for i in Index[0]:
        #print(i)
        values.append(list1[i])
    #print(values)
    if values != []:
        # todo: use numpy and np.argmax
        detected_angle = Index[0][values.index(max(values))]
    else:
        # todo: use None
        detected_angle = 'None'
    return detected_angle


#Save all the angles detected
def save_detected_angles(list1, Index):
    """Same as `detect_angle` but return *all* detected angles, not just max.

    Parameters
    ----------
    list1 : list of float
        Radon transform intensities.
    Index : tuple[array of int, properties dict]
        Indices of highest peaks as returned by scipy.signal.

    Returns
    -------
    angle_value : list of ints
        List of all angles detected.
    bottom : float
        The minimum value in the radon transform profile.
    """
    angle_value = []
    for i in range(0, len(Index[0])):
        #print(i)
        angle_value.append([])
        #print(Index[0][i])
        angle_value[i].append(Index[0][i])
        angle_value[i].append(round(list1[Index[0][i]], 3))
    #sort the list by the values
    angle_value = sorted(angle_value, reverse=True, key=lambda x: (x[1]))
    bottom = min(list1)
    return angle_value, bottom


#Check if there is a second peak
def bi_slip_check(SDA, bottom):
    """Check whether there are two slips.

    Parameters
    ----------
    SDA : list of int
        List of all detected angles.
    bottom : float
        Minimum value in the radon transform profile.
    """
    if len(SDA) > 1:
        if (SDA[0][1] - bottom) * 0.5 < (SDA[1][1] - bottom):
            bi_slip = 'Two'
            detected_angle2 = SDA[1][0]
        else:
            bi_slip = 'None'
            detected_angle2 = 'None'
    else:
        bi_slip = 'None'
        detected_angle2 = 'None'
    return bi_slip, detected_angle2


def get_slipsystem_info2(grainID, DicMap):
    """Grab slip system for a specific grain.

    Parameters
    ----------
    grainID : int
        The ID of the grain to examine.
    DicMap : defdap.hrdic.Map object
        The DIC map.

    Returns
    -------
    info_frame : list of lists
        Contains Slip plane labels, schmid factors, and slip trace angles.
    """

    #Load the slip systems for the current phase
    ssGroup = DicMap[grainID].ebsdGrain.phase.slipSystems

    #Calculate the schmid factor of each slip system
    schmidFactor = DicMap[grainID].ebsdGrain.averageSchmidFactors

    #Calculate the slip trace angles
    DicMap[grainID].ebsdGrain.calcSlipTraces()
    ST_Angle = np.rad2deg(DicMap[grainID].ebsdGrain.slipTraceAngles)

    ids = np.arange(1, 5)
    labels = [ssGroup[i][0].slipPlaneLabel for i in range(4)]
    sfs = [max(schmidFactor[i]) for i in range(4)]
    angles = [ST_Angle[i] for i in range(4)]
    frame = pd.DataFrame({
            'slip_plane': ids,
            'sp_label': labels,
            'sf': sfs,
            'angle_degs': angles,
            'color': ['blue', 'green', 'red', 'purple'],
            })
    return frame


def plot_slip_trace(k, DicMap, axes=None):
    """Plot the slip trace.

    k: grainID
    DicMap: defdap.hrdic.Map
    axes: List[Axes], optional
        A list of three matplotlib axes on which to plot the GrainPlot (with
        the shear angles), the possible slip angles, and the shear data.
    """
    if axes is None:
        fig = plt.figure(figsize=(13, 4))
        gs = gridspec.GridSpec(1, 3)
        ax0 = plt.subplot(gs[0])
        ax1 = plt.subplot(gs[1])
        ax2 = plt.subplot(gs[2])
    else:
        ax0, ax1, ax2 = axes
        fig = ax0.figure

    info_frame = get_slipsystem_info2(k, DicMap=DicMap)
    frame_sorted = info_frame.sort_values(
            by='sf', ascending=False, ignore_index=True
            )

    slipPlot = GrainPlot(fig=fig, callingGrain=DicMap[k], ax=ax0)
    slipPlot.addSlipTraces(topOnly=True, colours=info_frame['color'])
    ax0.axis('off')

    for i, (row, color) in enumerate(zip(
            frame_sorted.drop('color', axis=1).round(2).itertuples(
                    index=False, name='ST'),
            frame_sorted['color']
            )):
        ax1.text(0, 1 - 0.2 * i, str(row), color=color)
    ax1.axis('off')

    grainMapData = take_shear_data(k, DicMap=DicMap)
    im = ax2.imshow(
            grainMapData,
            vmin=0, vmax=0.1, interpolation='bilinear', cmap='viridis',
            )
    ax2.axis('off')


def matching(detected_angle, theo_angle):
    """Check whether detected angle matches theoretical angle.

    Parameters
    ----------
    detected_angle : int
        The detected angle in degrees in the grain using radon transform method.
    theo_angle : list of float
        The theoretical angles given the slip systems.

    Returns
    -------
    MT : str or int
        The index + 1 of the theoretical angle match, or two theoretical angle
        matches (if they are less than 7 degrees apart), or None.
    """
    if detected_angle != 'None':
        diff_exp_theo = []
        for t_angle in theo_angle:
            diff_exp_theo.append(abs(detected_angle - t_angle))

        ordered_diff = sorted(diff_exp_theo)
        #print(ordered_diff)
        if ordered_diff[0] < 7:
            best_match_index = diff_exp_theo.index(ordered_diff[0])
            MT = best_match_index + 1
            # todo: make return a list or something, not str, use proper
            # indices
            if ordered_diff[1] < 7:
                MT = str(MT) + ' or ' + str(
                    diff_exp_theo.index(ordered_diff[1]) + 1)
        else:
            MT = 'None'
    else:
        MT = 'None'
    return MT


def check_all(k, angle_list, theo_angle, angle_index, shear_map, threshold,
              DicMap, Noise_lim, plot=False):
    """Run all the functionality in the library for a given grain.

    This function runs:
        - grain plot
        - grab slip system info
        - compute the snr of radon transform max intensities array
        - check for bi-slip systems
        - detect the angle with maximum intensity
        - detect other high intensity angles
        - match the angles to the theoretical angles given the slip system

    If given `plot=False`, all the plotting functionality (which is the
    slowest) is silenced.

    Parameters
    ----------
    k : int
        Grain ID.
    angle_list : list of float, size (180,)
        The profile of max intensities of the radon transform per angle.
    theo_angle : list of float
        The theoretical angles of the slip systems in degrees.
    angle_index : list of int
        Position of the angles of maximum intensity.
    shear_map : numpy array
        Shear map of the current grain.
    threshold : float
        Threshold value to apply to the shear map before the radon transform.
    DicMap : defdap.hrdic.Map object
        The DicMap.
    Noise_lim : float
        Maximum allowable SNR.

    Returns
    -------
    Sb_dected : str {'True', 'False'}
        Whether a slip band was detected. # TODO make real bool
    MT : int or str
        Matched index of theoretical slip band, if any.
    detected_angle : int
        Angle in degrees of detected slip band.
    Detected_Angle2 : int or None
        Angle in degrees of second detected slip band if any.
    """
    ###
    #   Functions required: 1. GrainPlot 2. get_slipsystem_info2 3. signaltonoise
    #   4. bi_slip_check 5. detect_angle 6. save_detected_angles 7. matching
    ###

    ###
    ###     Calculate the variables needed     ###
    ###

    detected_angle = detect_angle(angle_list, angle_index)
    SDA, bottom = save_detected_angles(angle_list, angle_index)

    BiSlip, Detected_Angle2 = bi_slip_check(SDA, bottom)
    SNR = signaltonoise(angle_list)
    #SNR = np.array(1)

    if Detected_Angle2 != 'None':
        MT = []
        MT.append(matching(detected_angle, theo_angle))
        MT.append(matching(Detected_Angle2, theo_angle))

    else:
        MT = matching(detected_angle, theo_angle)

    if plot:
        fig, axes = plt.subplots(2, 3, figsize=(14, 9))
        fig = plt.figure(figsize=(14, 9))
        ax0, ax1, ax2, ax4, ax5 = (fig.add_subplot(230 + i)
                                   for i in [1, 2, 3, 5, 6])
        ax3 = fig.add_subplot(234, projection='polar')
        ax3.set_theta_zero_location('S')

        plot_slip_trace(k, DicMap, axes=(ax0, ax1, ax2))

        ax1.text(0, 0.2,
                f'Angle detected (Strain Map) = {detected_angle}',
                color='black', weight='bold'
                )

        angle_arr = np.concatenate([angle_list, angle_list])
        angles = np.linspace(0, 2*np.pi, 360, endpoint=False)
        ax3.plot(angles, angle_arr)
        ax3.set_title('Band angle distribution')
        ax3.set_xlabel(r'Angle in degrees')
        ax3.set_ylabel(r'Intensity')

        #Matching status

        ax4.text(0, 1,
                f'Signal to Noise: {SNR:.3f}',
                color='green', weight='bold', fontsize=12
                )
        if SNR != 0:
            if SNR < Noise_lim:
                if detected_angle != 'None':
                    ax4.text(0,
                             1.2,
                             'Slip bands detected',
                             color='red',
                             weight='bold',
                             fontsize=12)
                    Sb_dected = 'True'
                else:
                    ax4.text(0,
                             0.8,
                             'No slip bands detected',
                             color='red',
                             weight='bold',
                             fontsize=12)
                    MT = 'None'
                    Sb_dected = 'False'
            else:
                ax4.text(0,
                         0.8,
                         'No slip bands detected',
                         color='red',
                         weight='bold',
                         fontsize=12)
                MT = 'None'
                Sb_dected = 'False'
        else:
            ax4.text(0,
                     0.8,
                     'No slip band detected',
                     color='red',
                     weight='bold',
                     fontsize=12)
            MT = 'None'
            Sb_dected = 'False'

        if MT != 'None':
            ax4.text(0,
                     0.5,
                     'Matched ={}'.format(MT),
                     color='black',
                     weight='bold',
                     fontsize=12)
        else:
            ax4.text(0,
                     0.5,
                     'Matched:{}'.format(MT),
                     color='red',
                     weight='bold',
                     fontsize=20)

        if MT == 1:
            ax4.text(0.2,
                     0.8,
                     'Agreed'.format(MT),
                     color='red',
                     weight='bold',
                     fontsize=30)
        elif type(MT) == list:
            if MT[0] == 1 or MT[1] == 1:
                ax4.text(0.1,
                         0.8,
                         'Agreed with one band'.format(MT),
                         color='red',
                         weight='bold',
                         fontsize=20)

        ax4.text(0.2, 0.4, '{}'.format(SDA), color='black', fontsize=10)
        ax4.axis('off')

        if SNR < Noise_lim:
            if BiSlip != 'None':
                ax4.text(0.6, 1.2, ':{}'.format(BiSlip), color='red', fontsize=12)
                ax4.text(0.1,
                         1.1,
                         '1: {0}   2: {1}'.format(detected_angle, Detected_Angle2),
                         color='black',
                         fontsize=12)

        #Plot the filtered map
        #shear_map = grainMapData
        #threshold = detect_threshold

        median_filter = 3

        if threshold != None:
            shear_map_filt = shear_map > threshold
            strain_title = 'Threshold: {:2.3f}'.format(threshold)
        else:
            shear_map_filt = shear_map
            strain_title = 'Shear strain: no threshold'

        if median_filter != None:
            shear_map_filt = ndimage.median_filter(shear_map_filt,
                                                   size=median_filter)

        ax5.imshow(shear_map_filt, cmap='viridis')
        ax5.set_title(strain_title)
        ax5.axis('off')

    return Sb_dected, MT, detected_angle, Detected_Angle2


###
#    Function required: 1. get_slipsystem_info 2. sb_angle 3. check_all
###


def grain_explorer_traces(n,
                          DicMap,
                          folder_name=None,
                          Noise_lim=None,
                          Grain_filter=2500):
    """Function to explore grain traces for given stretch timestep.

    Parameters
    ----------
    n : int
        Step to compute. This is the integer step, not the index of the steps.
    DicMap : defdap.hrdic.Map
        The DicMap corresponding to this step.
    folder_name : str
        Folder for the output.
    Noise_lim : float
        The maximum SNR.
    Grain_filter : int
        The minimum grain size in pixels.
    """
    if folder_name is None:
        folder_name = 'Slip Trace analysis2'
    if Noise_lim is None:
        Noise_lim = 100

    # Create a folder for current step
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    folder_name_step = os.path.join(folder_name, f'Step {n}')
    if not os.path.exists(folder_name_step):
        os.mkdir(folder_name_step)

    folder_name_check = os.path.join(folder_name_step, 'Check')
    if not os.path.exists(folder_name_check):
        os.mkdir(folder_name_check)

    # Create a csv to save the information
    header = [
        'Grain IDs', 'Theo Angle', 'Exp Angle', 'Matched', 'Band Detected',
        'SF1', 'SF2', 'SF3', 'SF4', 'Trace observed'
    ]
    with open(folder_name + '/information {}.csv'.format(n), 'w',
              newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
    csvfile.close()

    grains = np.clip(DicMap.grains, 0, None)
    max_shear = DicMap.crop(DicMap.data.max_shear)
    props = [prop
            for prop in measure.regionprops(grains, max_shear)
            if prop.area > Grain_filter]
    for prop in tqdm(props):
        k = prop.label - 1  # position in DicMap list
        # grainMapData = take_shear_data(k, DicMap=DicMap)
        grainMapData = prop.intensity_image
        grainMapData[~prop.image] = np.nan

        fig, axes = plt.subplots(1, 3)
        plot_slip_trace(k, DicMap=DicMap, axes=axes)
        os.makedirs(folder_name + f'/Step {n}/Grain {k}', exist_ok=True)
        fig.savefig(folder_name +
                    f'/Step {n}/Grain {k}/4 Slip traces',
                    dpi=300)
        plt.close()

        # gert the mean max shear strain of the grain
        mean_shear_strain = np.mean(DicMap[k].maxShearList)
        detect_threshold = max(1.6 * mean_shear_strain, 0.013)

        # get the theo angle
        theo_angle, SF_list = get_slipsystem_info(k, DicMap=DicMap)

        # get the experimental angle
        angle_list, angle_index = sb_angle(grainMapData,
                                           threshold=detect_threshold,
                                           median_filter=3)

        plt.savefig(folder_name + '/Step {0}/Grain {1}/Radon'.format(n, k),
                    dpi=300)
        plt.close()

        #detected_angle = detect_angle(angle_list,angle_index)
        #SDA,bottom = save_detected_angles(angle_list,angle_index)
        #MT = matching(detected_angle,theo_angle)

        Sb_dected, MT, detected_angle, detected_angle2 = check_all(
            k,
            angle_list=angle_list,
            theo_angle=theo_angle,
            angle_index=angle_index,
            shear_map=grainMapData,
            threshold=detect_threshold,
            DicMap=DicMap,
            Noise_lim=Noise_lim,
            plot=True,
            )

        plt.savefig(folder_name + '/Step {0}/Check/Grain {1}'.format(n, k),
                    dpi=300)
        plt.close()

        if detected_angle2 != 'None':
            detected_angles = []
            detected_angles.append(detected_angle)
            detected_angles.append(detected_angle2)
            data_rows = [[
                k, theo_angle[0], detected_angles, MT, Sb_dected,
                SF_list[0], SF_list[1], SF_list[2], SF_list[3]
            ]]
        else:
            data_rows = [[
                k, theo_angle[0], detected_angle, MT, Sb_dected,
                SF_list[0], SF_list[1], SF_list[2], SF_list[3]
            ]]

        with open(folder_name + '/information {}.csv'.format(n),
                  'a',
                  newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data_rows)
        csvfile.close()
    print('Step:', n)

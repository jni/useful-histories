# IPython log file


with open('request.txt', mode='r') as fin:
    wells = [line.strip() for line in fin]
    
wells
plates = ['_'.join(well.split('_')[:2]) for well in wells]
plates
set.intersection(plates, os.listdir('/Volumes/King-Ecad-Screen-Tiffs2/tiffs/'))
set.intersection(set(plates), set(os.listdir('/Volumes/King-Ecad-Screen-Tiffs2/tiffs/')))
hdd = '/Volumes/King-Ecad-Screen-Tiffs2/tiffs/'
avail = list(set.intersection(set(plates), set(os.listdir(hdd))))
from glob import glob
import shutil
get_ipython().run_line_magic('pinfo', 'shutil.copyfile')
len(plates) == len(set(plates))
for well in wells:
    plate = '_'.join(well.split('_')[:2])
    if plate in avail:
        files = sorted(glob(os.path.join(hdd, plate, well + '*')))
        for file in files:
            shutil.copyfile(file, '.')
            print(f'copied: {os.path.basename(file)}')
            
for well in wells:
    plate = '_'.join(well.split('_')[:2])
    if plate in avail:
        files = sorted(glob(os.path.join(hdd, plate, well + '*')))
        for file in files:
            basename = os.path.basename(file)
            shutil.copyfile(file, os.path.join('.', basename))
            print(f'copied: {basename}')
            
hdd = '/Volumes/King-Ecad-Screen-Tiffs/tiff/
hdd = '/Volumes/King-Ecad-Screen-Tiffs/tiff/'
avail2 = list(set.intersection(set(plates), set(os.listdir(hdd))))
set.difference(set(plates), set(avail2).union(set(avail)))
not_avail = _18
for well in wells:
    plate = '_'.join(well.split('_')[:2])
    if plate in avail2:
        files = sorted(glob(os.path.join(hdd, plate, well + '*')))
        for file in files:
            basename = os.path.basename(file)
            shutil.copyfile(file, os.path.join('.', basename))
            print(f'copied: {basename}')
            
for well in wells:
    plate = '_'.join(well.split('_')[:2])
    if plate in not_avail:
        print(well)
        
for well in wells:
    plate = '_'.join(well.split('_')[:2])
    if plate not in not_avail:
        print(well)
        

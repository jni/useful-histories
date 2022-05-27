# IPython log file
import numpy as np


import typing as t
ImageData = t.Annotated[np.ndarray, 'image']
x : ImageData = np.random.random((512, 512))

print(__annotations__)

def gaussian(image: ImageData, sigma: int = 1) -> ImageData:
    return image

print(gaussian.__annotations__)
print(gaussian.__annotations__['image'] is __annotations__['x'])

ImageNewData = t.NewType('ImageNewData', np.ndarray)
ImageNewData
y : ImageNewData = np.random.random((512, 512))
print(__annotations__['y'] is ImageNewData)

LabelsData = t.Annotated[np.ndarray, 'labels']

def slic(image: ImageData) -> LabelsData:
    return (image * 256).astype(int)

class Segmenter(t.Protocol):
    def __call__(image: ImageData) -> LabelsData:
        ...

def map_segments(f: Segmenter, images: List[ImageData]) -> List[LabelsData]:
    ...

class Segmenter(t.Protocol):
    def __call__(image: ImageData, *args, **kwargs) -> LabelsData:
        ...

def slic(image: ImageData, n_segments: int = 200) -> LabelsData:
    return (image * n_segments).astype(int)



__all__ = ['slice_image']

import math

import ants
from ants.decorators import image_method
from ants.internal import get_lib_fn

@image_method
def slice_image(image, axis, idx, collapse_strategy=0):
    """
    Slice an image.

    Arguments
    ---------
    axis: integer 
        Which axis.

    idx: integer
        Which slice number.    

    collapse_strategy:  integer
        Collapse strategy for sub-matrix: 0, 1, or 2.  0: collapse to sub-matrix 
        if positive-definite.  Otherwise throw an exception. Default.  1: Collapse 
        to identity.  2:  Collapse to sub-matrix if positive definite. Otherwise
        collapse to identity.

    Example
    -------
    >>> import ants
    >>> mni = ants.image_read(ants.get_data('mni'))
    >>> mni2 = ants.slice_image(mni, axis=1, idx=100)
    """
    if image.dimension == 2:
        if axis == 0:
            return image[idx,:]
        elif axis == 1:
            return image[:,idx]
        raise Exception('Parameters not understood for 2D image.')
        
    if collapse_strategy != 0 and collapse_strategy != 1 and collapse_strategy != 2:
        raise ValueError('collapse_strategy must be 0, 1, or 2.') 

    inpixeltype = image.pixeltype
    ndim = image.dimension
    if image.pixeltype != 'float':
        image = image.clone('float')

    libfn = get_lib_fn('sliceImage')
    itkimage = libfn(image.pointer, axis, idx, collapse_strategy)

    return ants.from_pointer(itkimage).clone(inpixeltype)



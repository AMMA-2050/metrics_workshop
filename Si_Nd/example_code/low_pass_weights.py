"""
Applying a filter to a time-series
==================================

This example demonstrates low pass filtering a time-series by applying a
weighted running mean over the time dimension.

The time-series used is the Darwin-only Southern Oscillation index (SOI),
which is filtered using two different Lanczos filters, one to filter out
time-scales of less than two years and one to filter out time-scales of
less than 7 years.

References
----------

    Duchon C. E. (1979) Lanczos Filtering in One and Two Dimensions.
    Journal of Applied Meteorology, Vol 18, pp 1016-1022.

    Trenberth K. E. (1984) Signal Versus Noise in the Southern Oscillation.
    Monthly Weather Review, Vol 112, pp 326-332

"""
import numpy as np
import matplotlib.pyplot as plt
import iris
import iris.plot as iplt


def low_pass_weights(window, cutoff):
    """Calculate weights for a low pass Lanczos filter.

    Args:

    window: int
        The length of the filter window.

    cutoff: float
        The cutoff frequency in inverse time steps.

    """
    order = ((window - 1) // 2 ) + 1
    nwts = 2 * order + 1
    w = np.zeros([nwts])
    n = nwts // 2
    w[n] = 2 * cutoff
    k = np.arange(1., n)
    sigma = np.sin(np.pi * k / n) * n / (np.pi * k)
    firstfactor = np.sin(2. * np.pi * cutoff * k) / (np.pi * k)
    w[n-1:0:-1] = firstfactor * sigma
    w[n+1:-1] = firstfactor * sigma
    return w[1:-1]
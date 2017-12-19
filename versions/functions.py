import numpy as np
import matplotlib.pyplot as plt


def gauss(x, *p):
    a, mu, sigma = p
    return a * np.exp((-(x-mu)**2)/(2.*sigma**2))



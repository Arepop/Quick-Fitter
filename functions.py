import numpy as np
import matplotlib.pyplot as plt

def gauss(x, *p):
    a, mu, sigma = p
    return a * np.exp((-(x-mu)**2)/(2.*sigma**2))

def map_an(x, in_min, in_max, out_min, out_max):
    return ((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

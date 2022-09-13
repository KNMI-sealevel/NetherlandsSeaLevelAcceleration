# local_functions.py

import numpy as np
import spectrum as sp

def mtm(y, dt, NW=2.5, k=4):
    '''Use multi-taper method from the Spectrum library
    NW is he time half bandwidth parameter
    k the number of Slepian sequences to use.
    Additional information on how to use the library:
    https://stackoverflow.com/questions/62836233/multi-taper-spectral-analysis-with-spectrum-in-python'''
    
    N = len(y)
    xf = np.linspace(0.0, 1.0/(2.0*dt), N//2)
    
    # The multitapered method
    [tapers, eigen] = sp.dpss(N, NW, k)
    Sk_complex, weights, eigenvalues=sp.pmtm(y, e=eigen, v=tapers, NFFT=N, show=False)

    Sk = abs(Sk_complex)**2
    Sk = np.mean(Sk * np.transpose(weights), axis=0) * dt
    
    yf_full = Sk
    yf = Sk[0:N//2]
    
    return xf, yf, yf_full
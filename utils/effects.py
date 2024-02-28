def wavelength_to_rgb(wavelength, gamma=0.8):

    # This converts a given wavelength of light to an
    # approximate RGB color value. The wavelength must be given
    # in nanometers in the range from 380 nm through 750 nm
    #
    # Based on code by Dan Bruton
    # http://www.physics.sfasu.edu/astro/color/spectra.html

    wavelength = float(wavelength)
    if wavelength < 380:
        r = 0.0
        g = 0.0
        b = 0.0

    elif wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        r = (((440 - wavelength) / (440 - 380)) * attenuation) ** gamma
        g = 0.0
        b = (1.0 * attenuation) ** gamma

    elif wavelength <= 490:
        r = 0.0
        g = ((wavelength - 440) / (490 - 440)) ** gamma
        b = 1.0

    elif wavelength <= 510:
        r = 0.0
        g = 1.0
        b = ((510 - wavelength) / (510 - 490)) ** gamma

    elif wavelength <= 580:
        r = ((wavelength - 510) / (580 - 510)) ** gamma
        g = 1.0
        b = 0.0

    elif wavelength <= 645:
        r = 1.0
        g = ((645 - wavelength) / (645 - 580)) ** gamma
        b = 0.0

    elif wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        r = (1.0 * attenuation) ** gamma
        g = 0.0
        b = 0.0
    else:
        r = 0.0
        g = 0.0
        b = 0.0

    r *= 255
    g *= 255
    b *= 255
    return int(r), int(g), int(b)

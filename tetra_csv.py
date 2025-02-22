import sys, time, csv, argparse
import numpy as np
from rtlsdr import RtlSdr

###################
### Frequencies ###
###################


# Open the RTL-SDR
sdr = RtlSdr()

# Set default values
####SET YOUR DESIRED FREQUENCIESRANGE HERE.
##############################################################################
start_freq = 380e6 # Startfreq. in Hz(!) e.g. 106.7 MHz = 106700000 or 1067e5#
end_freq = 385e6 # Endfreq. in Hz(!)                                         #
##############################################################################
blacklist_time = 60 # Time in seconds for blacklist-scan
sdr.sample_rate = 256e4  # Hz Most SDR-Sticks for well with 2,56 MHz (set as 2560000 or 256e4)
sdr.freq_correction = 1  # PPM e.g. -10 / 10
sdr.gain = 30  # dB (on't use auto/0
num_samples = 2**16
squelch_level = -30
blacklist_auto = True 
blacklist_manual = False # Manually blacklist frequencies?
blacklist_custom = [] # Array of frequencies for manual blacklist. e.g. [433.000, 433.500, ]
blacklist_center = True #Blacklist the center frequency to make sure it gets detected (lots of qrm on center)
################
#Variable check#
################

#Startfreq
if start_freq <= 0 or start_freq>= 3e9:
    print("start_freq is NOT valid. Please enter valid value in Hz...")
else:
    print("start_freq is valid.")

#Endfreq
if end_freq <= 0 or end_freq>= 3e9:
    print("end_freq is valid.")
else:
    print("end_freq is NOT valid. Please enter valid value in Hz...")
#Check for exceeded scope
if end_freq - start_freq>= sdr.sample_rate:
    freqrange = end_freq - start_freq
    print(f"Warning: Selected Range is to big for selected sample_rate of {sdr.sample_rate}Hz")
    print(f"The configured start_freq and end_freq resulted in a range of {freqrange}Hz.\n This exceeds the available bandwidth of {sdr.sample_rate}. The complete specified range wont be covered")
#Blacklist Array
blacklist = []

#Calculate Centerfrequency
sdr.center_freq = (start_freq + end_freq) / 2
formatted_center  = '{:.3f}'.format(sdr.center_freq / 1000000.0)
print(f"Calculated the centerfrequency of {formatted_center} MHz")

# Blacklist frequncies manually
if blacklist_manual == True:
        blacklist.append(blacklist_custom)

    

#Exclude the centerfrequencie since it tends to detect a lot of QRM/ there



# Run automatic blacklisting for n seconds (blacklist_time)
if blacklist_auto == True:
    print(f"Scanning for frequencies to be blacklisted. This will take {blacklist_time} seconds.")
    t_end = time.time() + blacklist_time
    while time.time() < t_end:

        # Read samples from the RTL-SDR device
        samples3 = sdr.read_samples(num_samples)

        # Calculate the frequency range of the samples
        freq_range3 = np.linspace(start_freq, end_freq, num_samples, endpoint=False)
        
        # Convert the samples to a power spectrum
        spectrum3 = np.abs(np.fft.fftshift(np.fft.fft(samples3)))
        
        # Find the peak frequency in the spectrum
        peak_index3 = np.argmax(spectrum3)
        peak_freq3 = freq_range3[peak_index3]

        # Convert peak frequency to MHz
        peak_freq_mhz3 = f"{peak_freq3 / 1e6:.3f}"

        for i in blacklist:
            print(f"Adding[{i} to blacklist]")
            if i != peak_freq_mhz3:
                blacklist.append(peak_freq_mhz3)
                print("Added frequency to blacklist")
    # Append Center frequencies to blacklist
    blacklist.append(formatted_center)
    print(f"The following frequencie(s) are blacklisted: {blacklist} (including manual and automatic and the center frequency)")
    print("Blacklist created successfully!")
    print("CTRL + C to stop")

    # Append Center frequencies to blacklist
if blacklist_center == True:
    blacklist.append(formatted_center)
# Open the CSV file to write
with open('signal_log.csv', mode='w') as csvfile:
    signal_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    signal_writer.writerow(['Frequency (MHz)', 'Timestamp'])

    # The main loop with exception handling
    try:
        while True:
            # Read samples from the RTL-SDR device
            samples = sdr.read_samples(num_samples)

            # Calculate the frequency range of the samples
            freq_range = np.linspace(start_freq, end_freq, num_samples, endpoint=False)

            # Convert the samples to a power spectrum
            spectrum = np.abs(np.fft.fftshift(np.fft.fft(samples)))

            # Find the peak frequency in the spectrum
            peak_index = np.argmax(spectrum)
            peak_freq = freq_range[peak_index]

            # Convert peak frequency to MHz
            peak_freq_mhz = f"{peak_freq / 1e6:.3f}"

            # Only print the peak frequency if it exceeds the squelch level and is not excluded
            if spectrum[peak_index] > squelch_level and peak_freq_mhz in blacklist:
                pass
            else:
                print(f"Peak frequency detected: {peak_freq_mhz}Mhz")
                # Write to CSV file
                timestamp = time.ctime()
                signal_writer.writerow([peak_freq_mhz, timestamp])
                print("Frequency logged to CSV file")
    except KeyboardInterrupt:
        sdr.close()
        print("Bye!")
    finally:
        # Close the RTL-SDR
        sdr.close()

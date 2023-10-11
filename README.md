# rtl-sdr-tetra-detector

This tool is based on the [rtl-sdr-peak-detector](https://github.com/nootedandrooted/rtl-sdr-close-call-monitor/)
These scripts use an RTL-SDR device to detect peak signals on the preconfigured spectrum for tetra uplink.
The scripts is also preconfigured to automatic blacklist RF to prevent continuous false positives. 
If you need this script for other areas and usecases of detecting, I highly recommend to use the original software, because it walks your trough the configuration. This tool uses hardcoded frequencies. 


### Disclaimer
- This tool enables the detection of devices that use the Tetra Uplink frequencies and is a P.O.C.
- Devices that transmit on these frequencies are most of the time radios and tracker of ERT, Firefighter and the Police in European Countries.
- I do not assume any liability for the use of this tool. You decide what you do with it. If you use it for wrongdoing, atleast don't get caught. :D




### Dependencies

This code requires the following dependencies to run:

    numpy
    rtlsdr
    requests

These dependencies can be installed by running:

`pip install -r requirements.txt`

or


### Usage
Connect an RTL-SDR device to your computer.
    Open a terminal and navigate to the directory containing the python script.
    Run `python3 tetra_csv.py`

### Configure (optional)

   The python scripts has multiple variable you can tweak. By default it will listen on the Tetra Uplink frequencies with everything preconfigured you need.
   Even tho everything is preconfigured, I highly recommend to tweak the settings, especially things like Squelch and Gain, depending on your setup and antenna.
   Please consider, that most SDR-Devices only support 2.56 MHz of bandwith. (2560000 Hz)

   `start_freq`: the frequency to start scanning from (in Hz). e.g. 380000000 or 380e6 (e6 for six zeros)
   `end_freq`: the frequency to stop scanning at (in Hz). e.g. 385000000 or 385e6 (e6 for six zeros)   
   `blacklist_time`: Time to scan for QRM(static signals) to ignore when detecting
   `sdr.sample_rate`: Most SDR work well with the preconfigured value. Choose between the default value of 2.56MHz or a custom value (in Hz).        
   `sdr.freq_correction`: Finetune your receiver-frequencie. Set value in PPM. (Most of the time not necessary)       
   `sdr.gain`: Preconfigured. Actual gain used is rounded to the nearest supported value (in dB).
   `squelch_level`: he threshold for the squelch level, e.g., the level below which a signal is considered to be noise.   
   `blacklist_auto`: Enabled by default. Autoscan upon starting for interference to exclude from detecting
   `blacklist_manual` Use an predefined Array of known Frequencies to ignore.
   `blacklist_custom` Array of frequencies for manual blacklist. e.g. [433.000, 433.500 ]
   `blacklist_center` Highly recommend! Only disable if you know what you are doing.

        
### More about RTL-SDR

https://www.rtl-sdr.com/about-rtl-sdr/

It is important to know the basic capabilities of an RTL-SDR before using this script since you'll have to set different parameters correctly in order to have this script work as intented. 

### Raspberry pi 4

Install rtl-sdr package:
`sudo apt install rtl-sdr`

Download rtl-sdr.rules file from the official repository:
`sudo wget -O /etc/udev/rules.d/rtl-sdr.rules https://raw.githubusercontent.com/osmocom/rtl-sdr/master/rtl-sdr.rules`

Reload udev rules by running the following command:
`sudo udevadm control --reload-rules`

Unplug and plug back in the RTL-SDR device.

Install the GStreamer library and its Python bindings:
`sudo apt-get install gstreamer1.0-plugins-good gstreamer1.0-tools python3-gi python3-gst-1.0`

Make sure that the GST_PLUGIN_PATH and LD_LIBRARY_PATH environment variables are set:
`export GST_PLUGIN_PATH=/usr/lib/gstreamer-1.0:/usr/lib/arm-linux-gnueabihf/gstreamer-1.0`
`export LD_LIBRARY_PATH=/usr/lib/gstreamer-1.0:/usr/lib/arm-linux-gnueabihf/gstreamer-1.0`

### Contributing

If you would like to contribute to this project, feel free to submit a pull request or open an issue.

### License

This code is licensed under the GNU General Public License v3.0. See the LICENSE file for details.

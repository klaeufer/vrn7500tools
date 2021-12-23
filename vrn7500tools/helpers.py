# RepeaterBook CHIRP csv format
#   "Name": "..."
#   "Duplex": "+"
#   "Offset": "5.00000"
#   "Tone": "Tone" # accept 
#   "rToneFreq": "100.0"
#   "cToneFreq": "100.0" # set only if same as rToneFreq or TSQL
#   "DtcsCode": "023"
#   "DtcsPolarity": "NN"
#   "Mode": "FM"
#   "TStep": "5"
#   "Comment": "Macclenny"

# VR-N7500 JSON format
# aprs = {
#     "n": "APRS",
#     "rf": "144.390",
#     "tf": "144.390",
#     "ts": 10000, # 10 kHz
#     "rs": 10000,
#     "s": 1, # scan enabled
#     "w": 0, # narrowband
#     "eb": 1, # emphasis/deemphasis off
#     "id": 1,
#     "p": -2 # -1 LOW, -2 MED, 0 HIGH
# }

import logging
import csv
import json

MAX_CHANNELS = 14 # VR-N7500/RT99 limitation

def is2m(freq):
    return 130 <= float(freq) <= 170

def is70cm(freq):
    return 420 <= float(freq) <= 450

natl_simplex = {
    "n": "146.52",
    "rf": "146.52",
    "tf": "146.52",
    "ts": 10000,
    "eb": 1,
    "id": 1,
    "p": -2
}

aprs = {
    "n": "APRS",
    "rf": "144.390",
    "tf": "144.390",
    "ts": 10000,
    "eb": 1,
    "id": 1,
    "p": -2
}

def chirp2ht(channel):
    n = channel['Name']
    mode = channel['Mode']

    if mode != 'FM' and mode != 'Auto':
        logging.warning(f'skipping {n}, unsupported mode {mode}')
        return None

    rf = channel['Frequency']

    if not is2m(rf) and not is70cm(rf):
        logging.warning(f'skipping {n}, unsupported band {rf}')
        return None

    result = {'n': n, 'rf': rf, 's': 1, 'eb': 1, 'id': 1, 'p': -2}

    try:
        offset = float(channel['Offset'])
        rfreq = float(rf)
        if channel['Duplex'] == '+':
            tfreq = rfreq + offset
        elif channel['Duplex'] == '-':
            tfreq = rfreq - offset
        else:
            tfreq = rfreq
        result['tf'] = str(round(tfreq, 5))
    except:
        pass

    try:
        tone = channel['Tone']
        if tone == 'Tone' or tone == 'TSQL':
            ts = int(float(channel['rToneFreq']) * 100)
            result['ts'] = ts
            if tone == 'TSQL':
                rs = int(float(channel['cToneFreq']) * 100)
                result['rs'] = rs
            else:
                result['rs'] = ts
    except:
        pass

    return result

def chirp2cg(csvfile, name, skip):
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    channelList = list(filter(lambda row: row, map(chirp2ht, reader)))[skip:]
    num_channels = len(channelList)
    if num_channels > MAX_CHANNELS:
        logging.warn(f'{num_channels} is too many, truncating to {MAX_CHANNELS}')
        channelList = channelList[0:MAX_CHANNELS]
    for i in range(num_channels, MAX_CHANNELS):
        channelList.append(None)
    channelList.append(natl_simplex)
    channelList.append(aprs)
    channelGroup = {'n': name, 'chs': channelList}
    print(json.dumps(channelGroup, indent=2))
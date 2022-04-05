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
#     "m": 1, # mute
#     "id": 1,
#     "p": -2 # -1 LOW, -2 MED, 0 HIGH
# }

import logging
import csv
import json

MAX_CHANNELS = 13 # + 52, APRS VA, and APRS - VR-N7500/RT99 limitation

def is2m(freq):
    return 130 <= float(freq) <= 170

def is70cm(freq):
    return 420 <= float(freq) <= 480

natl_simplex = {
    "n": "146.52",
    "rf": "146.52",
    "tf": "146.52",
    "ts": 10000,
    "s": 1,
    "id": 1,
    "p": -2
}

# APRS voice alert channel
# scan-enabled, unmuted on device but with receive tone
# see also http://www.aprs.org/VoiceAlert3.html
aprs_va = {
    "n": "APRS VA",
    "rf": "144.390",
    "tf": "144.390",
    "ts": 10000,
    "rs": 10000,
    "s": 1,
    "id": 1,
    "p": -2
}

# standard APRS channel - muted on device
aprs = {
    "n": "APRS",
    "rf": "144.390",
    "tf": "144.390",
    "ts": 10000,
    "eb": 1,
    "id": 1,
    "m": 1,
    "p": -2
}

def chirp2ht(channel):
    n = channel['Name']
    mode = channel['Mode']
    rf = channel['Frequency']

    result = {'n': n, 'rf': rf, 's': 1, 'id': 1, 'p': -2}

    if mode == 'FM' or mode == 'Auto':
        pass
    elif mode == 'NFM':
        result['w'] = 0
    else:
        logging.warning(f'skipping {n}, unsupported mode {mode}')
        return None

    if not is2m(rf) and not is70cm(rf):
        logging.warning(f'skipping {n}, unsupported band {rf}')
        return None

    try:
        offset = float(channel['Offset'])
        rfreq = float(rf)
        duplex = channel['Duplex']
        if duplex == '+':
            tfreq = rfreq + offset
        elif duplex == '-':
            tfreq = rfreq - offset
        elif duplex == 'off':
            result['td'] = 1
        else:
            tfreq = rfreq
        if tfreq:
            result['tf'] = str(round(tfreq, 5))
    except:
        pass

    try:
        tone = channel['Tone']
        if tone == 'Tone' or tone == 'TSQL':
            ts = int(float(channel['rToneFreq']) * 100)
            result['ts'] = ts
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
    # fill with null entries if slots left
    for i in range(num_channels, MAX_CHANNELS):
        channelList.append(None)
    # append default channels
    channelList.append(natl_simplex)
    channelList.append(aprs_va)
    channelList.append(aprs)
    channelGroup = {'n': name, 'chs': channelList}
    print(json.dumps(channelGroup, indent=2))

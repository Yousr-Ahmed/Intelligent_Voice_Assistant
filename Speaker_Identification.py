import pickle

import speaker_verification_toolkit.tools as svt


def add_known_voice(sound_file_path, name):
    try:
        with open("data.pkl", "rb") as f:
            voices = pickle.load(f)
    except:
        voices = {}
    data = svt.extract_mfcc_from_wav_file(sound_file_path)
    voices[name] = data
    with open("data.pkl", "wb") as f:
        pickle.dump(voices, f)
    return F"{name} added to Known voices"


def get_unknown_voice(sound_file_path):
    try:
        with open("data.pkl", "rb") as f:
            voices = pickle.load(f)
    except:
        voices = {}
    if len(voices) == 0:
        return F"UNKNOWN USER"
    data = svt.extract_mfcc_from_wav_file(sound_file_path)
    index = svt.find_nearest_voice_data(voices.values(), data)
    name = list(voices.keys())[index]
    return F"{name}"

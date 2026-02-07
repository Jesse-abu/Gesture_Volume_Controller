from pycaw.pycaw import AudioUtilities

def set_volume(value, v_max, v_min):
    if value >= v_max:
        return ValueError('Exceeds limit')
    elif value <= v_min:
        return ValueError('Too low') 
    devices = AudioUtilities.GetSpeakers()
    volume = devices.EndpointVolume

    v1 = volume.GetVolumeRange()[0]
    dist = (v_max - value)/(value - v_min)
    conv = (v1*dist)/(dist + 1)

    volume.SetMasterVolumeLevel(conv, None)
    print(f"Volume level set to: {volume.GetMasterVolumeLevel()}")

    return conv

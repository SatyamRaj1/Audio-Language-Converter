import numpy as np
import pywt
import soundfile
from tqdm import tqdm
from noiseProfiler import NoiseProfiler


def mad(arr):
    arr = np.ma.array(arr).compressed()
    med = np.median(arr)
    return np.median(np.abs(arr - med))




class AudioDeNoise:

    def __init__(self, inputFile):
        self.__inputFile = inputFile
        self.__noiseProfile = None

    def deNoise(self, outputFile):
        """
        outputFile : str
            de-noised file name

        """
        info = soundfile.info(self.__inputFile)  # getting info of the audio
        rate = info.samplerate

        with soundfile.SoundFile(outputFile, "w", samplerate=rate, channels=info.channels) as of:
            for block in tqdm(soundfile.blocks(self.__inputFile, int(rate * info.duration * 0.10))):
                coefficients = pywt.wavedec(block, 'db4', mode='per', level=2)

                #  getting variance of the input signal
                sigma = mad(coefficients[- 1])

                # VISU Shrink thresholding by applying the universal threshold proposed by Donoho and Johnstone
                thresh = sigma * np.sqrt(2 * np.log(len(block)))

                # thresholding using the noise threshold generated
                coefficients[1:] = (pywt.threshold(i, value=thresh, mode='soft') for i in coefficients[1:])

                # getting the clean signal as in original form and writing to the file
                clean = pywt.waverec(coefficients, 'db4', mode='per')
                of.write(clean)

def denoiseAudio(input_file):
    output_file = "./uploads/denoised.wav"
    DenoisingObject = AudioDeNoise(input_file)
    DenoisingObject.deNoise(output_file)
    return output_file
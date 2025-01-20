from transformers import AutoProcessor
import torch, torchaudio
# import PySoundFile
from playsound import playsound
import soundfile as sf
from IPython.display import Audio
from Denoise import denoiseAudio
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
model = torch.load("Model.pt", weights_only=False)




def ChangeAudioLanguage(source_lang = "eng", target_lang="hin"):

    print("Change Audio Function Started ......")
    # denoised_audio = denoiseAudio(input_audio)
    denoised_audio = denoiseAudio("./uploads/recording.wav")
    print("audio Denoised")
    audio_file, orig_freq = sf.read(denoised_audio)
    print("audio Read")
    print(orig_freq)
    new_freq = model.config.sampling_rate
    audio_tensor = torch.tensor(audio_file).unsqueeze(dim = 0)
    print("Converted To Tensor")
    audio_newFreq =  torchaudio.functional.resample(audio_tensor, orig_freq=orig_freq, new_freq=new_freq) # must be a 16 kH
    print("Frequency Changed")
    audio_inputs = processor(audios=audio_newFreq, return_tensors="pt", sampling_rate = new_freq)
    print("Tokenized")
    audio_array_from_audio = model.generate(**audio_inputs, tgt_lang=target_lang)[0].cpu().numpy().squeeze()
    print("Audio Generated")
    output_audio = audio_array_from_audio
    converted_audio = "./uploads/converted.wav"
    sf.write(converted_audio, audio_array_from_audio, new_freq)
    # print(output_audio, type(output_audio))
    return new_freq
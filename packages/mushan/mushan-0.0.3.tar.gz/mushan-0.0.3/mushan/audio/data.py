from p_tqdm import p_umap
from glob import glob
import os
from scipy.io.wavfile import read

def convto2205(ori_audio_path):
    file_name = os.path.basename(ori_audio_path)
    dir_name = os.path.dirname(ori_audio_path)
    input_name = dir_name + '/' + 'new' + file_name
    output_name = ori_audio_path
    os.rename(ori_audio_path, input_name)
    os.system("ffmpeg -i "+ input_name+ " -loglevel fatal -y -ac 1 -ar 22050"+" " + output_name)
    os.remove(input_name)
    

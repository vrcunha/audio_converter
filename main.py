import os
from pathlib import Path

video_types = ['.mp4', '.mkv', '.avi']
audio_types = ['.m4a', '.ogg', '.mp3', '.wav', '.aac']

def convert_one(finput, foutput, out_suffix):
    finput = Path(finput)
    foutput = Path(foutput)
    if not finput.exists():
        return 'file not found'
    if not foutput.exists():
        os.mkdir(foutput)
        print(f'A folder was created in the path {foutput}')
    if finput.is_dir():
        return 'path is dir not file'
    fpath = Path(os.path.relpath(os.getcwd(), finput)).parents[1]
    fpath = os.path.join(fpath, finput)
    fname = Path(fpath).stem
    output_file = f'{foutput}/{fname}{out_suffix}'
    comando = f'ffmpeg -i {fpath} {output_file}'
    os.system(comando)

finput = '/Users/victorcunha/Downloads/wetransfer/parte_1.aac'
foutput = '/Users/victorcunha/Downloads/output/'
convert_one(finput, foutput, out_suffix='.wav')

import glob
import os
import shutil
import ffmpeg
import string
import argparse
import re
from pathlib import Path
from datetime import datetime
from profiles import profiles, opts
from vars import paths
from natsort import natsorted

startTime = datetime.now()

parser = argparse.ArgumentParser()
parser.add_argument('ipth', nargs='?')
parser.add_argument('-p')
parser.add_argument('-s')

args = parser.parse_args()

ipth = args.ipth or paths["i"]
opth = paths["o"]
epth = paths["e"]
dpth = paths["d"]

formats = {".mkv", ".m4v", ".mp4", ".ts",
           ".mov", ".flv", ".wmv", ".avi", ".webm"}
formats = formats | {x.upper() for x in formats}
sformats = {".srt", ".vtt"}
sformats = sformats | {x.upper() for x in sformats}
valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

prof = profiles[args.p or "720"]
print(prof)
start = int(args.s or 0)


def handle_move(ipath, opath):
    if opts["delete"] == "soft":
        shutil.copy2(ipath, opath)
        outpath = str(ipath).replace(ipth, dpth)
        shutil.move(ipath, outpath, copy_function=shutil.copy2)
    else:
        shutil.move(ipath, opath, copy_function=shutil.copy2)


def handle_delete(pth, isdir=False):
    pth = os.path.normpath(pth)
    if opts["delete"] == "hard":
        d = os.path.dirname(pth)
        f = os.path.basename(pth)
        nf = f"DEL_{f}"
        nfp = os.path.join(d, nf)
        os.rename(pth, nfp)
        if isdir == True:
            shutil.rmtree(nfp)
        else:
            with open(nfp, 'w'):
                pass
            os.remove(nfp)
    elif opts["delete"] == "soft":
        if isdir == False:
            outpath = str(pth).replace(ipth, dpth)
            shutil.move(pth, outpath, copy_function=shutil.copy2)


def err_hdl(fil):
    try:
        w = ffmpeg.probe(fil, cmd='ffprobe')
        z = w['format']['bit_rate']
        print(fil, w, z)
    except Exception as e:
        outpath = str(fil).replace(ipth, epth)
        shutil.move(fil, outpath, copy_function=shutil.copy2)
        raise


def bitrate_dir(path):
    root_directory = Path(path)
    x = [(f.stat().st_size, f.resolve()) for f in root_directory.glob(
        '**/*') if f.is_file() and f.suffix in formats]
    y = max(x, key=lambda t: t[0])
    fil = y[1]
    w = ffmpeg.probe(fil, cmd='ffprobe')
    z = w['format']['bit_rate']
    return int(z)


def filesize_dir(path):
    root_directory = Path(path)
    total_size = max(
        f.stat().st_size for f in root_directory.glob('**/*') if f.is_file()
    )
    return total_size


def size_dir(path):
    root_directory = Path(path)
    total_size = sum(
        f.stat().st_size for f in root_directory.glob('**/*') if f.is_file()
    )
    return total_size


def list_dir(path):
    files = glob.glob(path + "/*/")
    k = lambda t: size_dir(t)
    r = True
    if opts["list_dir"] == "modified":
        k = lambda t: t.stat().st_mtime
    elif opts["list_dir"] == "bitrate":
        k = lambda t: bitrate_dir(t)
    elif opts["list_dir"] == "filesize":
        k = lambda t: filesize_dir(t)
    return sorted(files, key=k, reverse=r)


def list_files(path):
    files = [os.path.join(root, name) for root, subdirs,
             files in os.walk(path) for name in files]
    print(path)
    print(files)
    files = [*set(files)]
    return natsorted(files)


def sanitize(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tup = os.path.basename(path)
    s = "".join(x for x in tup if x in valid_chars)
    return os.path.join(os.path.dirname(path), s)


def hasStream(video, audio, subtitle):
    if not video:
        print("""
###  ##   ## ##            ### ###    ####   ### ##   ### ###   ## ##   
  ## ##  ##   ##            ##  ##     ##     ##  ##   ##  ##  ##   ##  
 # ## #  ##   ##            ##  ##     ##     ##  ##   ##      ##   ##  
 ## ##   ##   ##            ##  ##     ##     ##  ##   ## ##   ##   ##  
 ##  ##  ##   ##            ### ##     ##     ##  ##   ##      ##   ##  
 ##  ##  ##   ##             ###       ##     ##  ##   ##  ##  ##   ##  
###  ##   ## ##               ##      ####   ### ##   ### ###   ## ##""")

    if not audio:
        print("""
###  ##   ## ##              ##     ##  ###  ### ##     ####    ## ##   
  ## ##  ##   ##              ##    ##   ##   ##  ##     ##    ##   ##  
 # ## #  ##   ##            ## ##   ##   ##   ##  ##     ##    ##   ##  
 ## ##   ##   ##            ##  ##  ##   ##   ##  ##     ##    ##   ##  
 ##  ##  ##   ##            ## ###  ##   ##   ##  ##     ##    ##   ##  
 ##  ##  ##   ##            ##  ##  ##   ##   ##  ##     ##    ##   ##  
###  ##   ## ##            ###  ##   ## ##   ### ##     ####    ## ##""")

    if not subtitle:
        print("""
###  ##   ## ##             ## ##   ##  ###  ### ##   #### ##    ####   #### ##  ####     ### ###  
  ## ##  ##   ##           ##   ##  ##   ##   ##  ##  # ## ##     ##    # ## ##   ##       ##  ##  
 # ## #  ##   ##           ####     ##   ##   ##  ##    ##        ##      ##      ##       ##      
 ## ##   ##   ##            #####   ##   ##   ## ##     ##        ##      ##      ##       ## ##   
 ##  ##  ##   ##               ###  ##   ##   ##  ##    ##        ##      ##      ##       ##      
 ##  ##  ##   ##           ##   ##  ##   ##   ##  ##    ##        ##      ##      ##  ##   ##  ##  
###  ##   ## ##             ## ##    ## ##   ### ##    ####      ####    ####    ### ###  ### ###""")


def get_subs(input):
    sstream = None
    p = Path(input)
    enpattern = re.compile(r"(.*)en(.*)", re.IGNORECASE)
    pattern = re.compile(r"(.*)\.(srt|vtt)", re.IGNORECASE)
    subtitle_files = []
    subtitle_files.extend(p.parent.glob(f'{p.stem}*'))
    subtitles = sorted(
        (file for file in subtitle_files if pattern.search(file.name)),
        key=lambda x: x.name.lower()  # Sort by filename to ensure consistent selection
    )
    if(len(subtitles) == 1):
        english_subtitles = subtitles
    else:
        english_subtitles = sorted(
            (file for file in subtitles if enpattern.search(file.name)),
            key=lambda x: x.name.lower()  # Sort by filename to ensure consistent selection
        )
        if(len(english_subtitles) == 0):
            english_subtitles = subtitles
    try:
        print("XXXXXXXXXXXXXXXSUBTITLEXXXXXXXXXXXXXXX", english_subtitles)
        sstream = ffmpeg.input(str(english_subtitles[0]))
        return sstream
    except:
        return None


def get_streams(input):
    istream = ffmpeg.input(input, **prof["iparams"])
    sstream = get_subs(input)
    streams = ffmpeg.probe(input)["streams"]
    video, audio, subtitle, hindi = None, None, None, None
    videos = [f for f in streams if f["codec_type"] == 'video']
    audios = [f for f in streams if f["codec_type"] == 'audio']
    subtitles = [f for f in streams if f["codec_type"] == 'subtitle']
    for v in videos:
        if video is None:
            video = istream.video.filter(*prof["scale"])
    try:
        for i,v in enumerate(audios):
            if audio is None and v['tags'].get('language') == 'eng':
                audio = istream[f'a:{i}']
            if hindi is None and (v['tags'].get('language') == 'hin' or v['tags'].get('language') is None):
                hindi = istream[f'a:{i}']
            if audio is None:
                audio = istream[f'a:{i}']
    except:
        for i,v in enumerate(audios):
            if audio is None:
                audio = istream[f'a:{i}']
    try:
        for i,v in enumerate(subtitles):
            if subtitle is None and v['tags'].get('language') == 'eng' and v['disposition']['forced'] != 1:
                subtitle = istream[f's:{i}']
    except:
        for i,v in enumerate(subtitles):
            if subtitle is None:
                subtitle = istream[f's:{i}']
                
    if subtitle is None:
        subtitle = sstream

    hasStream(video, audio, subtitle)

    return list(filter(None,[video, audio, subtitle, hindi]))


def process_encode(input, output):
    try:
        streams = get_streams(input)
        stream = ffmpeg.output(
            *streams, output,
            **prof["params"]
        ).overwrite_output()
        ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
    except ffmpeg._run.Error as e:
        print(input, 'stdout:', e.stdout.decode('utf8'))
        z = e.stderr.decode('utf8')
        if z:
            print('stderr:', z)
            raise z


def encode_func(lst, lth):
    for count, val in enumerate(lst):
        print(f"{count} of {lth}")
        if os.path.isdir(val):
            continue
        if count < start:
            with open(val, 'w'):
                pass
            handle_delete(val)
            continue
        tup = os.path.splitext(val)
        if (tup[1] in formats):
            try:
                err_hdl(val)
            except:
                continue
            outpath = tup[0].replace(ipth, opth) + '.mp4'
            outpath = sanitize(outpath)
            startenc = datetime.now()
            process_encode(val, outpath)
            before = Path(val).stat().st_size
            after = Path(outpath).stat().st_size
            print(before, '=>' , after, '=>', before - after, '=>', after / before * 100, "%", datetime.now() - startenc)
            with open(val, 'w'):
                pass
            handle_delete(val)
            print(outpath)
        elif (tup[1] in sformats):
            continue
        else:
            outpath = val.replace(ipth, opth)
            outpath = sanitize(outpath)
            print(outpath)
            handle_move(val, outpath)
    for count, val in enumerate(lst):
        tup = os.path.splitext(val)
        if (tup[1] in sformats):
            handle_delete(val)


def encode_del(path):
    current_time = datetime.now().timestamp()
    os.utime(path, (current_time, current_time))
    lst = list_files(path)
    lth = len(lst)
    while lth > 0:
        encode_func(lst, lth)
        lst = list_files(path)
        lth = len(lst)
    handle_delete(path, True)


def process():
    dirs = list_dir(ipth)
    if (len(dirs) <= 0):
        print("FINISHED!!!!!")
        return
    workdir = dirs[0]
    encode_del(workdir)
    process()


process()
print(datetime.now() - startTime)

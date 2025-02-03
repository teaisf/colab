opts = {
    "list_dir": "sizedir",
    "delete": "hard"
}

params = {
    "preset": "veryfast", "crf": "27", "movflags": "faststart",
    "map_metadata":"-1", "strict": "-2","scodec": 'mov_text', "disposition:s:0": "forced", 
    "vcodec": "libx264", "video_track_timescale": "15360",
    "acodec": "libopus", "ac": "1", "ar": "48000", "b:a": "48k",
}

gparams = {
    "map_metadata":"-1", "strict": "-2", "gpu": '0', 'movflags': 'faststart',
    "vcodec": 'hevc_nvenc', "preset": 'p7', 'b_ref_mode:v': 1,
    "acodec": "libopus", "ac": "1", "ar": "48000", "b:a": "32k",
    "scodec": 'mov_text', "disposition:s:0": "forced", "tune":'hq',
    "cq:v": '36', "rc:v": "vbr", 'temporal-aq': 1, 'spatial-aq': 1
}

iparams = {
    "hwaccel": "nvdec", "hwaccel_output_format": "cuda", "extra_hw_frames": "8", "err_detect": "ignore_err",
    "analyzeduration": 2147483647, "probesize": 2147483647
}

sparams = {
    "map_metadata":"-1", "strict": "-2","scodec": 'copy', "disposition:s:0": "forced", 
    "vcodec": "copy", "acodec": "copy",
}

def resol(r):
    return {
        "b:v": f"{r}k", "maxrate": f"{r}k", "bufsize": f"{int(r/2)}k",
        "b:a": f"{round(r/10)}k"
    }

profiles = {
    "360": {
        "scale": ("scale", -2, 360),
        "params": {**params, **resol(360)},
        "iparams": {}
    },
    "480": {
        "scale": ("scale", -2, 480),
        "params": {**params, **resol(480)},
        "iparams": {}
    },
    "540": {
        "scale": ("scale", -2, 540),
        "params": {**params, **resol(540)},
        "iparams": {}
    },
    "720": {
        "scale": ("scale", -2, 720),
        "params": {**params, **resol(720)},
        "iparams": {}
    },
    "1080": {
        "scale": ("scale", -2, 1080),
        "params": {**params, **resol(1080)},
        "iparams": {}
    },
    "copy": {
        "scale": ("scale", -1, -1),
        "params": sparams,
        "iparams": {}
    },
    "g360": {
        "scale": ("scale_cuda", -2, 360),
        "params": {**gparams, **resol(360)},
        "iparams": iparams
    },
    "g480": {
        "scale": ("scale_cuda", -2, 480),
        "params": {**gparams, **resol(480)},
        "iparams": iparams
    },
    "g540": {
        "scale": ("scale_cuda", -2, 540),
        "params": {**gparams, **resol(540)},
        "iparams": iparams
    },
    "g720": {
        "scale": ("scale_cuda", -2, 720),
        "params": {**gparams, **resol(720)},
        "iparams": iparams
    },
    "g1080": {
        "scale": ("scale_cuda", -2, 1080),
        "params": {**gparams, **resol(1080)},
        "iparams": iparams
    }
}
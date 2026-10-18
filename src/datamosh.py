# funny datamosher function
# 1. conv clips 2 raw avi
# 2. get raw bitstreams
# 3. poke bitstreams with a screwdriver (delete iframes for duration in clip2)
# 4. concat the vid bits to final product and write bytes to the output file
import subprocess
import os
# from pathlib import Path
import tempfile
import shutil
import sys

# Below are previous attempts at making this project. They are kept to show that there is in fact a reason this file has a large amount of time on Hackatime.
# Due to the lack of documentation for creating effects like these there was a lot of trial and error (and asking chatgpt for ffmpeg commands)

# def doDatamosh(clip1_path, clip2_path, output_path, transition_frame=None, mosh_duration=30):
#     ostemplocation = tempfile.gettempdir()
#     tempdir = f"{ostemplocation}/magicjump/"

#     if not os.path.isdir(tempdir):
#         print(f"Making a temp file for this run at {tempdir}")
#         os.makedirs(tempdir, exist_ok=True)
#     elif os.path.isdir(tempdir):
#         print(f"Using tempdir at {tempdir}")

#     # first step, convert the clips to raw avi
#     clip1_avi = f"{tempdir}/clip1.avi"
#     clip2_avi = f"{tempdir}/clip2.avi"

#     for inp, out in [(clip1_path, clip1_avi), (clip2_path, clip2_avi)]:
#         subprocess.run([
#             'ffmpeg', '-i', inp, '-y',
#             '-c:v', 'mpeg4',
#             '-q:v', '2',
#             '-g', '30',  # i frames every 30 frames
#             '-bf', '2',  # 2 b frames between p frames
#             '-an',  # audio is for nerds, im lazy
#             out
#         ], check=True)
    
#     # second step, extract the raw bitstreams
#     clip1_raw = f"{tempdir}/clip1.mp4"
#     clip2_raw = f"{tempdir}/clip2.mp4"

#     for avi, raw in [(clip1_avi, clip1_raw), (clip2_avi, clip2_raw)]:
#         subprocess.run([
#             'ffmpeg', '-i', avi, '-y',
#             '-c:v', 'copy',
#             '-bsf:v', 'mpeg4_unpack_bframes',
#             '-f', 'mp4',
#             raw
#         ], check=True)


#     # step three, do datamoshing by poking the bitstreams with a screwdriver or whatever

#     mosh_path= f"{tempdir}/moshed.mp4"

#     with open(clip1_raw, 'rb') as f1, open(clip2_raw, 'rb') as f2:
#         clip1_data = bytearray(f1.read())
#         clip2_data = bytearray(f2.read())

#         # iframes for MPEG4
#         iframe_marker =b'\x00\x00\x01\xB0'

#         iframe_pos = clip2_data.find(iframe_marker) # find i-frame to target for the datamosh

#         if iframe_pos != -1:
#             next_iframe = clip2_data.find(iframe_marker, iframe_pos + 4) # find next i-grame
#             if next_iframe != -1:
#                 # remove rest of iframes in the rest of the mosh duration fram
#                 modified_clip2 = bytearray()
#                 pos = 0
#                 iframe_count = 0
#                 while pos < len(clip2_data):
#                     next_i = clip2_data.find(iframe_marker, pos)

#                     if next_i == -1:
#                         modified_clip2.extend(clip2_data[pos:])
#                         break
                    
#                     # a deleted i-frame a day keeps the gf away
#                     if 0 < iframe_count <= mosh_duration // 30:
#                         # i frame the photo (and then dont hang it, this removes them)
#                         modified_clip2.extend(clip2_data[pos:next_i])
#                         pos = next_i + len(iframe_marker)
#                     else:
#                         modified_clip2.extend(clip2_data[pos:next_i + len(iframe_marker)])
#                         pos = next_i + len(iframe_marker)

#                     iframe_count += 1
#                 clip2_data = modified_clip2
        
#         # concat teh cliops
#         moshed_data = clip1_data + clip2_data
#         with open(mosh_path, 'wb') as out:
#             print(f"Writing moshed vid to {mosh_path}")
#             out.write(moshed_data)

#     # reencode final output
#     subprocess.run([
#     'ffmpeg', '-i', mosh_path, '-y',
#     '-c:v', 'libx264',
#     '-preset', 'medium',
#     '-crf', '18',
#     output_path
#     ], check=True, capture_output=True)

#     # complete :D :p



# def doDatamosh(clip1, clip2, output):
#     tempdir = f"{tempfile.gettempdir()}/magicjump"
#     os.makedirs(tempdir, exist_ok=True)
#     c1 = f"{tempdir}/c1.avi"
#     c2 = f"{tempdir}/c2.avi"
#     c2_noi = f"{tempdir}/c2_noi.avi"
#     subprocess.run(['ffmpeg','-i',clip1,'-y','-c:v','mpeg4','-q:v','2','-g','9999','-bf','0','-an',c1],check=True)
#     subprocess.run([
#         'ffmpeg', '-i', clip2, '-y',
#         '-vf', "select='not(eq(pict_type\\,I))',setpts=N/FRAME_RATE/TB",
#         '-c:v', 'mpeg4', '-q:v', '2', '-g', '9999', '-bf', '0', '-an',
#         c2_noi
#     ], check=True)
#     txt = f"{tempdir}/list.txt"
#     with open(txt,'w') as f: f.write(f"file '{c1}'\nfile '{c2_noi}'\n")
#     subprocess.run(['ffmpeg','-f','concat','-safe','0','-i',txt,'-y','-c','copy',output],check=True)

# def doDatamosh(in_video, out_video='moshed.mp4', start_frame=0, end_frame = -1, fps=30, delta=0):
#     input_avi = 'dm_input.avi'
#     output_avi = 'dm_output.avi'

#     subprocess.run([
#         'ffmpeg','-loglevel','error','-y','-i',in_video,
#         '-crf','0','-pix_fmt','yuv420p','-bf','0','-b','10000k','-r',str(fps),input_avi
#     ],check=True)

#     with open(input_avi, 'rb') as f: data=f.read()
#     split_token = bytes.fromhex('30306463')
#     frames = data.split(split_token)
#     header = frames[0]
#     frames = frames[1:]
#     iframe = bytes.fromhex('0001B0')
#     pframe = bytes.fromhex('0001B6')

#     n_video_frames = len([x for x in frames if x[5:8]==iframe or x[5:8]==pframe])

#     if end_frame < 0: end_frame = n_video_frames

#     def write_frame(f, out): out.write(split_token+f)

#     with open(output_avi, 'wb') as out:
#         out.write(header)
        
#         if delta:
#             repeat_frames=[]; ri=0
#             for i, f in enumerate(frames):
#                 if (f[5:8]!=iframe and f[5:8]!=pframe) or not start_frame<=i<end_frame:
#                     write_frame(f, out); continue

#                 if len(repeat_frames)<delta and f[5:8]!=iframe:
#                     repeat_frames.append(f); write_frame(f,out)

#                 elif len(repeat_frames)==delta:
#                     write_frame(repeat_frames[ri],out)
#                     ri=(ri+1)%delta

#                 else:write_frame(f, out)

#         else:
#             for i, f in enumerate(frames):
#                 if i<start_frame or end_frame<i or f[5:8]==iframe: continue
                
#                 write_frame(f,out)

#     subprocess.run([
#         'ffmpeg','-loglevel','error','-y','-i',output_avi,
#         '-crf','18','-pix_fmt','yuv420p','-vcodec','libx264','-acodec','aac','-b','10000k','-r',str(fps),out_video
#     ],check=True)

#     os.remove(input_avi)
#     os.remove(output_avi)

# def doDatamosh(vid1, vid2, output='moshed.mp4', fps=30):
#     tempdir=f"{tempfile.gettempdir()}/magicjump"
#     os.makedirs(tempdir,exist_ok=True)
#     a=f"{tempdir}/a.avi"
#     b=f"{tempdir}/b.avi"
#     b_noi=f"{tempdir}/b_noi.avi"
#     merged=f"{tempdir}/merged.avi"

#     subprocess.run(['ffmpeg','-i',vid1,'-y','-c:v','mpeg4','-q:v','2','-g','9999','-bf','0','-an',a],check=True)

#     subprocess.run(['ffmpeg','-i',vid2,'-y','-c:v','mpeg4','-q:v','2','-g','9999','-bf','0','-an',b],check=True)

#     subprocess.run(['ffmpeg','-i',b,'-y','-vf',"select='not(eq(pict_type\\,I))',setpts=N/FRAME_RATE/TB",
#                     '-c:v','mpeg4','-q:v','2','-g','9999','-bf','0','-an',b_noi],check=True)

#     with open(f"{tempdir}/list.txt",'w') as f:
#         f.write(f"file '{a}'\nfile '{b_noi}'\n")

#     subprocess.run(['ffmpeg','-f','concat','-safe','0','-i',f"{tempdir}/list.txt",
#                     '-y','-c','copy',merged],check=True)

#     subprocess.run(['ffmpeg','-i',merged,'-y','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-r',str(fps),output],check=True)

#     shutil.rmtree(tempdir)

# def doDatamosh(clip1, clip2, output, mosh_duration=30, fps=30):
#     tempdir = os.path.join(tempfile.gettempdir(), "magicjump")
#     os.makedirs(tempdir, exist_ok=True)

#     c1 = os.path.join(tempdir, "c1.avi")
#     c2 = os.path.join(tempdir, "c2.avi")
#     c2_noi = os.path.join(tempdir, "c2_noi.avi")
#     moshed = os.path.join(tempdir, "moshed.mp4")

#     # 1 conc avi
#     subprocess.run(['ffmpeg', '-y', '-i', clip1, '-c:v', 'mpeg4', '-q:v', '2', '-g', '9999', '-bf', '0', '-an', c1], check=True)
#     subprocess.run(['ffmpeg', '-y', '-i', clip2, '-c:v', 'mpeg4', '-q:v', '2', '-g', '9999', '-bf', '0', '-an', c2], check=True)

#     # 2 remove i frames
#     subprocess.run([
#         'ffmpeg', '-y', '-i', c2,
#         '-vf', "select='not(eq(pict_type\\,I))',setpts=N/FRAME_RATE/TB",
#         '-c:v', 'mpeg4', '-q:v', '2', '-g', '9999', '-bf', '0', '-an',
#         c2_noi
#     ], check=True)

#     # 3 concat raw AVI bitstreams at binary level
#     with open(c1, 'rb') as f1, open(c2_noi, 'rb') as f2, open(moshed, 'wb') as out:
#         data1 = f1.read()
#         data2 = f2.read()
#         out.write(data1 + data2)

#     # 4 wraip in mp4 without reincode
#     final = output
#     subprocess.run([
#         'ffmpeg', '-y', '-i', moshed,
#         '-c:v', 'copy',
#         '-an',
#         final
#     ], check=True)

#     # clean up
#     for f in [c1, c2, c2_noi, moshed]:
#         os.remove(f)

# def doMelt(clip, output, extend_seconds=3, quality=5):
#     temp = "temp.avi"
#     subprocess.run([
#         "ffmpeg", "-y", "-i", clip, "-c:v", "mpeg4", "-q:v", str(quality),
#         "-g", "2500", "-bf", "0", temp
#     ], check=True)

#     with open(temp, 'rb') as f:
#         data = bytearray(f.read())

#     vop_marker = b'\x00\x00\x01\xb6'
#     last_vop = data.rfind(vop_marker)
#     if last_vop == -1:
#         raise RuntimeError("No vops were found")
    
#     tail = data[last_vop:]
#     fps = int(subprocess.check_output([
#         "ffprobe", "-v", "error", "-select_streams", "v:0",
#         "-show_entries", "stream=r_frame_rate",
#         "-of", "default=noprint_wrappers=1:nokey=1", clip
#     ]).decode().strip().split('/')[0])

#     repeat_count = max(1, int(fps * extend_seconds / 2))
#     melted = data + tail * repeat_count

#     os.remove(temp)

#     with open(output, 'wb') as f:
#         f.write(melted)

def get_ffmpeg():
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
        return os.path.join(base, 'ffmpeg.exe' if sys.platform == 'win32' else 'ffmpeg')
    return 'ffmpeg'

def get_ffprobe():
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
        return os.path.join(base, 'ffprobe.exe' if sys.platform == 'win32' else 'ffprobe')
    return 'ffprobe'

def doMelt(clip, output, extend_frames=40, quality=5):
    temp = "temp.avi"
    raw = "raw.m4v"
    
    subprocess.run([
        get_ffmpeg(), "-y", "-i", clip,
        "-c:v", "mpeg4", "-q:v", str(quality),
        "-g", "99999", "-bf", "0", temp
    ], check=True)
    
    subprocess.run([
        get_ffmpeg(), "-y", "-i", temp,
        "-an", "-c:v", "copy", "-f", "m4v", raw
    ], check=True)
    
    with open(raw, "rb") as f:
        data = f.read()
    
    split_marker = b"\x00\x00\x01"
    frames = []
    i = 0
    while True:
        start = data.find(split_marker, i)
        if start == -1:
            break
        next_pos = data.find(split_marker, start + 3)
        frames.append(data[start:next_pos if next_pos != -1 else len(data)])
        i = next_pos if next_pos != -1 else len(data)
    
    pframe_indices = [i for i, f in enumerate(frames) if len(f) > 3 and f[3:4] == b"\xb6"]
    
    if not pframe_indices:
        melt_frames = frames
    else:
        num_to_loop = min(extend_frames, len(pframe_indices))
        loop_indices = pframe_indices[-num_to_loop:]
        
        melt_frames = frames[:]
        for _ in range(8):
            for idx in loop_indices:
                melt_frames.append(frames[idx])
    
    with open(raw, "wb") as f:
        f.write(b"".join(melt_frames))
    
    subprocess.run([
        get_ffmpeg(), "-y", "-f", "m4v", "-i", raw,
        "-c:v", "copy", output
    ], check=True)
    
    os.remove(temp)
    os.remove(raw)

def doDatamosh(clip1, clip2, output, iframe_skip=1, quality=5):
    temp1 = "temp1.avi"
    temp2 = "temp2.avi"

    subprocess.run([
        get_ffmpeg(), "-y", "-i", clip1,
        "-c:v", "mpeg4", "-q:v", str(quality),
        "-g", "9999", "-bf", "0",
        "-force_key_frames", "0",
        temp1
    ], check=True)

    subprocess.run([
        get_ffmpeg(), "-y", "-i", clip2, "-c:v", "mpeg4", "-q:v", str(quality),
        "-g", "2500", "-bf", "0", temp2
    ], check=True)

    with open(temp1, "rb") as f1:
        data1 = bytearray(f1.read())
    with open(temp2, "rb") as f2:
        data2 = bytearray(f2.read())

    iframe_marker = b'\x00\x00\x01\xb6'
    positions = []
    pos = 0
    while True:
        pos = data2.find(iframe_marker, pos)
        if pos == -1:
            break
        positions.append(pos)
        pos += 1

    if len(positions) > iframe_skip:
        moshed = data1 + data2[positions[iframe_skip]:]
    elif positions:
        moshed = data1 + data2[positions[0]:]
    else:
        moshed = data1 + data2

    with open(output, "wb") as f:
        f.write(moshed)

    result = subprocess.run(
        [get_ffprobe(), "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", output],
        capture_output=True, text=True
    )
    t_max = float(result.stdout.strip())

    expr = f"expr:gte(t,{t_max - 0.2})"

    subprocess.run([
        get_ffmpeg(), "-y", "-i", output,
        "-c:v", "mpeg4", "-q:v", str(quality),
        "-g", "9999", "-bf", "0",
        "-force_key_frames", expr,
        output + ".temp.avi"
    ], check=True)

    os.replace(output + ".temp.avi", output)
    os.remove(temp1)
    os.remove(temp2)


# test the datamoshing function
# doDatamosh("before.mp4", "final.mp4", "moshed.mp4", iframe_skip=5)

# test the p-frame duplication function:

# doMelt("moshed.mp4", "melted.mp4", extend_frames=40)
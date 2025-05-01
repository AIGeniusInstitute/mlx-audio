# 1、读取文件夹下面的按照幻灯片顺序命名的图片、音频文件
# 2、合成视频（每张图片对应一个音频，在合成图片的视频帧的时候，考虑音频的时长，视频切换图片时间要匹配音频的时间轴）
# 3、保存视频 mp4

import os
import glob
import re

from moviepy import ImageClip, AudioFileClip
from moviepy.editor import *
from pydub import AudioSegment
import numpy as np


def natural_sort_key(s):
    """用于自然排序的辅助函数，确保文件按照1, 2, 10而不是1, 10, 2的顺序排序"""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]


def get_audio_duration(audio_path):
    """获取音频文件的时长（秒）"""
    try:
        # 使用moviepy获取音频时长
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        audio.close()
        return duration
    except:
        # 如果moviepy失败，尝试使用pydub
        try:
            audio = AudioSegment.from_file(audio_path)
            return len(audio) / 1000.0  # 毫秒转秒
        except:
            print(f"无法获取音频 {audio_path} 的时长，使用默认值5秒")
            return 5.0  # 默认时长


def create_video_from_images_and_audio(image_folder, audio_folder, output_path,
                                       image_extension='.png', audio_extension='.wav'):
    """
    从图片和音频创建视频

    参数:
    - image_folder: 包含图片的文件夹路径
    - audio_folder: 包含音频的文件夹路径
    - output_path: 输出视频的路径
    - image_extension: 图片文件扩展名
    - audio_extension: 音频文件扩展名
    """
    # 获取所有图片和音频文件
    image_files = glob.glob(os.path.join(image_folder, f'*{image_extension}'))
    audio_files = glob.glob(os.path.join(audio_folder, f'*{audio_extension}'))

    # 自然排序文件名
    image_files.sort(key=natural_sort_key)
    audio_files.sort(key=natural_sort_key)

    print(f"找到 {len(image_files)} 个图片文件和 {len(audio_files)} 个音频文件")

    if len(image_files) == 0 or len(audio_files) == 0:
        print("没有找到图片或音频文件")
        return

    # 确保图片和音频数量匹配
    if len(image_files) != len(audio_files):
        print(f"警告: 图片数量 ({len(image_files)}) 与音频数量 ({len(audio_files)}) 不匹配")
        # 使用较小的数量
        count = min(len(image_files), len(audio_files))
        image_files = image_files[:count]
        audio_files = audio_files[:count]

    # 创建视频片段列表
    clips = []
    audio_clips = []

    for i, (img_path, audio_path) in enumerate(zip(image_files, audio_files)):
        # 获取音频时长
        audio_duration = get_audio_duration(audio_path)
        print(f"处理第 {i + 1}/{len(image_files)} 组: 图片 {os.path.basename(img_path)}, "
              f"音频 {os.path.basename(audio_path)}, 时长 {audio_duration:.2f}秒")

        # 创建图片片段，时长与对应音频相同
        img_clip = ImageClip(img_path).set_duration(audio_duration)

        # 创建音频片段
        audio_clip = AudioFileClip(audio_path)

        # 为图片片段设置音频
        video_clip = img_clip.set_audio(audio_clip)

        clips.append(video_clip)
        audio_clips.append(audio_clip)

    # 连接所有视频片段
    final_clip = concatenate_videoclips(clips, method="compose")

    # 设置输出视频的分辨率（可选，这里使用第一张图片的分辨率）
    first_img = ImageClip(image_files[0])
    width, height = first_img.size
    first_img.close()

    final_clip = final_clip.resize((width, height))

    # 写入视频文件
    print(f"正在生成视频: {output_path}")
    final_clip.write_videofile(output_path, fps=24, codec='libx264',
                               audio_codec='aac', threads=4)

    # 清理资源
    final_clip.close()
    for clip in clips:
        clip.close()
    for audio in audio_clips:
        audio.close()

    print(f"视频已成功生成: {output_path}")


if __name__ == "__main__":
    # 用户可以修改这些路径
    image_folder = "/Users/bytedance/github/mlx-audio/ppt2video_image/AI学习指南从新手入门到进阶提升"  # 图片文件夹
    audio_folder = "/Users/bytedance/github/mlx-audio/ppt2video_image/AI学习指南从新手入门到进阶提升"  # 音频文件夹
    output_video = "/Users/bytedance/github/mlx-audio/ppt2video_video/AI学习指南从新手入门到进阶提升.mp4"  # 输出视频路径

    # 创建视频
    create_video_from_images_and_audio(image_folder, audio_folder, output_video)

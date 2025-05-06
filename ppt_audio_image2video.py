# 1、读取文件夹下面的按照幻灯片顺序命名的图片、音频文件
# 2、合成视频（每张图片对应一个音频，在合成图片的视频帧的时候，考虑音频的时长，视频切换图片时间要匹配音频的时间轴）
# 3、保存视频 mp4

import os
import re

from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from tqdm import tqdm


def natural_sort_key(s):
    """用于自然排序的键函数，确保文件按照1, 2, 10而不是1, 10, 2的顺序排序"""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]


def advanced_animation(clip, effect_type='ken_burns'):
    """
    使用OpenCV实现高级动画效果

    参数:
        clip: MoviePy视频剪辑对象
        effect_type: 效果类型，可选'ken_burns', 'rotate_zoom', 'pulse'
    """
    import cv2
    import numpy as np

    duration = clip.duration

    def effect(get_frame, t):
        frame = get_frame(t)
        h, w = frame.shape[:2]
        progress = t / duration  # 0到1之间的进度值

        if effect_type == 'ken_burns':
            # Ken Burns效果：平移+缩放
            zoom = 1 + 0.1 * progress
            x_offset = int(w * 0.1 * progress)
            y_offset = int(h * 0.1 * progress)

            matrix = np.float32([
                [zoom, 0, -x_offset],
                [0, zoom, -y_offset]
            ])

            frame = cv2.warpAffine(frame, matrix, (w, h))

        elif effect_type == 'rotate_zoom':
            # 旋转+缩放效果
            angle = 1 * progress  # 最大旋转1度
            zoom = 1 + 0.1 * progress

            center = (w / 2, h / 2)
            rot_matrix = cv2.getRotationMatrix2D(center, angle, zoom)
            frame = cv2.warpAffine(frame, rot_matrix, (w, h))

        elif effect_type == 'pulse':
            # 脉冲效果：周期性缩放
            zoom = 1 + 0.1 * np.sin(progress * np.pi * 4)

            matrix = np.float32([
                [zoom, 0, w / 2 * (1 - zoom)],
                [0, zoom, h / 2 * (1 - zoom)]
            ])

            frame = cv2.warpAffine(frame, matrix, (w, h))

        return frame

    try:
        return clip.transform(effect)  # 新版MoviePy
    except AttributeError:
        return clip.fl(effect)  # 兼容旧版MoviePy


def create_slideshow_video(image_folder, audio_folder, output_file, image_ext='.png', audio_ext='.wav'):
    """
    创建幻灯片视频

    参数:
        image_folder: 包含图片的文件夹路径
        audio_folder: 包含音频的文件夹路径
        output_file: 输出视频文件的路径
        image_ext: 图片文件扩展名
        audio_ext: 音频文件扩展名
    """

    # 确保扩展名格式正确（带点）
    if not image_ext.startswith('.'):
        image_ext = '.' + image_ext
    if not audio_ext.startswith('.'):
        audio_ext = '.' + audio_ext

    # 获取并排序图片和音频文件
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(image_ext)]
    audio_files = [f for f in os.listdir(audio_folder) if f.lower().endswith(audio_ext)]

    # 自然排序文件名
    image_files.sort(key=natural_sort_key)
    audio_files.sort(key=natural_sort_key)

    # 检查图片和音频文件数量是否匹配
    if len(image_files) != len(audio_files):
        print(f"警告: 图片数量({len(image_files)})与音频数量({len(audio_files)})不匹配")

    # 创建视频片段列表
    video_clips = []

    print("正在处理幻灯片和音频...")
    for i, (img_file, audio_file) in enumerate(
            tqdm(zip(image_files, audio_files), total=min(len(image_files), len(audio_files)))):
        # 加载图片
        img_path = os.path.join(image_folder, img_file)
        # 加载音频并获取其时长
        audio_path = os.path.join(audio_folder, audio_file)
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration

        # 创建图片视频片段，持续时间与音频相同
        img_clip = ImageClip(img_path).with_duration(duration)

        # 图片动画效果
        # 从 ['ken_burns','rotate_zoom','pulse'] 数组中随机选择一个动画效果
        effect_type = ['ken_burns', 'rotate_zoom', 'pulse'][i % 3]
        # 应用动画效果
        img_clip = advanced_animation(img_clip, effect_type=effect_type)

        # 添加音频到图片片段
        video_clip = img_clip.with_audio(audio_clip)
        video_clips.append(video_clip)

        print(f"处理第 {i + 1} 张幻灯片: {img_file} 与音频: {audio_file} (时长: {duration:.2f}秒)")

    # 连接所有视频片段
    print("正在合成最终视频...")
    final_clip = concatenate_videoclips(video_clips)

    # 设置输出视频的编解码器和比特率
    print(f"正在保存视频到: {output_file}")
    final_clip.write_videofile(
        output_file,
        fps=24,
        codec='libx264',
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True,
        threads=4
    )

    print("视频创建完成!")


if __name__ == "__main__":
    ppt_filename = 'AI大模型的本质'

    # 用户可以修改这些路径
    image_folder = f"/Users/bytedance/github/mlx-audio/ppt2video_image/{ppt_filename}"  # 图片文件夹
    audio_folder = f"/Users/bytedance/github/mlx-audio/ppt2video_image/{ppt_filename}"  # 音频文件夹
    output_video = f"/Users/bytedance/github/mlx-audio/ppt2video_video/{ppt_filename}.mp4"  # 输出视频路径

    # 创建视频
    create_slideshow_video(
        image_folder,
        audio_folder,
        output_video,
        '.png',
        '.wav'
    )

from ppt2images import ppt_to_images_pptx
from ppt2video_audio import text2audio
from ppt2video_text import read_images_text
from ppt_audio_image2video import create_slideshow_video


def ppt2video(ppt_filename):
    ppt_suffix = '.pptx'
    ppt_path = f'/Users/bytedance/github/mlx-audio/ppt2video_ppt/{ppt_filename}{ppt_suffix}'

    print(f"ppt_path: {ppt_path}")

    # 1.PPT转图片, 默认图片输出目录：ppt2video_image/{ppt_filename}
    ppt_to_images_pptx(ppt_path)

    # 2.图片转文本
    image_dir = f'/Users/bytedance/github/mlx-audio/ppt2video_image/{ppt_filename}'
    read_images_text(image_dir)

    # 3.文本转音频
    text_dir = image_dir
    text2audio(text_dir)

    # 4.合成视频
    image_folder = image_dir  # 图片文件夹
    audio_folder = image_dir  # 音频文件夹
    output_video = f'/Users/bytedance/github/mlx-audio/ppt2video_video/{ppt_filename}.mp4'  # 输出视频路径

    create_slideshow_video(
        image_folder,
        audio_folder,
        output_video,
        '.png',
        '.wav'
    )


if __name__ == '__main__':
    ppt_files = [
        '知识博客自媒体创业账号矩阵流量运营推广方案书',
        '程序员从大厂回归独立开发创业计划书',
        '技术博客创业计划书',
    ]

    for ppt_filename in ppt_files:
        ppt2video(ppt_filename)

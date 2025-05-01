import sys

from ppt2video_video import create_slideshow_video

from ppt2images import ppt_to_images_pptx
from ppt2video_audio import text2audio
from ppt2video_text import read_images_text


def ppt2video(ppt_filename):
    ppt_suffix = '.pptx'
    ppt_path = f'/Users/bytedance/github/mlx-audio/ppt2video_ppt/{ppt_filename}{ppt_suffix}'

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
    ppt_filename = ''
    # ppt_filename 从命令行参数获取
    # 参数校验
    if len(sys.argv) > 2:
        print("参数错误，请输入一个PPT文件名")
        sys.exit(1)

    args = sys.argv[1:]
    if len(args) > 0:
        ppt_filename = args[0]

    print(f"ppt_filename: {ppt_filename}")

    if ppt_filename == '':
        print("参数错误，请输入一个PPT文件名")
        sys.exit(1)

    ppt2video(ppt_filename)

from ppt2images import ppt_to_images_pptx
from ppt2video_text import read_images_text
from ppt2video_video import create_slideshow_video

if __name__ == '__main__':
    ppt_filename = 'AI大模型的本质'
    ppt_suffix = '.pptx'
    ppt_path = f'/Users/bytedance/github/mlx-audio/ppt2video_ppt/{ppt_filename}{ppt_suffix}'

    # 1.PPT转图片, 默认图片输出目录：ppt2video_image/{ppt_filename}
    ppt_to_images_pptx(ppt_path)

    # 2.图片转文本
    image_dir = f'/Users/bytedance/github/mlx-audio/ppt2video_image/{ppt_filename}'
    read_images_text(image_dir)

    # 4.文本转音频
    read_images_text(image_dir)

    # 4.创建视频
    image_folder = image_dir  # 图片文件夹
    audio_folder = image_dir  # 音频文件夹
    # 输出视频路径
    output_video = f'/Users/bytedance/github/mlx-audio/ppt2video_video/{ppt_filename}.mp4'

    create_slideshow_video(
        image_folder,
        audio_folder,
        output_video,
        '.png',
        '.wav'
    )

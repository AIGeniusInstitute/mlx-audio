# 1.读取 /Users/bytedance/github/mlx-audio/ppt2video_image/AI学习指南从新手入门到进阶提升 目录下的所有图片文件
# 2.提取图片中的文本内容知识点
# 3.将文本内容知识点写入 /Users/bytedance/github/mlx-audio/ppt2video_image/{图片文件名}.txt 文件中
import os

from image2text import read_image


def read_images_text(image_dir):
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    for image_file in image_files:
        image_path = os.path.join(image_dir, image_file)
        text = read_image(image_path)
        text_file = os.path.splitext(image_file)[0] + '.txt'
        text_path = os.path.join(image_dir, text_file)
        with open(text_path, 'w') as f:
            f.write(text)

        print(f"已处理图片 {image_file}，文本内容已写入 {text_file}")


if __name__ == "__main__":
    image_dir = '/Users/bytedance/github/mlx-audio/ppt2video_image/AI学习指南从新手入门到进阶提升'
    read_images_text(image_dir)

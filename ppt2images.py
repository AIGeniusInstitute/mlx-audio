import os
import subprocess
import tempfile

from pdf2image import convert_from_path

def ppt_to_images_pptx(ppt_path, output_dir=None, format="png", dpi=200):
    """
    通过PDF中转将PPTX文件的每一张幻灯片转换为图片

    参数:
        ppt_path (str): PPTX文件的路径
        output_dir (str, optional): 输出图片的目录，默认为ppt2video_image/{PPT文件名}
        format (str, optional): 输出图片的格式，默认为 png
        dpi (int, optional): 输出图片的DPI，默认为200

    返回:
        list: 生成的图片文件路径列表
    """
    # 检查文件是否为.pptx格式
    if not ppt_path.lower().endswith('.pptx'):
        raise ValueError("此方法仅支持.pptx格式文件")

    # 获取PPT文件名（不含扩展名）
    ppt_filename = os.path.splitext(os.path.basename(ppt_path))[0]

    # 如果未指定输出目录，则创建默认目录
    if output_dir is None:
        output_dir = os.path.join("ppt2video_image", ppt_filename)

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 创建临时目录用于存储PDF文件
    with tempfile.TemporaryDirectory() as temp_dir:
        # 临时PDF文件路径
        pdf_path = os.path.join(temp_dir, f"{ppt_filename}.pdf")

        # 使用LibreOffice或unoconv将PPTX转换为PDF
        try:
            # 尝试使用LibreOffice
            print("正在将PPTX转换为PDF...")
            subprocess.run(
                ["soffice", "--headless", "--convert-to", "pdf", "--outdir", temp_dir, ppt_path],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                # 尝试使用unoconv
                subprocess.run(
                    ["unoconv", "-f", "pdf", "-o", temp_dir, ppt_path],
                    check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
            except (subprocess.CalledProcessError, FileNotFoundError):
                raise RuntimeError("无法将PPTX转换为PDF。请安装LibreOffice或unoconv。")

        # 检查PDF文件是否生成
        if not os.path.exists(pdf_path):
            raise RuntimeError("PDF文件生成失败")

        # 使用pdf2image将PDF转换为图片
        print("正在将PDF转换为图片...")
        try:
            images = convert_from_path(pdf_path, dpi=dpi)
        except Exception as e:
            raise RuntimeError(f"PDF转图片失败: {e}")

        # 保存图片
        image_paths = []
        for i, img in enumerate(images, 1):
            output_path = os.path.join(output_dir, f"slide_{i:03d}.{format}")
            img.save(output_path, format=format.upper())
            image_paths.append(output_path)
            print(f"已处理第 {i}/{len(images)} 张幻灯片")

        return image_paths

if __name__ == "__main__":
    ppt_path = '/Users/bytedance/github/mlx-audio/ppt2video_ppt/AI学习指南从新手入门到进阶提升.pptx'
    ppt_to_images_pptx(ppt_path)

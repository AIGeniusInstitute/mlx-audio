# 1.读取 /Users/bytedance/github/mlx-audio/ppt2video_image/AI学习指南从新手入门到进阶提升 目录下的所有 txt 文件
# 2.遍历 txt 文本内容，调用 generate_audio() 生成音频文件
# 3.将音频文件写入 /Users/bytedance/github/mlx-audio/ppt2video_image/{txt文件名}.wav 文件中
import os

from mlx_audio.tts.generate import generate_audio


def gen_audio(text, audio_fname):
    # Example: Generate an audiobook chapter as mp3 audio
    generate_audio(
        text=text,
        model_path="prince-canuma/Kokoro-82M",
        # https://huggingface.co/prince-canuma/Kokoro-82M/tree/main/voices
        voice="zm_yunjian",
        speed=1,
        # Language Options
        # 🇺🇸 'a' - American English
        # 🇬🇧 'b' - British English
        # 🇯🇵 'j' - Japanese (requires pip install misaki[ja])
        # 🇨🇳 'z' - Mandarin Chinese (requires pip install misaki[zh])
        # lang_code="a",  # Kokoro: (a)f_heart, or comment out for auto
        lang_code="z",  # Kokoro: (a)f_heart, or comment out for auto
        file_prefix=audio_fname,
        audio_format="wav",
        sample_rate=24000,
        join_audio=True,
        verbose=True,  # Set to False to disable print messages
        temperature=0.7,
    )


def text2audio(text_dir):
    # 遍历 text_dir文件夹下面的 txt 文本，调用 gen_audio() 生成音频文件
    text_files = [f for f in os.listdir(text_dir) if f.endswith('.txt')]

    for text_file in text_files:
        text_path = os.path.join(text_dir, text_file)
        with open(text_path, 'r') as f:
            text = f.read()

        audio_file = os.path.splitext(text_file)[0]
        audio_path = os.path.join(text_dir, audio_file)

        gen_audio(text, audio_path)

        print(f"已处理文本 {text_file}，音频文件已写入 {audio_file}")


if __name__ == "__main__":
    text_dir = '/Users/bytedance/github/mlx-audio/ppt2video_image/AI大模型的本质'
    text2audio(text_dir)

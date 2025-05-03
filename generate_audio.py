from mlx_audio.tts.generate import generate_audio

if __name__ == '__main__':
    # Example: Generate an audiobook chapter as mp3 audio
    generate_audio(
        text=(
            "你好,我是陈光剑.中国程序员,AI天才研究院和光剑读书创始人,资深技术专家和架构师,AI大模型应用架构师和大数据架构师."
        ),
        model_path="prince-canuma/Kokoro-82M",
        # https://huggingface.co/prince-canuma/Kokoro-82M/tree/main/voices
        # voice="af_heart",
        # voice="zm_yunjian",
        # voice="zm_yunyang",
        voice="zm_yunxi",
        # voice="zm_yunxia",

        # model_path="OuteAI/Llama-OuteTTS-1.0-1B",
        # model_path="mlx-community/Llama-OuteTTS-1.0-1B-4bit",
        # voice="/Users/bytedance/github/mlx-audio/mlx_audio/tts/models/outetts/default_speaker.json",
        speed=1,
        # Language Options
        # 🇺🇸 'a' - American English
        # 🇬🇧 'b' - British English
        # 🇯🇵 'j' - Japanese (requires pip install misaki[ja])
        # 🇨🇳 'z' - Mandarin Chinese (requires pip install misaki[zh])
        # lang_code="a",  # Kokoro: (a)f_heart, or comment out for auto
        lang_code="z",  # Kokoro: (a)f_heart, or comment out for auto
        file_prefix="audiobook_chapter1",
        audio_format="wav",
        sample_rate=24000,
        join_audio=True,
        verbose=True,  # Set to False to disable print messages
        temperature=0.7,
    )

    print("Audiobook chapter successfully generated!")

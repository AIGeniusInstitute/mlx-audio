from mlx_audio.tts.generate import generate_audio


# Example: Generate an audiobook chapter as mp3 audio
generate_audio(
    text=(
        "你好,我是陈光剑.中国程序员,AI天才研究院和光剑读书创始人,资深技术专家和架构师,AI大模型应用架构师和大数据架构师."
        """
        儒、释（佛）、道三家思想：

释（佛家）：处理好人与心的关系，我们要战胜自己；
儒（儒家）：处理好人与人的关系，我们要团结好他人；
道（道家）：处理好人与自然的关系，我们应该顺势而为。

明人陆绍珩《醉古堂剑扫》自叙有云：
一愿识尽人间好人，
二愿读尽世间好书，
三愿看尽世间好山水。
或曰：静则安能，但身到处，莫放过耳。旨哉言乎！
余性懒，逢世一切炎热争逐之场，了不关情。
惟是高山流水，任意所如，遇翠丛紫莽，竹林芳径，偕二三知己，抱膝长啸，欣然忘归。
加以名姝凝盻，素月入怀，
轻讴缓板，远韵孤箫，
青山送黛，小鸟兴歌，
侪侣忘机，茗酒随设，
余心最欢，乐不可极。
若乃闭关却扫，图史杂陈，
古人相对，百城坐列，
几榻之余，绝不闻户外事。则又如桃源人，尚不识汉世，又安论魏晋哉？此其乐，更未易一二为俗人言也。

又云：宠辱不惊，看庭前花开花落；去留无意，望天上云卷云舒。

其实就是讲内心修炼到了一种心境平和，淡泊自然的境界。

技术人成长的悖论
在程序员界有一个悖论持续在困惑着很多技术人：

1、在写代码的人的困惑是一直写代码是不是会丧失竞争力，会不会被后面年轻的更能加班写代码的人汰换。典型代表就是工作5年左右的核心技术骨干，此时正处于编码正嗨但也开始着手规划下一个职业发展阶段的时候。

2、没在写代码的人困惑是我长时间不写代码（或者代码量较少）我的技术功底是不是在退化，我在市场上还会有竞争力吗，我的发展空间是不是被限制住了。典型代表就是带业务项目的架构师或者团队Team Leader，他们更多的精力是在业务需求理解和拆分，团队事务的管理上。

这种“内卷”现象非常严重，也是技术人在职业发展过程中必定会面临的困境。
        """
    ),
    model_path="prince-canuma/Kokoro-82M",
    # https://huggingface.co/prince-canuma/Kokoro-82M/tree/main/voices
    # voice="af_heart",
    voice="zm_yunjian",

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

import librosa
import numpy as np
import json
import os
from pathlib import Path
import soundfile as sf
from scipy.signal import medfilt
import argparse
from tqdm import tqdm
import speech_recognition as sr  # 替代 whisper


def generate_outetts_config(audio_path, text=None, output_path="my_voice.json"):
    """
    从语音样本生成OutetTS配置文件

    参数:
        audio_path: 语音样本文件路径
        text: 语音内容文本(如果为None则尝试自动识别)
        output_path: 输出的配置文件路径
    """
    print(f"正在处理音频文件: {audio_path}")

    # 加载音频
    y, sr_audio = librosa.load(audio_path, sr=None)

    # 如果没有提供文本，尝试识别
    if text is None:
        print("未提供文本，尝试自动识别...")
        try:
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                print(f"识别出的文本: {text}")
        except Exception as e:
            print(f"语音识别失败: {e}")
            text = "这是一段用于声音克隆的示例文本。"
            print(f"使用默认文本: {text}")

    # 标准化音频
    y_normalized = librosa.util.normalize(y)

    # 简单的能量分割
    print("使用能量分割来识别单词边界...")
    onset_frames = librosa.onset.onset_detect(y=y_normalized, sr=sr_audio)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr_audio)

    # 简单估计单词边界
    words = text.split()
    if len(onset_times) < len(words):
        print(f"警告: 检测到的边界({len(onset_times)})少于单词数({len(words)})")
        # 简单地平均分配时间
        total_duration = len(y_normalized) / sr_audio
        avg_word_duration = total_duration / len(words)
        words_with_timestamps = []
        for i, word in enumerate(words):
            start = i * avg_word_duration
            end = (i + 1) * avg_word_duration
            words_with_timestamps.append({
                "word": word,
                "start": start,
                "end": end
            })
    else:
        # 使用检测到的边界
        words_with_timestamps = []
        for i, word in enumerate(words):
            if i < len(onset_times) - 1:
                start = onset_times[i]
                end = onset_times[i + 1]
            else:
                start = onset_times[i] if i < len(onset_times) else 0
                end = len(y_normalized) / sr_audio
            words_with_timestamps.append({
                "word": word,
                "start": start,
                "end": end
            })

    # 提取全局特征
    # 1. 能量
    global_energy = int(np.mean(librosa.feature.rms(y=y_normalized)[0]) * 100)
    global_energy = min(30, max(5, global_energy))  # 限制在5-30范围内

    # 2. 频谱质心
    global_spectral_centroid = int(np.mean(librosa.feature.spectral_centroid(y=y_normalized, sr=sr_audio)[0]) / 100)
    global_spectral_centroid = min(40, max(10, global_spectral_centroid))  # 限制在10-40范围内

    # 3. 音高
    pitches, magnitudes = librosa.piptrack(y=y_normalized, sr=sr_audio)
    pitch_values = []
    for t in range(magnitudes.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0:  # 过滤掉零值
            pitch_values.append(pitch)

    if pitch_values:
        global_pitch = int(np.mean(pitch_values) / 10)
        global_pitch = min(45, max(15, global_pitch))  # 限制在15-45范围内
    else:
        global_pitch = 25  # 默认值

    # 处理每个单词
    words_data = []
    for word_info in tqdm(words_with_timestamps, desc="处理单词"):
        word = word_info["word"]
        start_time = word_info["start"]
        end_time = word_info["end"]

        # 提取单词音频
        start_sample = int(start_time * sr_audio)
        end_sample = int(end_time * sr_audio)
        if end_sample > len(y_normalized):
            end_sample = len(y_normalized)

        word_audio = y_normalized[start_sample:end_sample]
        if len(word_audio) == 0:
            continue

        # 计算持续时间
        duration = end_time - start_time

        # 提取单词特征
        # 1. 能量
        word_energy = int(np.mean(librosa.feature.rms(y=word_audio)[0]) * 100)
        word_energy = min(30, max(5, word_energy))

        # 2. 频谱质心
        word_spectral_centroid = int(np.mean(librosa.feature.spectral_centroid(y=word_audio, sr=sr_audio)[0]) / 100)
        word_spectral_centroid = min(40, max(10, word_spectral_centroid))

        # 3. 音高
        pitches, magnitudes = librosa.piptrack(y=word_audio, sr=sr_audio)
        pitch_values = []
        for t in range(magnitudes.shape[1]):
            if t < magnitudes.shape[1]:
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)

        if pitch_values:
            word_pitch = int(np.mean(pitch_values) / 10)
            word_pitch = min(45, max(15, word_pitch))
        else:
            word_pitch = global_pitch

        # 生成c1和c2系数
        # 这里使用MFCC系数的变换
        mfccs = librosa.feature.mfcc(y=word_audio, sr=sr_audio, n_mfcc=30)

        # 生成合适长度的c1和c2
        c1_length = min(15, max(9, int(duration * 75)))  # 根据持续时间调整长度
        c2_length = c1_length

        # 使用MFCC系数的变换生成c1和c2
        c1 = []
        c2 = []

        for i in range(c1_length):
            # 将MFCC值映射到1-1023范围
            if i < mfccs.shape[1]:
                c1_val = int(((mfccs[0, i % mfccs.shape[1]] + 20) / 40) * 1023) + 1
                c2_val = int(((mfccs[1, i % mfccs.shape[1]] + 20) / 40) * 1023) + 1
            else:
                # 如果MFCC系数不足，使用随机值
                c1_val = np.random.randint(1, 1024)
                c2_val = np.random.randint(1, 1024)

            # 确保在有效范围内
            c1_val = max(1, min(1023, c1_val))
            c2_val = max(1, min(1023, c2_val))

            c1.append(c1_val)
            c2.append(c2_val)

        # 创建单词数据
        word_data = {
            "word": word,
            "duration": round(duration, 2),
            "c1": c1,
            "c2": c2,
            "features": {
                "energy": word_energy,
                "spectral_centroid": word_spectral_centroid,
                "pitch": word_pitch
            }
        }

        words_data.append(word_data)

    # 创建最终配置
    speaker_config = {
        "text": text,
        "words": words_data,
        "global_features": {
            "energy": global_energy,
            "spectral_centroid": global_spectral_centroid,
            "pitch": global_pitch
        },
        "interface_version": 3
    }

    # 保存配置文件
    with open(output_path, "w") as f:
        json.dump(speaker_config, f, indent=2)

    print(f"配置文件已保存至: {output_path}")
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从语音样本生成OutetTS配置文件")
    parser.add_argument("--audio", required=True, help="语音样本文件路径")
    parser.add_argument("--text", help="语音内容文本(可选)")
    parser.add_argument("--output", default="my_voice.json", help="输出的配置文件路径")

    args = parser.parse_args()

    generate_outetts_config(args.audio, args.text, args.output)
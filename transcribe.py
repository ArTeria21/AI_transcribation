#!/home/artemka/Codding/Scripts/transcribation/venv/bin/python3

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import os
import sys
import subprocess
import whisper
import torch
import warnings

def extract_audio(video_path, audio_path):
    # Извлечение аудио из видео с помощью ffmpeg
    command = ['ffmpeg', '-i', video_path, '-vn', '-acodec', 'copy', audio_path]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def transcribe_audio(audio_path, device, language):
    # Загрузка модели на указанное устройство
    model = whisper.load_model("base", device=device)
    
    # Подавление предупреждений
    warnings.filterwarnings("ignore")
    
    # Распознавание речи с указанием языка
    print("Начало распознавания...")
    result = model.transcribe(audio_path, verbose=False, language=language)
    return result["text"]

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Использование: python transcribe.py <путь_к_mp3_или_mp4> [путь_к_выходному_файлу] [eng|rus]")
        sys.exit(1)
        
    input_path = sys.argv[1]
    output_path = None
    language_code = 'rus'  # Язык по умолчанию
    
    if len(sys.argv) == 3:
        if sys.argv[2] in ['eng', 'rus']:
            language_code = sys.argv[2]
        else:
            output_path = sys.argv[2]
    elif len(sys.argv) == 4:
        output_path = sys.argv[2]
        language_code = sys.argv[3]
        
    if language_code not in ['eng', 'rus']:
        print("Неподдерживаемый язык. Пожалуйста, выберите 'eng' или 'rus'.")
        sys.exit(1)
        
    # Отображение кодов языков на формат, понятный Whisper
    language_map = {'eng': 'en', 'rus': 'ru'}
    language = language_map[language_code]
    
    if not os.path.isfile(input_path):
        print(f"Файл {input_path} не существует.")
        sys.exit(1)
        
    _, ext = os.path.splitext(input_path)
    ext = ext.lower()
    
    # Определение доступности GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Используемое устройство: {device}")
    
    if ext in ['.mp3', '.m4a', '.wav']:
        # Прямая транскрипция
        text = transcribe_audio(input_path, device, language)
    elif ext == '.mp4':
        # Извлечение аудио из видео
        audio_path = 'temp_audio.m4a'
        print("Извлечение аудио из видео...")
        extract_audio(input_path, audio_path)
        
        text = transcribe_audio(audio_path, device, language)
        
        # Удаление временного аудиофайла
        os.remove(audio_path)
    else:
        print("Неподдерживаемый формат файла. Пожалуйста, предоставьте mp3, mp4 или wav файл.")
        sys.exit(1)
        
    if output_path:
        # Запись результата в файл
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"\nРезультат транскрипции сохранен в файл: {output_path}")
    else:
        # Вывод результата в терминал
        print("\nРаспознанный текст:")
        print(text)

if __name__ == '__main__':
    main()

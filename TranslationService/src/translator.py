import torch
import torchaudio
import languages
import numpy as np
from seamless_communication.models.inference import Translator
from io import BytesIO

TASK_NAMES = {
    "S2ST": "(Speech to Speech translation)",
    "S2TT": "(Speech to Text translation)",
    "T2ST": "(Text to Speech translation)",
    "T2TT": "(Text to Text translation)",
    "ASR": "(Automatic Speech Recognition)",
}

AUDIO_SAMPLE_RATE = 16000.0
MAX_INPUT_AUDIO_LENGTH = 60  # in seconds
DEFAULT_TARGET_LANGUAGE = "English"

# Initialize a Translator object with a multitask model, vocoder on the GPU.
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
translator = Translator(
    model_name_or_card="seamlessM4T_large",
    vocoder_name_or_card="vocoder_36langs", 
    device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu"),
    dtype=torch.float16 if "cuda" in device.type else torch.float32,)

def predict_S2ST(
        audio_input: bytes,
        source_language: str | None,
        target_language: str,) -> tuple[tuple[int, np.ndarray], str]:
    
    task_name = task_name.split()[0]
    source_language_code = languages.LANGUAGE_NAME_TO_CODE[source_language] if source_language else None
    target_language_code = languages.LANGUAGE_NAME_TO_CODE[target_language]

    # change result bytes stream to file-like object
    input_data = BytesIO(audio_input)

    input_array, orig_freqency = torchaudio.load(input_data)
    new_input_array = torchaudio.functional.resample(
        input_array, 
        orig_freq=orig_freqency, 
        new_freq=AUDIO_SAMPLE_RATE
    )
    max_length = int(MAX_INPUT_AUDIO_LENGTH * AUDIO_SAMPLE_RATE)
    if new_input_array.shape[1] > max_length:
        new_input_array = new_input_array[:, :max_length]
        print(
            f"Input audio is too long. Only the first {MAX_INPUT_AUDIO_LENGTH} seconds is used."
        )
    torchaudio.save("buffer_audio.wav", new_input_array, sample_rate=int(AUDIO_SAMPLE_RATE))
    
    text_out, wav_result, sample_rate = translator.predict(
        input=input_data,
        task_str="S2ST",
        tgt_lang=target_language_code,
        src_lang=source_language_code,
        ngram_filtering=True,
    )
    return (sample_rate, wav_result.cpu().detach().numpy()), text_out
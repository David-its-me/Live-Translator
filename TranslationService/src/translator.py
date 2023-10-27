import torch
import torchaudio
from seamless_communication.models.inference import Translator

"""
# Initialize a Translator object with a multitask model, vocoder on the GPU.
translator = Translator("seamlessM4T_large", "vocoder_36langs", torch.device("cuda:0"), torch.float16)


# S2ST
translated_text, wav, sr = translator.predict(<path_to_input_audio>, "s2st", <tgt_lang>)

wav, sr = translator.synthesize_speech(<speech_units>, <tgt_lang>)

# Save the translated audio generation.
torchaudio.save(
    <path_to_save_audio>,
    wav[0].cpu(),
    sample_rate=sr,
)
"""
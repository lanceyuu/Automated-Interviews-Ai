import os
import wave
import audioop

# Configuration
RECORDINGS_DIR = 'recordings'  # Directory containing .raw files
SAMPLE_RATE = 8000             # Hz
CHANNELS = 1                   # Mono
SAMPLE_WIDTH = 1               # bytes (for μ-law, it's 1 byte)

def convert_raw_to_wav(raw_path, wav_path):
    """
    Convert a G.711 μ-law encoded .raw file to a .wav file.

    Parameters:
    - raw_path: Path to the input .raw file.
    - wav_path: Path to the output .wav file.
    """
    try:
        with open(raw_path, 'rb') as raw_file:
            raw_data = raw_file.read()

        # Decode μ-law to linear PCM
        pcm_data = audioop.ulaw2lin(raw_data, 2)  # 2 bytes per sample for PCM16

        # Write PCM data to WAV file
        with wave.open(wav_path, 'wb') as wav_file:
            wav_file.setnchannels(CHANNELS)
            wav_file.setsampwidth(2)          # 2 bytes for PCM16
            wav_file.setframerate(SAMPLE_RATE)
            wav_file.writeframes(pcm_data)

        print(f"Converted: {raw_path} -> {wav_path}")
    except Exception as e:
        print(f"Failed to convert {raw_path}: {e}")

def main():
    """
    Convert all .raw files in the RECORDINGS_DIR to .wav format.
    """
    if not os.path.isdir(RECORDINGS_DIR):
        print(f"Directory '{RECORDINGS_DIR}' does not exist.")
        return

    # List all .raw files in the directory
    raw_files = [f for f in os.listdir(RECORDINGS_DIR) if f.lower().endswith('.raw')]

    if not raw_files:
        print(f"No .raw files found in '{RECORDINGS_DIR}'.")
        return

    print(f"Found {len(raw_files)} .raw file(s) in '{RECORDINGS_DIR}'. Starting conversion...")

    for raw_file in raw_files:
        raw_path = os.path.join(RECORDINGS_DIR, raw_file)
        wav_file = raw_file[:-4] + '.wav'  # Replace .raw with .wav
        wav_path = os.path.join(RECORDINGS_DIR, wav_file)

        convert_raw_to_wav(raw_path, wav_path)

    print("Conversion process completed.")

if __name__ == "__main__":
    main()


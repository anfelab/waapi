import os
import struct
 
def read_riff_chunks(file_path):
    """
    Reads RIFF chunks from a WAV file to extract all metadata.
    """
    try:
        with open(file_path, "rb") as f:
            riff_header = f.read(12)  # RIFF header
            if riff_header[:4] != b'RIFF' or riff_header[8:12] != b'WAVE':
                print("Error: Not a valid WAV file.")
                return
            print("--- RIFF Metadata ---")
            print(f"ChunkID: {riff_header[:4].decode('ascii')}")
            print(f"Format: {riff_header[8:12].decode('ascii')}")
            while True:
                chunk_header = f.read(8)
                if len(chunk_header) < 8:
                    break
 
                chunk_id = chunk_header[:4].decode('ascii')
                chunk_size = struct.unpack('<I', chunk_header[4:])[0]
                chunk_data = f.read(chunk_size)
 
                print(f"\nChunkID: {chunk_id}")
                print(f"ChunkSize: {chunk_size}")
                if chunk_id == 'fmt ':
                    audio_format, num_channels, sample_rate = struct.unpack('<HHI', chunk_data[:8])
                    print(f"Audio Format: {audio_format}")
                    print(f"Number of Channels: {num_channels}")
                    print(f"Sample Rate: {sample_rate}")
                elif chunk_id == 'data':
                    print("Audio Data (not displayed)")
                elif chunk_id == 'LIST':
                    print("LIST Metadata:")
                    print(chunk_data.decode('ascii', errors='ignore'))
                elif chunk_id == 'iXML':
                    print("iXML Metadata (Full):")
                    print(chunk_data.decode('utf-8', errors='ignore'))
                else:
                    print(f"Raw Data: {chunk_data[:100]}... (truncated)")
 
    except Exception as e:
        print(f"Error reading RIFF chunks: {e}")
 
def print_wav_metadata(file_path):
    """
    Extracts and prints all WAV metadata.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return
 
    try:
        print(f"Reading metadata from: {file_path}")
        read_riff_chunks(file_path)
 
    except Exception as e:
        print(f"Error reading WAV metadata: {e}")
 
if __name__ == "__main__":
    file_path = input("Enter the path to the WAV file: ")
    print_wav_metadata(file_path)
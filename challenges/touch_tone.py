import numpy as np
import wave
import requests
import json

# frequencies observed after spectrum analyzing the tone:   
#                                       1=1209Hz,   4=697Hz
#                                       2=1336Hz,   3=770Hz
#                                       3=1477Hz,   2=852Hz
#                                                   1=941Hz
def mapping(freq1_, freq2_):

    dif_maxfreq = np.inf
    freq1 = 0
    dif_minfreq = np.inf
    freq2 = 0

    for i in [1209, 1336, 1477]:
        if(abs(freq1_ - i) < dif_maxfreq):
            print("freq1, refFreq: " + str(freq1_) + ", " + str(i))
            dif_maxfreq = abs(freq1_ - i)
            freq1 = i

    for i in [697, 770, 852, 941]:
        if(abs(freq2_ - i) < dif_minfreq):
            dif_minfreq = abs(freq2_ - i)
            freq2 = i


    if(freq1 == 1209):
        if(freq2 == 941):
            char = '*'
        elif(freq2 == 852):
            char = '7'
        elif(freq2 == 770):
            char = '4'
        elif(freq2 == 697):
            char = '1'
    
    elif(freq1 == 1336):
        if(freq2 == 941):
            char = '0'
        elif(freq2 == 852):
            char = '8'
        elif(freq2 == 770):
            char = '5'
        elif(freq2 == 697):
            char = '2'

    elif(freq1 == 1477):
        if(freq2 == 941):
            char = '#'
        elif(freq2 == 852):
            char = '9'
        elif(freq2 == 770):
            char = '6'
        elif(freq2 == 697):
            char = '3'
    return(char)

    
# URL of the .wav file
url = "https://hackattic.com/challenges/touch_tone_dialing/problem?access_token=b93a5ed3374f1740"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    json_data = response.json()
    
    # Extract the wav_url from the JSON
    wav_url = json_data.get("wav_url")
    
    if wav_url:
        # Send a GET request to the wav_url to download the .wav file
        wav_response = requests.get(wav_url)
        
        if wav_response.status_code == 200:
            # Save the .wav file locally
            with open("touchtone.wav", "wb") as file:
                file.write(wav_response.content)
            print("Audio file downloaded successfully.")
        else:
            print(f"Failed to download the .wav file. Status code: {wav_response.status_code}")
    else:
        print("No 'wav_url' found in the JSON response.")
else:
    print(f"Failed to fetch JSON data. Status code: {response.status_code}")
output = ""

# Open the wave file
w = wave.open('touchtone.wav', 'rb')

# Get audio parameters
sample_rate = w.getframerate()
n_channels = w.getnchannels()
sample_width = w.getsampwidth()
total_frames = w.getnframes()

# Read all audio frames
frames = w.readframes(total_frames)

# Convert audio data to a NumPy array
# Assuming 16-bit PCM audio (2 bytes per sample)
audio_samples = np.frombuffer(frames, dtype=np.int16)

# If stereo, take only one channel (e.g., left channel)
if n_channels == 2:
    audio_samples = audio_samples[::2]

# Define frame size (e.g., 1024 samples per frame)
# AudioFIle contains 32 characters so frame size = total_frames/32
frame_size = int(np.floor(total_frames/32))

# Iterate through the audio in frames
for i in range(0, len(audio_samples), frame_size):
    # Extract a frame
    frame = audio_samples[i:i + frame_size]

    # Skip if the frame is too small
    if len(frame) < frame_size:
        continue

    # Compute the FFT
    fft_result = np.fft.fft(frame)
    magnitude_spectrum = np.abs(fft_result)

    # Compute the frequency bins
    frequencies = np.fft.fftfreq(len(frame), 1 / sample_rate)

    # Only consider positive frequencies (since FFT output is symmetric)
    positive_freq_indices = np.where(frequencies >= 0)
    frequencies = frequencies[positive_freq_indices]
    magnitude_spectrum = magnitude_spectrum[positive_freq_indices]

    # Find the top 2 frequencies with the highest magnitudes
    top_indices = np.argsort(magnitude_spectrum)[-2:]  # Indices of top 2 magnitudes
    top_frequencies = frequencies[top_indices]
    
    output = output + mapping(max(top_frequencies), min(top_frequencies))


# Close the wave file
w.close()

output_json = {
    "sequence": output
}

# URL to which the JSON data will be posted
post_url = "https://hackattic.com/challenges/touch_tone_dialing/solve?access_token=b93a5ed3374f1740"

# Convert the result data to JSON
json_data = json.dumps(output_json)

# Set the headers to indicate JSON content
headers = {"Content-Type": "application/json"}

# Send a POST request with the JSON data
response = requests.post(post_url, data=json_data, headers=headers)

# Check the response
if response.status_code == 200:
    print("Data posted successfully.")
    print("Response from server:", response.json())  # Print the server's response
else:
    print(f"Failed to post data. Status code: {response.status_code}")
    print("Response from server:", response.text)

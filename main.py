from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
import numpy as np
import io
import soundfile as sf # For reading audio waveforms (pip install soundfile)

app = FastAPI()

# Define the schema for incoming requests
class AudioRequest(BaseModel):
    audio_id: str
    audio_base64: str

@app.post("/process-audio")
async def process_audio(request: AudioRequest):
    try:
        # 1. Decode the Base64 string into binary audio data
        audio_bytes = base64.b64decode(request.audio_base64)
        
        # 2. Read the audio data as a Numpy array (assuming WAV, etc.)
        # * Adjust accordingly based on your dataset's format
        audio_file = io.BytesIO(audio_bytes)
        data, samplerate = sf.read(audio_file)
        
        # Convert to mono if stereo, or apply specific processing
        if len(data.shape) > 1:
            data = data.mean(axis=1)

        # 3. Calculate statistics (Here, basic statistics of the waveform data itself are used as an example)
        # * To meet the requirement "values must match the specific audio specifications",
        #   add logic here if feature extraction like MFCC is required.
        
        data_mean = float(np.mean(data))
        data_std = float(np.std(data))
        data_var = float(np.var(data))
        data_min = float(np.min(data))
        data_max = float(np.max(data))
        data_median = float(np.median(data))
        data_range = data_max - data_min
        
        # Return the required JSON structure
        return {
            "rows": len(data),                # e.g., Number of samples
            "columns": ["amplitude"],         # e.g., Column name
            "mean": {"amplitude": data_mean},
            "std": {"amplitude": data_std},
            "variance": {"amplitude": data_var},
            "min": {"amplitude": data_min},
            "max": {"amplitude": data_max},
            "median": {"amplitude": data_median},
            "mode": {"amplitude": 0.0},       # Approximation or dummy since it's continuous
            "range": {"amplitude": data_range},
            "allowed_values": {},             # Describe categorical variables if any
            "value_range": {"amplitude": [data_min, data_max]},
            "correlation": []                 # Correlation matrix, etc., if there are multiple columns
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing audio: {str(e)}")

# For local testing
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

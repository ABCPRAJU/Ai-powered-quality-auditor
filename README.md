# AI Quality Auditor

A comprehensive AI-powered quality auditing system for analyzing customer service interactions, evaluating compliance, and providing actionable insights for improvement.

## Overview

The AI Quality Auditor processes audio transcriptions of customer service calls, cleans and analyzes the dialogue, scores compliance, and presents results through an interactive dashboard. It evaluates interactions based on empathy, professionalism, and regulatory compliance.

## Features

- **Audio Transcription**: Converts MP3 audio files to text using OpenAI Whisper
- **Text Processing**: Cleans and preprocesses transcripts for analysis
- **Speaker Labeling**: Automatically formats dialogue with Agent and Customer labels using Groq AI
- **Compliance Scoring**: Evaluates call quality across multiple dimensions:
  - Empathy (1-100 scale)
  - Professionalism (1-100 scale)
  - Compliance Status (Pass/Warn/Fail)
  - Policy Violations
  - Improvement Suggestions
- **RAG Integration**: Retrieves and applies relevant compliance rules to evaluation
- **Interactive Dashboard**: Visualizes audit results with Streamlit

## Project Structure

```
Ai quality auditor/
├── backend/
│   ├── transcribe.py              # Audio transcription (Step 1)
│   ├── Transcript_Preprocessing.ipynb  # Text cleaning (Step 2)
│   ├── clean_transcript.py         # Speaker labeling (Step 3)
│   ├── upload_policies.py          # Policy upload to Pinecone
│   ├── rag_compliance.py           # RAG compliance checker
│   ├── scoring_engine.py           # Quality scoring (Step 4)
│   └── policy.txt                  # Compliance policies
├── frontend/
│   └── dashboard.py                # Interactive Streamlit dashboard
├── data/
│   ├── 1_raw_transcript.txt        # Raw transcription output
│   ├── 2_cleaned_transcript.txt    # Cleaned transcript
│   ├── 3_labeled_dialogue.txt      # Formatted dialogue
│   └── audit_results.csv           # Final audit scores and analysis
├── .env                            # Environment variables (not included)
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Installation

### Prerequisites

- Python 3.10+
- FFmpeg (for audio processing)
- Virtual environment manager

### Setup Steps

1. **Clone or extract the project**
   ```bash
   cd "d:\Ai quality auditor"
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1  # Windows PowerShell
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   ```

5. **Prepare sample audio**
   Place an MP3 file named `sample.mp3` in the project root directory.

## Usage

### Step-by-Step Execution

#### Step 1: Transcribe Audio
```bash
cd backend
python transcribe.py
```
- Input: `sample.mp3`
- Output: `../data/1_raw_transcript.txt`

#### Step 2: Clean Transcript
Run the Jupyter notebook or execute via Python:
```bash
jupyter notebook Transcript_Preprocessing.ipynb
# Or execute the preprocessing code
```
- Input: `../data/1_raw_transcript.txt`
- Output: `../data/2_cleaned_transcript.txt`

#### Step 3: Label Speakers
```bash
python clean_transcript.py
```
- Input: `../data/2_cleaned_transcript.txt`
- Output: `../data/3_labeled_dialogue.txt`

#### Step 4: Score Quality
```bash
python scoring_engine.py
```
- Input: `../data/3_labeled_dialogue.txt`
- Output: `../data/audit_results.csv`

#### Step 5: View Dashboard
```bash
cd..
streamlit run frontend/dashboard.py
```
- Opens interactive dashboard at: `http://localhost:8501`

### Pipeline Overview

```
Audio File (MP3)
    ↓
Transcribe (Whisper)
    ↓
1_raw_transcript.txt
    ↓
Clean & Preprocess
    ↓
2_cleaned_transcript.txt
    ↓
Label Speakers (Groq)
    ↓
3_labeled_dialogue.txt
    ↓
Score Quality (RAG + Groq)
    ↓
audit_results.csv
    ↓
Dashboard Visualization
```

## Output Files

### 1. Raw Transcript (`1_raw_transcript.txt`)
Contains the complete transcription from the audio file, preserving all spoken words including filler words and repetitions.

### 2. Cleaned Transcript (`2_cleaned_transcript.txt`)
Processed transcript with:
- Lowercase normalization
- Filler words removed (um, uh, hmm, ah, like)
- Whitespace normalized

### 3. Labeled Dialogue (`3_labeled_dialogue.txt`)
Formatted conversation with speaker labels:
```
Agent: [statement]
Customer: [response]
Agent: [statement]
...
```

### 4. Audit Results (`audit_results.csv`)
Detailed scoring for each dialogue chunk plus final summary:

| Column | Description |
|--------|-------------|
| Chunk | Dialogue segment number or 'FINAL' |
| empathy | Empathy score (0-100) |
| professionalism | Professionalism score (0-100) |
| compliance | Status (Pass/Warn/Fail) |
| reason | Explanation of assessment |
| violations | Identified policy violations |
| suggestions | Recommended improvements |

## Technologies Used

- **Audio Processing**: OpenAI Whisper
- **LLM**: Groq (llama-3.3-70b-versatile)
- **Vector Database**: Pinecone (optional)
- **Text Processing**: Pandas, Scikit-learn, Librosa
- **Web Framework**: Streamlit
- **Visualization**: Plotly, Streamlit

## API Keys Required

1. **Groq API Key** (Required)
   - Sign up at https://console.groq.com
   - Add to `.env`: `GROQ_API_KEY=your_key`

2. **Pinecone API Key** (Optional)
   - For full RAG compliance checking
   - Sign up at https://www.pinecone.io
   - Add to `.env`: `PINECONE_API_KEY=your_key`

## Troubleshooting

### "FFmpeg not found"
- Windows: Run `winget install ffmpeg --accept-source-agreements --accept-package-agreements`
- The script auto-downloads FFmpeg if not available

### "Module not found" errors
- Ensure virtual environment is activated
- Run: `pip install -r requirements.txt`

### Dashboard shows "audit_results.csv not found"
- Run `scoring_engine.py` first to generate the file
- Ensure you're in the project root directory when running the dashboard

### API Key errors
- Verify `.env` file exists in project root
- Check API keys are valid
- Ensure keys have proper permissions

## Configuration

### Whisper Model
In `transcribe.py`, change the model size:
```python
model = whisper.load_model("base")  # Options: tiny, base, small, medium, large
```

### Groq Model
In `clean_transcript.py` and `scoring_engine.py`:
```python
model="llama-3.3-70b-versatile"  # Can use other Groq models
```

### Chunk Size
In `scoring_engine.py`, adjust dialogue chunks:
```python
for i in range(0, len(lines), 5):  # Change 5 to desired chunk size
```

## Performance Metrics

The dashboard displays:
- **Average Empathy Score**: Overall empathy across all chunks
- **Average Professionalism Score**: Overall professionalism across all chunks
- **Compliance Status**: Pass/Warn/Fail determination
- **Trend Analysis**: Visual graphs of scores across dialogue chunks
- **Violation Summary**: Aggregated list of all policy violations
- **Recommendations**: Compiled improvement suggestions

## Example Audit Results

```
Final Empathy Score: 43.48 / 100
Final Professionalism Score: 64.78 / 100
Overall Compliance: FAIL

Key Violations:
- Inefficient communication
- Lack of clear introduction
- Excessive repetition
- Uncertain tone used by agent

Recommendations:
- Start with a clear and concise greeting
- Use concise language to avoid repetition
- Provide clear resolution or next steps
```

## Future Enhancements

- Multi-language support
- Custom policy rule creation UI
- Real-time call monitoring
- Agent performance tracking over time
- Automated feedback generation
- Integration with CRM systems

## License

[Add your license information here]

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review API documentation for Groq and Pinecone
3. Ensure all dependencies are properly installed

## Version History

- **v1.0** (February 2026): Initial release with full audit pipeline
  - Audio transcription
  - Text preprocessing
  - Speaker labeling
  - Quality scoring
  - Interactive dashboard

# Enhanced RAG System with Conformal Prediction 

A Retrieval-Augmented Generation (RAG) system enhanced with conformal prediction to improve answer reliability and reduce hallucinations.

## 🌟 Key Features

- **Conformal Prediction Integration**: Statistical approach to ensure reliable information retrieval
- **Calibrated Confidence Scoring**: Automated system to measure retrieval quality
- **Metadata Matching**: Semantic search across table and column metadata
- **Interactive Web Interface**: Built with Streamlit for easy interaction

## 🏗️ Project Structure

```
├── app/
│   ├── calibration/         # Conformal prediction implementation
│   ├── data_loader.py      # Data ingestion utilities
│   ├── metadata_vectorstore.py  # Vector storage for embeddings
│   ├── rag_pipeline.py     # Main RAG implementation
│   └── schema_inferencer.py # Database schema analysis
├── data/                    # Data storage
└── streamlit_app.py         # Web interface
```

## 🔧 How It Works

### 1. RAG Pipeline
- Loads data from CSV into SQLite
- Extracts and analyzes schema metadata
- Generates embeddings for semantic search
- Uses calibrated retrieval for accurate matches

### 2. Conformal Prediction Enhancement

Conformal prediction improves RAG reliability through:

a) **Calibration Phase**:
- Generates representative question set
- Records retrieval performance metrics
- Builds calibration dataset for scoring

b) **Prediction Phase**:
- Calculates confidence scores for retrieved chunks
- Applies statistical threshold based on desired error rate
- Filters out unreliable matches

c) **Benefits**:
- Quantifiable confidence in retrieved information
- Reduced hallucinations through strict filtering
- Adjustable error rate for different use cases

### 3. Confidence Scoring

The system uses cosine distance metrics to:
- Measure similarity between queries and chunks
- Apply calibrated thresholds
- Provide transparency in match quality

## 🚀 Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the web interface:
```bash
streamlit run streamlit_app.py
```

3. Configure the error rate:
- Lower values (e.g., 0.1) = More permissive matching
- Higher values (e.g., 0.9) = Stricter matching

## 📊 Example Usage

1. Load your CSV data
2. Ask questions through the web interface
3. View matched columns and confidence scores
4. Adjust error rate to balance precision vs. recall

## 🔍 Technical Details

### Conformal Prediction Process

1. **Calibration**:
   - Creates diverse question set
   - Records cosine distances for known good matches
   - Builds statistical model of match quality

2. **Retrieval**:
   - Calculates cosine distance for new matches
   - Compares against calibration distribution
   - Filters based on statistical confidence

3. **Threshold Calculation**:
   ```python
   threshold = np.percentile(calibration_scores, (1 - error_rate) * 100)
   ```

4. **Filtering**:
   - Keeps matches below distance threshold
   - Provides confidence metrics
   - Returns only statistically reliable results

## 🎯 Understanding Conformal Prediction

### Practical Example

Let's say we have a database about cars and someone asks: "What's the average price of electric vehicles?"

**Without Conformal Prediction:**
- RAG might retrieve any chunks mentioning "price" or "electric"
- Could include irrelevant information about gas prices or electric batteries
- Might lead to incorrect or hallucinated answers

**With Conformal Prediction:**
1. Calibration Data:
   ```python
   calibration_records = [
       {"question": "What's the price of Tesla Model 3?", "cosine_distance": 0.15},
       {"question": "How much does a Nissan Leaf cost?", "cosine_distance": 0.18},
       {"question": "Average EV price in 2023?", "cosine_distance": 0.12},
       # ... more similar questions about car prices
   ]
   ```

2. When the new question comes in:
   ```python
   # Calculate threshold (e.g., for 90% confidence)
   error_rate = 0.1  # 90% confidence
   threshold = np.percentile(calibration_scores, (1 - error_rate) * 100)
   # threshold might be 0.20
   ```

3. Retrieved chunks are only accepted if their cosine distance is below 0.20:
   ```python
   filtered_chunks = [
       ✅ {"content": "Average EV price in 2023: $45,000", "cosine_distance": 0.14},
       ✅ {"content": "Electric vehicle pricing data...", "cosine_distance": 0.19},
       ❌ {"content": "Electric battery technology...", "cosine_distance": 0.25},
       ❌ {"content": "Gas prices trending...", "cosine_distance": 0.35}
   ]
   ```
## 🔍 RAG UI Screenshot

This screenshot shows how the system highlights the most relevant match and provides confidence metrics based on conformal prediction.

![RAG UI Screenshot](assets/ui-screenshot.png)


### Benefits Illustrated

1. **Quality Control**: Only information that's statistically similar to known good matches is used
2. **Confidence Levels**: You can adjust the error rate:
   - 0.1 = 90% confidence (more permissive)
   - 0.05 = 95% confidence (more strict)
3. **Transparency**: Each match comes with a confidence score you can verify
4. **Reduced Hallucinations**: By filtering out uncertain matches, the LLM is less likely to make up information


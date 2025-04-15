from typing import List, Dict
import numpy as np

def conformal_filter(
    retrieved_chunks: Dict,
    calibration_records: List[Dict],
    error_rate: float = 0.1,
    verbose: bool = False
) -> List[Dict]:
    """
    Filter retrieved chunks using conformal prediction to ensure a specified error rate.
    
    Args:
        retrieved_chunks: Dictionary containing 'matches' list with chunks and their confidence scores
        calibration_records: List of calibration records with cosine distances
        error_rate: Desired error rate (between 0 and 1), default 0.1 (90% confidence)
        verbose: Whether to print debug information
    
    Returns:
        List of filtered chunks that meet the confidence threshold
    """
    if not calibration_records or not retrieved_chunks.get('matches'):
        return []

    # Get calibration scores
    calibration_scores = [record['cosine_distance'] for record in calibration_records]
    print(calibration_scores)
    # Calculate threshold based on desired error rate
    # We use (1 - error_rate) percentile as we want scores BELOW the threshold
    threshold = np.percentile(calibration_scores, (1 - error_rate) * 100)
    print(threshold)
    # Filter chunks based on threshold
    filtered_chunks = []
    for chunk in retrieved_chunks['matches']:
        if chunk['metadata']['type'] == 'column':  # Only consider column-level matches
            # Get chunk embedding and calculate cosine distance
            #cosine_distance = 1 - chunk['confidence']  # Convert confidence to distance
            print('distances',chunk['cosine_distance'])
            if chunk['cosine_distance'] <= threshold:
                filtered_chunks.append(chunk)
    
    if verbose:
        print(f"Conformal prediction threshold (cosine distance): {threshold:.4f}")
        print(f"Input chunks: {len(retrieved_chunks['matches'])}")
        print(f"Filtered chunks: {len(filtered_chunks)}")
        print(f"Target confidence level: {(1 - error_rate) * 100:.1f}%")
    
    
    return filtered_chunks

def do_conformal_rag(
    question: str,
    retrieved_chunks: Dict,
    calibration_records: List[Dict],
    error_rate: float = 0.1,
    verbose: bool = False
) -> Dict:
    """
    Perform RAG with conformal prediction filtering.
    
    Args:
        question: User question
        retrieved_chunks: Retrieved chunks from vector store
        calibration_records: Calibration records for conformal prediction
        error_rate: Desired error rate
        verbose: Whether to print debug information
    
    Returns:
        Dictionary containing filtered results and metadata
    """
    # Apply conformal filtering
    filtered_chunks = conformal_filter(
        retrieved_chunks=retrieved_chunks,
        calibration_records=calibration_records,
        error_rate=error_rate,
        verbose=verbose
    )
    
    # Calculate confidence metrics for filtered results
    if filtered_chunks:
        confidence_scores = [(1 - chunk['cosine_distance']) for chunk in filtered_chunks]
        avg_confidence = np.mean(confidence_scores)
        max_confidence = np.max(confidence_scores)
        min_confidence = np.min(confidence_scores)
    else:
        avg_confidence = max_confidence = min_confidence = 0.0
    
    if verbose:
        print("\n=== Final Results ===")
        print(f"Chunks retained: {len(filtered_chunks)}")
        print(f"Average confidence: {avg_confidence:.3f}")
        print(f"Confidence range: {min_confidence:.3f} - {max_confidence:.3f}")
        
        # Show column-level results
        if filtered_chunks:
            print("\nSelected Columns:")
            for chunk in filtered_chunks:
                print(f"- {chunk['metadata']['column_name']}: {1 - chunk['cosine_distance']:.3f} confidence")
    
    return {
        'matches': filtered_chunks,
        'confidence_summary': {
            'average_confidence': round(float(avg_confidence), 3),
            'max_confidence': round(float(max_confidence), 3),
            'min_confidence': round(float(min_confidence), 3),
            'sufficient_confidence': len(filtered_chunks) > 0,
            'num_chunks': len(filtered_chunks)
        },
        'error_rate': error_rate,
        'confidence_level': (1 - error_rate) * 100
    }

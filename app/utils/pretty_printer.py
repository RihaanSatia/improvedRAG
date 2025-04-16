import json
from typing import Dict, Any
from colorama import Fore, Style, init
import logging

# Initialize colorama for cross-platform color support
init()

def setup_logger():
    """Configure logger for terminal output"""
    logger = logging.getLogger('RAG_Assistant')
    logger.setLevel(logging.INFO)
    
    # Create console handler with custom formatting
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        f'{Fore.CYAN}%(asctime)s{Style.RESET_ALL} - %(message)s',
        datefmt='%H:%M:%S'
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

logger = setup_logger()

def format_match(match: Dict[str, Any]) -> str:
    """Format a single match entry"""
    return (
        f"\n{Fore.GREEN}Match Details:{Style.RESET_ALL}\n"
        f"  • Content: {match['content']}\n"
        f"  • Column: {match['metadata']['column_name']}\n"
        f"  • Table: {match['metadata']['table_name']}\n"
        f"  • Distance: {match['cosine_distance']:.3f}\n"
    )

def format_confidence_summary(summary: Dict[str, Any]) -> str:
    """Format confidence summary"""
    return (
        f"\n{Fore.YELLOW}Confidence Summary:{Style.RESET_ALL}\n"
        f"  • Average: {summary['average_confidence']:.3f}\n"
        f"  • Max: {summary['max_confidence']:.3f}\n"
        f"  • Min: {summary['min_confidence']:.3f}\n"
        f"  • Matches found: {summary['num_chunks']}\n"
        f"  • Sufficient confidence: {summary['sufficient_confidence']}\n"
    )

def log_rag_response(response: Dict[str, Any]):
    """Log RAG response details to terminal"""
    logger.info(
        f"\n{Fore.BLUE}=== RAG Response Details ==={Style.RESET_ALL}\n"
        f"Status: {response.get('status', 'N/A')}\n"
        f"Error Rate: {response.get('error_rate', 'N/A')}\n"
        f"Confidence Level: {response.get('confidence_level', 'N/A')}%"
    )
    
    # Log matches
    for match in response.get('matches', []):
        logger.info(format_match(match))
    
    # Log confidence summary
    if 'confidence_summary' in response:
        logger.info(format_confidence_summary(response['confidence_summary']))
    
    logger.info(f"\n{Fore.BLUE}{'=' * 25}{Style.RESET_ALL}\n")
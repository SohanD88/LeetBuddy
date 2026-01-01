from typing import Tuple
import re

def verify_proof_text(proof_text: str) -> Tuple[str, float]:
    """
    Verifies the proof of the completion by the user
    Returs a verdict and confidence score
    Verdict is pass or fail
    Confidence is a float between 0 and 1

    This is v1
    """

    text = proof_text.lower()
    success_indicators = ["accepted", "runtime", "submission accepted", "passed", "success"]
    failure_indicators = ["wrong answer", "time limit exceeded", "runtime error", "compilation error", "failed"]

    for indicator in success_indicators:
        if indicator in text:
            return "pass", 0.85
        
    for indicator in failure_indicators:
        if indicator in text:
            return "fail", 0.85
        
    return "fail", 0.4

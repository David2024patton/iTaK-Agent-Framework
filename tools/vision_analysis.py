"""
iTaK Vision Analysis Tool

Analyze images using local LLM with vision capabilities.
Part of Layer 2 (Recon) - multimodal understanding.

Based on vision_analysis.py from iTaK's this.md specification.
"""

import os
import base64
import json
from typing import Optional
from dataclasses import dataclass


@dataclass
class VisionResult:
    """Result from vision analysis."""
    success: bool
    analysis: str
    error: Optional[str] = None
    model: str = ""
    

def encode_image_base64(image_path: str) -> Optional[str]:
    """Encode an image file to base64 string."""
    if not os.path.exists(image_path):
        return None
    
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception:
        return None


def analyze_image(
    image_path: str,
    prompt: str = "Describe this image in technical detail.",
    model: str = None,
    base_url: str = None,
) -> VisionResult:
    """Analyze an image using a vision-capable LLM.
    
    Args:
        image_path: Path to the image file
        prompt: Analysis prompt
        model: Vision model to use (defaults to env var VISION_MODEL)
        base_url: LLM API base URL (defaults to env var LLM_BASE_URL)
        
    Returns:
        VisionResult with analysis or error
    """
    # Configuration with environment variable fallbacks
    base_url = base_url or os.getenv("LLM_BASE_URL", "http://127.0.0.1:11434/v1")
    model = model or os.getenv("VISION_MODEL", "llava")
    
    print(f"👁️ VISION: Analyzing {image_path} using {model}...")
    
    # Check file exists
    if not os.path.exists(image_path):
        return VisionResult(
            success=False,
            analysis="",
            error=f"Image file not found: {image_path}",
            model=model,
        )
    
    # Encode image
    b64_image = encode_image_base64(image_path)
    if not b64_image:
        return VisionResult(
            success=False,
            analysis="",
            error="Failed to encode image",
            model=model,
        )
    
    try:
        from openai import OpenAI
        
        client = OpenAI(base_url=base_url, api_key="not-needed")
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{b64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=500,
        )
        
        return VisionResult(
            success=True,
            analysis=response.choices[0].message.content,
            model=model,
        )
        
    except ImportError:
        return VisionResult(
            success=False,
            analysis="",
            error="OpenAI package not installed. Run: pip install openai",
            model=model,
        )
    except Exception as e:
        return VisionResult(
            success=False,
            analysis="",
            error=f"Vision API error: {str(e)}",
            model=model,
        )


def analyze_screenshot(
    image_path: str,
    focus: str = "UI",
) -> VisionResult:
    """Analyze a screenshot with focus on specific aspects.
    
    Args:
        image_path: Path to screenshot
        focus: What to focus on (UI, errors, data, layout)
        
    Returns:
        VisionResult with analysis
    """
    prompts = {
        "UI": "Analyze this UI screenshot. Describe the layout, components, and any usability issues.",
        "errors": "Look for any error messages, warnings, or issues in this screenshot. List them all.",
        "data": "Extract any visible data, text, numbers, or information from this screenshot.",
        "layout": "Describe the visual layout, spacing, alignment, and design of this interface.",
    }
    
    prompt = prompts.get(focus, prompts["UI"])
    return analyze_image(image_path, prompt)


def compare_images(
    image1_path: str,
    image2_path: str,
) -> VisionResult:
    """Compare two images and describe differences.
    
    Useful for visual verification - comparing expected vs actual.
    
    Args:
        image1_path: Path to first image
        image2_path: Path to second image
        
    Returns:
        VisionResult with comparison
    """
    # This would require a model that can handle multiple images
    # For now, we analyze each separately
    
    result1 = analyze_image(image1_path, "Describe this image in detail.")
    if not result1.success:
        return result1
    
    result2 = analyze_image(image2_path, "Describe this image in detail.")
    if not result2.success:
        return result2
    
    # Return combined analysis
    return VisionResult(
        success=True,
        analysis=f"Image 1: {result1.analysis}\n\nImage 2: {result2.analysis}",
        model=result1.model,
    )


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python vision_analysis.py <path_to_image> [prompt]")
        sys.exit(1)
    
    path = sys.argv[1]
    user_prompt = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Describe this image."
    
    result = analyze_image(path, user_prompt)
    print(json.dumps({
        "success": result.success,
        "analysis": result.analysis,
        "error": result.error,
        "model": result.model,
    }, indent=2))

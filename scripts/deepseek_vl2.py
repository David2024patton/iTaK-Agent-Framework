#!/usr/bin/env python3
"""
DeepSeek-VL2 Local Inference Script
Runs DeepSeek vision-language models directly from HuggingFace using transformers.
No GGUF conversion needed!

Usage:
    python deepseek_vl2.py --image path/to/image.jpg --prompt "Describe this image"
    python deepseek_vl2.py --image url --prompt "What do you see?"
    python deepseek_vl2.py --interactive  # Interactive mode
"""

import argparse
import sys
import os
from pathlib import Path

# Suppress warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def check_dependencies():
    """Check if required packages are installed."""
    missing = []
    try:
        import torch
    except ImportError:
        missing.append("torch")
    try:
        import transformers
    except ImportError:
        missing.append("transformers")
    try:
        from PIL import Image
    except ImportError:
        missing.append("pillow")
    try:
        import requests
    except ImportError:
        missing.append("requests")
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print(f"   Install with: pip install {' '.join(missing)}")
        sys.exit(1)

check_dependencies()

import torch
from transformers import AutoModelForCausalLM, AutoProcessor
from PIL import Image
import requests
from io import BytesIO

# Available DeepSeek-VL2 models
MODELS = {
    "tiny": "deepseek-ai/deepseek-vl2-tiny",
    "small": "deepseek-ai/deepseek-vl2-small", 
    "base": "deepseek-ai/deepseek-vl2",
}

class DeepSeekVL2:
    """DeepSeek-VL2 inference wrapper."""
    
    def __init__(self, model_size: str = "tiny", device: str = None):
        """
        Initialize DeepSeek-VL2 model.
        
        Args:
            model_size: One of 'tiny', 'small', 'base'
            device: 'cuda', 'cpu', or None for auto-detect
        """
        self.model_name = MODELS.get(model_size, MODELS["tiny"])
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.processor = None
        
        print(f"🔧 Device: {self.device}")
        if self.device == "cuda":
            print(f"   GPU: {torch.cuda.get_device_name(0)}")
            print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    
    def load(self):
        """Load the model and processor."""
        if self.model is not None:
            return  # Already loaded
            
        print(f"📥 Loading {self.model_name}...")
        print("   (First run will download ~3GB)")
        
        try:
            self.processor = AutoProcessor.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
            # Load with appropriate precision
            dtype = torch.float16 if self.device == "cuda" else torch.float32
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                trust_remote_code=True,
                torch_dtype=dtype,
                device_map="auto" if self.device == "cuda" else None,
                low_cpu_mem_usage=True
            )
            
            if self.device == "cpu":
                self.model = self.model.to(self.device)
            
            print("✅ Model loaded!")
            
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            raise
    
    def unload(self):
        """Unload model to free GPU memory."""
        if self.model is not None:
            del self.model
            del self.processor
            self.model = None
            self.processor = None
            
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            print("🗑️  Model unloaded, GPU memory freed")
    
    def load_image(self, image_path: str) -> Image.Image:
        """Load image from file path or URL."""
        if image_path.startswith(("http://", "https://")):
            response = requests.get(image_path, timeout=30)
            return Image.open(BytesIO(response.content)).convert("RGB")
        else:
            return Image.open(image_path).convert("RGB")
    
    def generate(
        self,
        image: str | Image.Image,
        prompt: str,
        max_new_tokens: int = 512,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate response for image + prompt.
        
        Args:
            image: Image path, URL, or PIL Image
            prompt: Text prompt/question about the image
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0 = deterministic)
            
        Returns:
            Generated text response
        """
        self.load()  # Ensure model is loaded
        
        # Load image if needed
        if isinstance(image, str):
            image = self.load_image(image)
        
        # Prepare conversation format
        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt}
                ]
            }
        ]
        
        # Process inputs
        inputs = self.processor(
            conversation,
            return_tensors="pt",
            padding=True
        ).to(self.device)
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature if temperature > 0 else None,
                do_sample=temperature > 0,
                pad_token_id=self.processor.tokenizer.pad_token_id,
            )
        
        # Decode response
        response = self.processor.decode(
            outputs[0][inputs["input_ids"].shape[1]:],
            skip_special_tokens=True
        )
        
        return response.strip()


def interactive_mode(model: DeepSeekVL2):
    """Run interactive chat mode."""
    print("\n" + "="*50)
    print("🖼️  DeepSeek-VL2 Interactive Mode")
    print("="*50)
    print("Commands:")
    print("  /image <path_or_url>  - Load an image")
    print("  /model <tiny|small|base> - Switch model")
    print("  /quit - Exit")
    print("="*50 + "\n")
    
    current_image = None
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["/quit", "/exit", "/q"]:
                print("👋 Goodbye!")
                break
            
            if user_input.startswith("/image "):
                image_path = user_input[7:].strip()
                try:
                    current_image = model.load_image(image_path)
                    print(f"✅ Image loaded: {image_path}")
                except Exception as e:
                    print(f"❌ Failed to load image: {e}")
                continue
            
            if user_input.startswith("/model "):
                size = user_input[7:].strip()
                if size in MODELS:
                    model.unload()
                    model.model_name = MODELS[size]
                    print(f"✅ Switched to {size} model")
                else:
                    print(f"❌ Unknown model size. Use: tiny, small, base")
                continue
            
            if current_image is None:
                print("⚠️  No image loaded. Use /image <path_or_url> first")
                continue
            
            # Generate response
            print("🤔 Thinking...")
            response = model.generate(current_image, user_input)
            print(f"\n🤖 DeepSeek: {response}\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Run DeepSeek-VL2 vision-language model locally",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python deepseek_vl2.py --image photo.jpg --prompt "Describe this image"
  python deepseek_vl2.py --image https://example.com/img.jpg --prompt "What's in this?"
  python deepseek_vl2.py --interactive
  python deepseek_vl2.py --model small --image photo.jpg --prompt "Analyze this"
        """
    )
    
    parser.add_argument(
        "--model", "-m",
        choices=["tiny", "small", "base"],
        default="tiny",
        help="Model size (default: tiny, ~3GB)"
    )
    parser.add_argument(
        "--image", "-i",
        help="Path or URL to image"
    )
    parser.add_argument(
        "--prompt", "-p",
        help="Prompt/question about the image"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=512,
        help="Maximum tokens to generate (default: 512)"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature (default: 0.7, use 0 for deterministic)"
    )
    parser.add_argument(
        "--keep-loaded",
        action="store_true",
        help="Keep model loaded after inference (for multiple queries)"
    )
    
    args = parser.parse_args()
    
    # Initialize model
    model = DeepSeekVL2(model_size=args.model)
    
    try:
        if args.interactive:
            interactive_mode(model)
        elif args.image and args.prompt:
            print(f"\n📷 Image: {args.image}")
            print(f"❓ Prompt: {args.prompt}\n")
            
            response = model.generate(
                args.image,
                args.prompt,
                max_new_tokens=args.max_tokens,
                temperature=args.temperature
            )
            
            print(f"🤖 Response:\n{response}")
            
            if not args.keep_loaded:
                model.unload()
        else:
            parser.print_help()
            print("\n⚠️  Either use --interactive or provide --image and --prompt")
    
    except KeyboardInterrupt:
        print("\n👋 Interrupted")
    finally:
        if not args.keep_loaded:
            model.unload()


if __name__ == "__main__":
    main()

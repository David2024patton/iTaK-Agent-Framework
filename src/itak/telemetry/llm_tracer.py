"""
iTaK LLM Tracer - Training Data Collection

Logs all LLM interactions for:
1. Runtime recall - agent searches past solutions
2. Training data - export logs for fine-tuning

Based on llm_tracer.py from iTaK's this.md specification.
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Optional, List, Literal
from dataclasses import dataclass, field, asdict
from pathlib import Path


@dataclass
class LLMInteraction:
    """A single LLM interaction (prompt/response pair)."""
    timestamp: str
    model: str
    prompt: str
    response: str
    system_prompt: str = ""
    tokens_in: int = 0
    tokens_out: int = 0
    duration_ms: float = 0
    metadata: dict = field(default_factory=dict)
    
    def __post_init__(self):
        # Generate unique ID
        content = f"{self.timestamp}{self.prompt}{self.response}"
        self.id = hashlib.md5(content.encode()).hexdigest()[:12]


class LLMTracer:
    """Trace and log all LLM interactions for training and recall."""
    
    def __init__(
        self,
        log_dir: str = None,
        enabled: bool = None,
    ):
        """Initialize the tracer.
        
        Args:
            log_dir: Directory for log files
            enabled: Whether tracing is enabled
        """
        self.log_dir = log_dir or os.getenv("ITAK_TRACE_DIR", "logs/traces")
        self.enabled = enabled if enabled is not None else os.getenv("TRACE_ENABLED", "true").lower() == "true"
        self.interactions: List[LLMInteraction] = []
        self._current_file = None
        
        if self.enabled:
            os.makedirs(self.log_dir, exist_ok=True)
            self._init_log_file()
    
    def _init_log_file(self) -> None:
        """Initialize a new log file for this session."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._current_file = Path(self.log_dir) / f"trace_{timestamp}.jsonl"
    
    def log(
        self,
        model: str,
        prompt: str,
        response: str,
        system_prompt: str = "",
        tokens_in: int = 0,
        tokens_out: int = 0,
        duration_ms: float = 0,
        metadata: dict = None,
    ) -> Optional[LLMInteraction]:
        """Log an LLM interaction.
        
        Args:
            model: Model name used
            prompt: User prompt
            response: LLM response
            system_prompt: System prompt if any
            tokens_in: Input tokens
            tokens_out: Output tokens
            duration_ms: Response time in ms
            metadata: Additional metadata
            
        Returns:
            The logged interaction or None if disabled
        """
        if not self.enabled:
            return None
        
        interaction = LLMInteraction(
            timestamp=datetime.now().isoformat(),
            model=model,
            prompt=prompt,
            response=response,
            system_prompt=system_prompt,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            duration_ms=duration_ms,
            metadata=metadata or {},
        )
        
        self.interactions.append(interaction)
        
        # Append to log file
        if self._current_file:
            with open(self._current_file, "a") as f:
                f.write(json.dumps(asdict(interaction)) + "\n")
        
        return interaction
    
    def get_stats(self) -> dict:
        """Get statistics about logged interactions."""
        if not self.interactions:
            return {"total": 0}
        
        return {
            "total": len(self.interactions),
            "models_used": list(set(i.model for i in self.interactions)),
            "total_tokens_in": sum(i.tokens_in for i in self.interactions),
            "total_tokens_out": sum(i.tokens_out for i in self.interactions),
            "avg_duration_ms": sum(i.duration_ms for i in self.interactions) / len(self.interactions),
            "log_file": str(self._current_file) if self._current_file else None,
        }
    
    def export(
        self,
        output_path: str,
        format: Literal["sharegpt", "alpaca", "jsonl"] = "sharegpt",
    ) -> int:
        """Export logs for fine-tuning.
        
        Args:
            output_path: Output file path
            format: Export format (sharegpt, alpaca, jsonl)
            
        Returns:
            Number of interactions exported
        """
        print(f"📤 Exporting {len(self.interactions)} interactions to {output_path} ({format} format)")
        
        # Load all log files
        all_interactions = list(self.interactions)
        
        for log_file in Path(self.log_dir).glob("trace_*.jsonl"):
            with open(log_file) as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        all_interactions.append(LLMInteraction(**data))
                    except:
                        pass
        
        # Deduplicate by ID
        seen_ids = set()
        unique = []
        for i in all_interactions:
            if i.id not in seen_ids:
                seen_ids.add(i.id)
                unique.append(i)
        
        # Export in requested format
        exported = []
        
        for interaction in unique:
            if format == "sharegpt":
                # ShareGPT format for most fine-tuning
                entry = {
                    "conversations": [
                        {"from": "human", "value": interaction.prompt},
                        {"from": "gpt", "value": interaction.response},
                    ]
                }
                if interaction.system_prompt:
                    entry["conversations"].insert(0, {
                        "from": "system", 
                        "value": interaction.system_prompt
                    })
                exported.append(entry)
                
            elif format == "alpaca":
                # Alpaca format
                entry = {
                    "instruction": interaction.prompt,
                    "input": "",
                    "output": interaction.response,
                }
                exported.append(entry)
                
            else:  # jsonl
                exported.append(asdict(interaction))
        
        # Write output
        with open(output_path, "w") as f:
            for entry in exported:
                f.write(json.dumps(entry) + "\n")
        
        print(f"✅ Exported {len(exported)} unique interactions")
        return len(exported)
    
    def search(self, query: str, limit: int = 5) -> List[LLMInteraction]:
        """Search past interactions for similar prompts.
        
        Simple keyword search - for production, use ChromaDB.
        
        Args:
            query: Search query
            limit: Max results
            
        Returns:
            List of matching interactions
        """
        query_lower = query.lower()
        matches = []
        
        for interaction in self.interactions:
            if query_lower in interaction.prompt.lower():
                matches.append(interaction)
        
        return matches[:limit]


# Global tracer instance
_tracer: Optional[LLMTracer] = None


def get_tracer() -> LLMTracer:
    """Get the global tracer instance."""
    global _tracer
    if _tracer is None:
        _tracer = LLMTracer()
    return _tracer


def log_interaction(**kwargs) -> Optional[LLMInteraction]:
    """Convenience function to log an interaction."""
    return get_tracer().log(**kwargs)


if __name__ == "__main__":
    import sys
    
    tracer = get_tracer()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python llm_tracer.py stats           # Show statistics")
        print("  python llm_tracer.py export FILE FMT # Export to file")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "stats":
        print(json.dumps(tracer.get_stats(), indent=2))
    
    elif cmd == "export":
        output = sys.argv[2] if len(sys.argv) > 2 else "training.jsonl"
        fmt = sys.argv[3] if len(sys.argv) > 3 else "sharegpt"
        tracer.export(output, fmt)

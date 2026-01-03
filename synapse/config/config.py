from dataclasses import dataclass

@dataclass
class SynapseConfig:
    OUTPUT_DIR: str = "data"
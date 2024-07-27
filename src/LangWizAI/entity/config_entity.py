from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EuroparlDataIngestionConfig:
    root_dir: Path
    source_URL: str
    unzip_dir: Path
    dataset_names: list

@dataclass(frozen=True)
class WMTChatDataIngestionConfig:
    root_dir: Path
    source_URL: str
    unzip_dir: Path
    dataset_names: list
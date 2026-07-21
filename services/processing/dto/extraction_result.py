from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class ExtractionResult:

    text : str
    page_count : int
    word_count : int
    character_count : int
    extracted_at: datetime = field(default_factory=datetime.utcnow)
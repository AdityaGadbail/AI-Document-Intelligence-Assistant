from dataclasses import dataclass
import datetime


dataclass(slots=True)
class ExtractionResult:

    text : str
    page_count : int
    word_count : int
    character_count : int
    extracted_at: datetime
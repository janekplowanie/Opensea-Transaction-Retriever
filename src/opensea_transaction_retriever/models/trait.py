from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Trait:
    trait_type: str
    value: str
    count: int
    rarity_score: float = 0.0

    @classmethod
    def from_api_response(cls, trait_type: str, value: str, count: int, total_supply: int) -> 'Trait':
        """Create Trait instance from OpenSea API response with calculated rarity score."""
        rarity_score = 1 / (count / total_supply) if count > 0 else 0
        return cls(
            trait_type=trait_type,
            value=value,
            count=count,
            rarity_score=rarity_score
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert trait to dictionary format."""
        return {
            "trait_type": self.trait_type,
            "value": self.value,
            "count": self.count,
            "rarity_score": self.rarity_score
        }

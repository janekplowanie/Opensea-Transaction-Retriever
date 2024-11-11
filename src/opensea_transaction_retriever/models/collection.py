from dataclasses import dataclass
from typing import Dict, List, Optional
from .trait import Trait

@dataclass
class Collection:
    slug: str
    name: str
    total_supply: int
    traits: Optional[Dict[str, List[Trait]]] = None
    
    @classmethod
    def from_api_response(cls, data: Dict) -> 'Collection':
        """Create Collection instance from OpenSea API response."""
        return cls(
            slug=data.get('slug'),
            name=data.get('name'),
            total_supply=data.get('total_supply', 0)
        )

    def add_traits(self, traits_data: Dict) -> None:
        """Add traits data to collection."""
        self.traits = {}
        for trait_type, values in traits_data.items():
            self.traits[trait_type] = [
                Trait.from_api_response(
                    trait_type=trait_type,
                    value=value,
                    count=count,
                    total_supply=self.total_supply
                )
                for value, count in values.items()
            ]

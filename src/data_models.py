from dataclasses import asdict, dataclass


@dataclass
class Product:
    name: str
    price: str
    description: str = None
    url: str = None
    image_url: str = None

    def to_dict(self):
        return asdict(self)

from dataclasses import dataclass
from enum import Enum
from typing import Literal, Optional

from dacite import Config

opt_str = Optional[str]
opt_int = Optional[int]


# add backward compability in Literal annotation on dacite
# see https://github.com/konradhalas/dacite/issues/109
class JikanMediaType(Enum):
    tv = "TV"
    ova = "OVA"
    movie = "Movie"
    special = "Special"
    ona = "ONA"
    music = "Music"

LiteralMediaType = Literal[
    JikanMediaType.tv,
    JikanMediaType.ova,
    JikanMediaType.movie,
    JikanMediaType.special,
    JikanMediaType.ona,
    JikanMediaType.music,
]

class JikanAnimeStatus(Enum):
    finished = "Finished Airing"
    airing = "Currently Airing"
    unaired = "Not yet aired"

LiteralAnimeStatus = Literal[
    JikanAnimeStatus.finished,
    JikanAnimeStatus.airing,
    JikanAnimeStatus.unaired,
]


@dataclass
class JikanTitle:
    """Title model"""
    type: str
    """Type of title"""
    title: str
    """Title name"""


@dataclass
class JikanAiredPropertyUnit:
    """Aired property model"""
    day: int
    """Day of release"""
    month: int
    """Month of release"""
    year: int
    """Year of release"""

@dataclass
class JikanAiredProperty:
    """Aired property model"""
    from_: JikanAiredPropertyUnit
    """Date of start"""
    to: JikanAiredPropertyUnit
    """Date of end"""
    string: str
    """Date as string"""

@dataclass
class JikanAired:
    """Aired model"""
    from_: str
    """Date of start"""
    to: str
    """Date of end"""
    prop: JikanAiredProperty
    """Aired property"""

@dataclass
class JikanBroadcast:
    """Broadcast model"""
    day: str
    """Day of release"""
    time: str
    """Time of release"""
    timezone: str
    """Timezone of release"""
    string: str
    """Broadcast as string"""

@dataclass
class JikanExternalUri:
    """External uri model"""
    name: str
    """Name of the service"""
    url: str
    """Url of the service"""

@dataclass
class JikanData:
    """Data model"""
    mal_id: int
    """Mal id"""
    url: str
    """Url"""
    titles: list[JikanTitle]
    """
    List of titles available in MAL.

    For default display title (romanized), check if title.type == "Default".
    """
    type: Optional[JikanMediaType]
    """Type of title"""
    source: opt_str
    """Source of title"""
    episodes: opt_int
    """Episodes of title"""
    status: Optional[JikanAnimeStatus]
    """Status of title"""
    airing: bool
    """Is title airing"""
    aired: JikanAired
    """Aired property"""
    duration: opt_str
    """Duration of title"""
    broadcast: JikanBroadcast
    """Broadcast detail"""
    external_links: list[JikanExternalUri]
    """External links of title"""
    year = opt_int


def transform_jikan_literal(value: str) -> LiteralMediaType | LiteralAnimeStatus:
    """Transform string to Literal"""
    # do check
    if value in LiteralMediaType.__args__:
        return LiteralMediaType(value)
    elif value in LiteralAnimeStatus.__args__:
        return LiteralAnimeStatus(value)
    else:
        raise ValueError(f"Unknown literal value: {value}")

DaciteJikanConfig = Config(
    check_types=False,
    type_hooks={
        LiteralMediaType: transform_jikan_literal,
        LiteralAnimeStatus: transform_jikan_literal,
    },
)

from dataclasses import dataclass
from enum import Enum
from typing import Literal, Optional

from dacite import Config

opt_str = Optional[str]

# add backward compability in Literal annotation on dacite
# see https://github.com/konradhalas/dacite/issues/109
class SimklMediaType(Enum):
    """Media type"""
    anime = "anime"
    show = "show"
    movie = "movie"

LiteralMediaType = Literal[
    SimklMediaType.anime,
    SimklMediaType.show,
    SimklMediaType.movie,
]

@dataclass
class SimklMaps:
    """Maps of ids to other services"""
    simkl: int
    """Simkl id"""
    slug: opt_str
    """Slug of the entry"""
    anidb: opt_str
    """AniDB id"""
    mal: opt_str
    """MyAnimeList id"""
    tvdb: opt_str
    """TVDB id"""
    imdb: opt_str
    """IMDB id"""
    tmdb: opt_str
    """TMDB id"""
    kitsu: opt_str
    """Kitsu id"""
    anilist: opt_str
    """AniList id"""

@dataclass
class SimklEntry:
    """Entry in Simkl"""
    title: str
    """Title of the entry"""
    year: Optional[int]
    """Year of release"""
    type: Optional[LiteralMediaType]
    """Media type"""
    en_title: opt_str
    """English title"""
    ids: Optional[SimklMaps]
    """Maps of ids to other services"""


def transform_simkl_literal(value: str) -> LiteralMediaType:
    """Transform string to LiteralMediaType"""
    if value in LiteralMediaType.__args__:
        return LiteralMediaType(value)
    else:
        raise ValueError(f"Invalid value for LiteralMediaType: {value}")


DaciteSimklConfig = Config(
    type_hooks={
        LiteralMediaType: transform_simkl_literal,
    },
    check_types=False,
)

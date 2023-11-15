# BetterAnimeTraktMapper (BATM)

Better implementation to map MAL/AniDB &lt;-> Trakt and TMDB, alternative to
[ryuuganime/aniTrakt-IndexParser][atip]

## Why?

[AniTrakt][at] has decent public database to map MAL with Trakt but in their publicly accessible
database missed a lot of information regarding of episode offset, or even non-Japanese media.
Then there's also [anime-lists][als] that has been used widely by media server (Jellyfin/Emby,
Plex, etc) plugins is capable enough to use it as base to scrobble and shouldn't be an issue...
until the entry in Trakt has been migrated to TMDB, which has its own unique challange.
*also did I mention [anime-lists][als] is actually quite hard to use due to XML nature?*

So BATM tries to solve this problem while keeping it simple to use and easily understandable.

## How it works

1. BATM will ask user to provide title to lookup. Then based on the data:
   * BATM will fetch data from [ATIP][atip] for latest exisiting mapping from [AniTrakt][at]
   * If none, BATM will check on [SIMKL] if there's existing relationship to Trakt.
   * If not exist at all, BATM will ask user to manually link/map entry to Trakt.
2. BATM will check if episode on the season matches with MAL episode schema.
   * If not, BATM will ask user to manually select correct episode range.
   * If the season has less episodes than MAL counterpart, it will prompt user to add additional
     season to the array, and do episode range correction.
   * Else, user will be asked to add episode offset.
3. BATM will populate additional IDs from AniDB, AniList, IMDb, Kitsu, SIMKL, TMDB, and TVDB for
   better integration with 3rd party applications, but wont add additional episode correction to
   each platforms.
   * This will be solved by my future project in [Ryuuganime][ryuu] to fix all this mess once
     BATM finished, and [animeApi](https://animeapi.my.id) dropped [anime-offline-database][aod]
     as dependency and changed license to MIT. ;-;

## Data format

* All data are based on how MAL index their database; if the title does not exist in MAL, then
  BATM will not index it.
* Season relationship will be inserted into array for better compability
  * See "Gintama" in [MAL][mgin] and [TMDB][tmgin] for use case.
* Episode correction uses Array in Array (`[[1, 2, 3], [4]]`) with index is MAL episode order
  while `int` represent Trakt episode order. `null` will be used if no correction used.
  * This is due to TMDB's rule regarding on how episode should be counted.
  * For example, if `episodes: [[1, 2, 3]]`, then Episode 1 in MAL equal to Episode 1-3 in
    TMDB/Trakt.
  * 3rd party app must resolve this splitted episode order from their end by subtracting
    runtime in MAL with episode runtime in TMDB.
  * See "Uchitama?! Have you seen my Tama?" in [MAL][muchi] and [TMDB][tmmuchi] for use case.
* Trakt data source info will be provided if it still uses TVDB or have been migrated to TMDB.
  * If the entry still uses TVDB, BATM will warn contributor about likely outdated info.
* While BATM has episode correction, BATM also provide episode offset started from 0.
  * For example, if `offset: 0`, then Trakt and MAL episode of that season started from
    `S01E01`, otherwise `offset: 12` would be `S01E13`.
  * Episode correction may also provided if the episode order in TMDB is splitted.
    Example:

    ```yaml
    offset: 25
    episodes: [[26, 27], [28], [29, 30, 31], ...]
    ```
    
* Music video and Advertorial will be excluded from BATM.
* Upcoming title/season should not be prioritized, unless full date of release is confirmed,
  available in Trakt, and data source from TMDB.
* If Trakt has multiple entries of the same show, BATM will prioritize complete and/or
  entry with most users.

## Contribution Guide

*Coming soon!*

## Dependencies Used

* [ATIP][atip]/[AniTrakt by Huere][at]
* [Jikan](https://jikan.moe) to get info of the title in MAL, alternative to MAL's official API
* [SIMKL] to get AniDB, AniList, Kitsu, and SIMKL ID
* [Trakt](https://trakt.com)

[aod]: https://github.com/manami-project/anime-offline-database
[als]: https://github.com/Anime-Lists/anime-lists
[at]: https://anitrakt.huere.net/
[atip]: https://github.com/ryuuganime/aniTrakt-IndexParser
[ryuu]: https://github.com/ryuuganime
[tmgin]: https://www.themoviedb.org/tv/57041
[mgin]: https://myanimelist.net/anime/918
[tmmuchi]: https://www.themoviedb.org/tv/96660
[muchi]: https://myanimelist.net/anime/39942
[SIMKL]: https://simkl.com

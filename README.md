<!-- markdownlint-disable MD033 -->
# BetterAnimeTraktMapper (BATM)

BATM: Bridging the gap between [MyAnimeList][MAL] and [Trakt][tk] with a
user-friendly solution for seamless data integration and episode order precision. 🚀

## Why?

[AniTrakt][at], crafted by the talented huere, boasts an impressive database
connecting [MAL] and [Trakt][tk]. However, when it comes to episode order and
non-Japanese media, the publicly available database falls a bit short.

Enter the alternative: [anime-lists][als]. Widely used by media server plugins
like Jellyfin, Emby, and Plex for scrobbling and fetching media information
accurately, anime-lists is a handy tool. However, it may hit a snag when an entry
in Trakt switches its data source from TVDB to TMDB, throwing a unique challenge
into the mix. To complicate matters, anime-lists can be a bit tricky to navigate,
thanks to its XML format and unconventional structure.

Cue the entrance of BATM! 🎉

BATM is a tool that combines the best of both worlds, offering a comprehensive
database that's easy to navigate and update while keeping it permissive with
its license ~~unlike that one particular database~~. No one really asked for it,
except maybe me (lol), but trust me, it's here to simplify things for you.

## How Does It Work?

1. **Searching for Shows:**
   * BATM asks you to tell the name of a show you like to search for.
   * It then looks in different places (like [ATIP][atip], [AniTrakt][at], and
     [SIMKL]) to find information about that show.
2. **Finding the Right Season:**
   * It tries to guess the right part based on the name of the show. For
     example, if the show is called "Poputepipikku 2nd Season," BATM knows to
     look for the second season of the show on Trakt and asks if it's correct.
   * If the show has more than one season and BATM can not understand previous
     step, BATM will asks you which season you're talking about.
   * If there's only one season, BATM just picks it for you, unless there's a
     special season (Season 0), then it asks you which one you mean.
3. **Checking Episodes:**
   * BATM makes sure that the episodes match up correctly.
   * If there are too few or too many episodes compared to [MAL], BATM asks you
     to help fix it. It might ask if you want to adjust the episode numbers.
4. **Adding IDs for Better Connections:**
   * BATM wants to make sure it connects well with other cool apps, so it
     collects extra information (IDs) from different sites (AniDB, AniList,
     IMDb, Kitsu, SIMKL, TMDB, and TVDB) as well.
   * But, for now, it doesn't fix any episode problems on those other sites.
     It's saving that for a future project on Ryuuganime.

<details>
<summary>A little bit technical explanation</summary>
<blockquote><strong>Note</strong><br/>
tl;dr: BATM will attempt to locate the most suitable match for the title by
analyzing data from numerous sources (or manually inputting if none available)
and subsequently requesting the user to confirm the outcome.
</blockquote>

1. BATM will ask user to provide title to lookup. Then based on the data:
   * BATM will fetch data from [ATIP][atip] for latest exisiting mapping from
     [AniTrakt][at]
   * If none, BATM will check on [SIMKL] if there's existing relationship to Trakt.
   * If not exist at all, BATM will ask user to manually link/map entry to Trakt.
2. BATM will check if the title has multiple seasons, and ask user to select
   which season to map.
   * BATM will try to guess which season to map based on the title from MAL. For
     example, if MAL title is "Poputepipikku 2nd Season", then BATM will try to
     find 2nd season in Trakt and ask user to confirm.
   * If the title has multiple seasons, BATM will ask user to select which season
     to map.
   * If the title has only one season, BATM will automatically select it, UNLESS
     the title has Season 0 (Special), then BATM will ask user to select which
     season to map.
3. BATM will check if episode on the season matches with MAL episode schema.
   * If the season has less episodes than MAL counterpart, it will prompt user
     to add additional season to the array, and do episode range correction.
   * If the season has more episodes than MAL counterpart, it will prompt user
     to do episode range correction or add episode offset.
   * Else, user will be asked to add episode offset.
4. BATM will populate additional IDs from AniDB, AniList, IMDb, Kitsu, SIMKL,
   TMDB, and TVDB for better integration with 3rd party applications, but won't
   add additional episode correction to each platforms.
   * This will be solved by my future project in [Ryuuganime][ryuu] to fix all
     this mess once BATM finished, and [animeApi](https://animeapi.my.id)
     dropped [anime-offline-database][aod] as dependency and changed license to
     MIT.

</details>

## Data Format Overview

Here's a guide to how BATM organizes its data:

### Title Inclusion

* BATM uses [MAL] database as its reference, so if a title isn't on MAL, BATM
  won't include it.

### Season Relationships

* BATM organizes season relationships in an array for smoother compatibility.
  * Check out the "Gintama" example on [MAL][mgin] and [TMDB][tmgin] for a
    real-life scenario.

### Episode Corrections

* BATM handles episode corrections using a user-friendly approach: an Array in
  Array (`[[1, 2, 3], [4]]`).
  * This setup aligns MAL episode order with Trakt episode order, using `null`
    if no corrections are needed.
  * This helps accommodate TMDB's episode counting rules.
  * For instance, if `episodes: [[1, 2, 3]]`, Episode 1 in MAL corresponds to
    Episode 1-3 in TMDB/Trakt.
  * Third-party apps can easily resolve any episode order splits by adjusting
    runtimes by comparing expected runtime in MAL with actual runtime in TMDB.
  * Check out "Uchitama?! Have you seen my Tama?" on [MAL][muchi] and
    [TMDB][tmmuchi] for a practical example.

### Episode Offsets with Corrections

* BATM not only corrects episodes but also offers episode offsets starting from 0.
  * For example, an offset of `0` means Trakt and MAL episodes for that season
    start from `S01E01`.
  * If a correction is applied, the offset compensates for any mismatch between
    the episode orders in MAL and TMDB/Trakt.
  * For instance:

    ```yaml
    offset: 25
    episodes: [[26, 27], [28], [29, 30, 31], ...]
    ```

    If the MAL episode is Episode 1, with a 25-episode offset, it corresponds to
    Episode 26-27 in TMDB/Trakt, and so on.
  * This comprehensive approach helps handle both corrections and offsets
    seamlessly.

### Trakt Data Source

* BATM provides info on Trakt's data source, specifying whether it still uses
  TVDB or has migrated to TMDB.
  * A warning is issued if the entry still uses TVDB, alerting contributors to
    potentially outdated info.

### Exclusions and Prioritization

* BATM excludes music videos and advertorials.
* Upcoming titles/seasons aren't prioritized unless there's a confirmed release
  date, available in Trakt, and sourced from TMDB.

### Handling Multiple Trakt Entries

* In cases of multiple Trakt entries for the same show, BATM prioritizes
  completeness and the entry with the most users.

## Where to find the data?

You can find the data in `data` folder, and the data will be provided in 2
different format:

* `data.bson` is the raw data in BSON (Binary JSON) format, which can be
  imported to MongoDB directly (or any application that supports BSON). File is
  significantly smaller than JSON format.
* `data.json` is the data in JSON format, which can be used by any application
  that supports JSON.

## Contribution Guide

*Coming soon!*

## Dependencies Used

* [ATIP][atip]/[AniTrakt by Huere][at]
* [Jikan](https://jikan.moe) to get info of the title in MAL, alternative to
  MAL's official API
* [SIMKL] to get AniDB, AniList, Kitsu, and SIMKL ID
* [Trakt][tk]

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
[tk]: https://trakt.tv
[MAL]: https://myanimelist.net

import os
import re
import threading
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from typing import List


URL: str = "http://s8.bitdl.ir/Series/friends/"
BASE_FOLDER: str = "Friends/"
THREADS: int = 10

sem: threading.Semaphore = threading.Semaphore(THREADS)
threads_pool: List[threading.Thread] = []


def wait_threads() -> None:
    for thread in threads_pool:
        thread.join()


def url_retrieve(url: str, outfile: Path) -> None:
    R: requests.models.Response = requests.get(url, allow_redirects=True)

    if R.status_code != 200:
        raise ConnectionError(
            'could not download {}\nerror code: {}'.format(url, R.status_code))

    outfile.write_bytes(R.content)
    sem.release()


def download_episode(episode: Tag, season_link: str, out_dir: str) -> None:
    episode_title: str = episode['title']
    episode_link: str = season_link + episode['href']
    episode_path: str = f'{out_dir}/{episode_title}'

    if os.path.isfile(episode_path):
        print(f'Skiping {episode_title}')
        return

    sem.acquire()

    print(f'Downloading {episode_title}')

    thread: threading.Thread = threading.Thread(target=url_retrieve, args=(
        episode_link, Path(episode_path),))
    thread.start()
    threads_pool.append(thread)


def download_season(season: Tag):
    season_title: str = season['title']
    season_link: str = URL + season['href']
    season_path: str = BASE_FOLDER + season_title

    if not os.path.isdir(season_path):
        os.mkdir(season_path)

    season_page: str = requests.get(season_link).text
    season_soup: BeautifulSoup = BeautifulSoup(season_page, 'html.parser')
    episodes: ResultSet = season_soup.find_all(
        'a', {'href': re.compile(r'(f|F)riends.*')})
    for episode in episodes:
        download_episode(episode, season_link, season_path)


def get_seasons() -> ResultSet:
    seasons_page: str = requests.get(URL).text
    seasons_soup: BeautifulSoup = BeautifulSoup(seasons_page, 'html.parser')
    seasons: ResultSet = seasons_soup.find_all(
        'a', {'href': re.compile(r'S\d+/')})
    return seasons


def main() -> None:
    if not os.path.isdir(BASE_FOLDER):
        os.mkdir(BASE_FOLDER)

    seasons = get_seasons()

    for season in seasons:
        download_season(season)

    wait_threads()


if __name__ == '__main__':
    main()

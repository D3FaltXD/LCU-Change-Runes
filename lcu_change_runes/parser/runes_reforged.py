"""Rune Manager for scrapers"""
import requests
from lcu_change_runes.parser.constants import (MISSING_SHARDS,
                                               URL_RUNES_REFORGED)


class RunesReforged:
    """Rune management"""

    def __init__(self):
        self.runes = {}

    def get_runes_from_source(self):
        """Gets all runes from data dragon CDN

        Returns:
            JSON of all runes
        """
        return requests.get(URL_RUNES_REFORGED).json()

    def parse_all_runes(self):
        """Converts runes from data dragon into key-value pairs of id and rune name"""

        all_runes = self.get_runes_from_source()
        for rune_path in all_runes:
            self.runes[rune_path["id"]] = rune_path["name"]
            for runes in rune_path["slots"]:
                for rune in runes["runes"]:
                    self.runes[rune["id"]] = rune["name"]

        self.runes.update(MISSING_SHARDS)

    def map_to_id(self, raw_runes):
        """FOR SCRAPERS
        Standardizes and maps runes to their respective ids/names

        Args:
            raw_runes: Rune names obtained from scraping a website

        Returns:
            Key-value pairs of id and rune name
        """
        mapped_runes = []
        for rune in raw_runes:
            for rune_id, rune_name in self.runes.items():
                if rune_name in rune:
                    mapped_runes.append((rune_id,rune_name))
        return mapped_runes


if __name__ == "__main__":
    _runes = RunesReforged()
    _runes.parse_all_runes()
    print(_runes.runes)

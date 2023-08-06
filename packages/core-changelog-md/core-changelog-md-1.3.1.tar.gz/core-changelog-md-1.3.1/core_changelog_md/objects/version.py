import datetime
import re
from typing import Optional

import packaging.version

from core_changelog_md.exceptions import VersionNotFoundException
from core_changelog_md.objects.changes import ChangeCollection


class VersionCollection(list):
    def sorted(self):
        return sorted(self, reverse=True)

    def text(self):
        result = ''
        for index, item in enumerate(self.sorted()):
            if index == 0 and item.version.public.lower() != 'unreleased':
                result += VersionBlock(version='unreleased').text()
            result += item.text()
        return result.strip()

    def get_by_name(self, version_name):
        for item in self:
            if item.version.public == version_name:
                return item
        raise VersionNotFoundException(f"Not found version {version_name} in {self.names()}")

    def names(self):
        return [item.version.public for item in self.sorted()]


class VersionBlock(object):
    RE_NUM_VERSION_BLOCK = re.compile(r'\[([0-9\.]+)\]')
    RE_NUM_RC_VERSION_BLOCK = re.compile(r'\[([0-9\.]+.[a-zA-Z0-9]+)\]')

    RE_VERSION_BLOCK = re.compile(r'\[([A-Za-z0-9])\]')

    def __init__(self, version, date=None, change_collection=None):
        self.change_blocks = change_collection if change_collection else ChangeCollection()
        self.version: packaging.version.Version = packaging.version.parse(version)
        self.date: Optional[datetime.datetime] = date

    def __str__(self):
        return self.version.public

    def __gt__(self, other):
        if 'unreleased' in [self.version.public, other.version.public]:
            return other.version.public.lower() != 'unreleased'
        return self.version > other.version

    def __lt__(self, other):
        if 'unreleased' in [self.version.public.lower(), other.version.public.lower()]:
            return self.version.public.lower() != 'unreleased'
        return self.version < other.version

    def __eq__(self, other: "VersionBlock"):
        value = other.version.public if isinstance(other, VersionBlock) else other
        return self.version.public == value

    def get_priority(self) -> int:
        """
        Возвращает приоритет поднятия версии согласно типам изменений
        Fixed, Misc (Приоритет 1) - меняет patch версию
        Featured, Changed (Приоритет 0) - меняет minor версию
        """
        changes = [item.change_type.priority for item in self.change_blocks.values() if item.changes]
        return min(changes) if changes else None

    def text(self):
        """
        Возвращает приведенный к тексту элемент
        """
        result = f"## [{self.version.public.upper()}]"
        result = result + f' - {self.date.strftime("%Y-%m-%d")}\n' if self.date else result + '\n'
        for item in self.change_blocks:
            result += self.change_blocks[item].text()
        if self.version.public.lower() == 'unreleased':
            result += '\n---\n\n'
        else:
            result += '\n'
        return result

import os
import re
import logging
import lxml.html
from typing import List, Tuple, Optional, Union

import bs4


log = logging.getLogger(__name__)


def is_html(s: str) -> bool:
    # from bs4 import BeautifulSoup
    # bool(BeautifulSoup(html, "html.parser").find())
    # True
    # bool(BeautifulSoup(non_html, "html.parser").find())
    # False

    # import lxml.html
    # html = 'Hello, <b>world</b>'
    # non_html = "<ht fldf d><"
    # lxml.html.fromstring(html).find('.//*') is not None
    # True
    # lxml.html.fromstring(non_html).find('.//*') is not None
    # False
    return lxml.html.fromstring(s).find('.//*') is not None


def is_filepath(s: str) -> bool:
    return os.path.exists(s) and os.path.isfile(s)


class UntwinerError(Exception):
    """"""


class Link:
    def __init__(self, data: str):
        self.data = data
        temp = data.replace('[[', '').replace(']]', '')

        try:
            if '->' in temp:
                self.text, self.target = temp.split('->')
            elif '<-' in temp:
                self.target, self.text = temp.split('<-')
            elif '|' in temp:
                self.text, self.target = temp.split('|')
            else:
                self.text, self.target = temp, temp
        except ValueError as err:
            log.exception('Link={}; Error={};'.format(data, err))


class Node:
    """
    Implements a passage from the story map.
    """

    def __init__(self, passage_text: str, **kwargs):
        self.data = passage_text

        self.id = int(kwargs.get('pid', -1))
        self.name = kwargs.get('name')
        self.tags = kwargs.get('tags', '').split()

        self.media = self._parse_media(passage_text)
        self.links = self._parse_links(passage_text)
        self.text = self._prepare_text(passage_text, self.media, self.links)

    @staticmethod
    def _parse_media(data: str) -> List[str]:
        expr = r'(?:<img.+?>|<audio.+?>.+?</audio>' \
               r'|<video.+?>.+?</video>|<(?:!|/?[a-zA-Z]+).*?/?>)'
        return re.findall(expr, data)

    @staticmethod
    def _parse_links(data: str) -> List[Link]:
        links = []
        expr = r'\[\[.+?\]\]'

        for link_text in re.findall(expr, data):
            links.append(Link(link_text))

        return links

    @staticmethod
    def _prepare_text(data: str,
                      media: List[str],
                      links: List[Link]) -> str:
        text = data

        for link in links:
            text = text.replace(link.data, link.text)
        for media in media:
            text = text.replace(media, '')

        return text.strip()


class Untwiner:
    """
    Implements a the story map.
    """
    ROOT_TAG = 'tw-storydata'
    NODE_TAG = 'tw-passagedata'

    def __init__(self, twine_doc: str, encoding: str = 'utf-8'):
        """
        :param twine_doc:
        :param encoding:
        """

        if is_html(twine_doc):
            self.data = twine_doc
        elif is_filepath(twine_doc):
            with open(twine_doc, 'r', encoding=encoding) as f:
                self.data = f.read()

        self._parser = bs4.BeautifulSoup(self.data, 'lxml')
        self._story_map = {}
        self._meta = {}

        self._load_story()

    @property
    def parser(self) -> bs4.BeautifulSoup:
        if not self._parser and self.data:
            self._parser = bs4.BeautifulSoup(self.data, 'lxml')
        elif not self.data:
            raise UntwinerError('Empty data.')
        return self._parser

    def _load_story(self):
        root = self.parser.find_all(self.ROOT_TAG)[0]
        self._meta.update(root.attrs)
        # TODO: process by story format

        passages = self.parser.find_all(self.NODE_TAG)
        for passage in passages:
            name = passage.attrs.get('name')
            self._story_map[name] = Node(str(passage.string), **passage.attrs)

    def start_node(self) -> Optional[Node]:
        return self.node_by_id(int(self._meta.get('startnode')))

    def node_by_id(self, node_id: int) -> Optional[Node]:
        for item in self._story_map.values():
            if item.id == node_id:
                return item
        return None

    def node_by_name(self, name: str) -> Optional[Node]:
        return self._story_map.get(name)

    def node_by_link(self, next_node: Link) -> Optional[Node]:
        return self._story_map.get(next_node.target)

    def nodes_by_tags(self, tags: Union[str, List[str]]) -> List[Optional[Node]]:
        result = []
        tags = tags.split() if isinstance(tags, str) else tags
        for item in self._story_map.values():
            for tag in tags:
                if tag in item.tags:
                    result.append(item)
                    break
        return result

    def __getitem__(self, item: Union[int, str, Link]) -> Node:
        if isinstance(item, str):
            return self.node_by_name(item)
        if isinstance(item, Link):
            return self.node_by_link(item)
        if isinstance(item, int):
            return self.node_by_id(item)
        raise UntwinerError('Unsupported type')

    @property
    def title(self) -> str:
        return self._meta.get('name')

    @property
    def creator(self) -> str:
        return self._meta.get('creator')

    @property
    def creator_version(self) -> str:
        return self._meta.get('creator-version')

    @property
    def format(self) -> str:
        return self._meta.get('format')

    @property
    def format_version(self) -> str:
        return self._meta.get('format-version')

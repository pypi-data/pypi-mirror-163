# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grab_fork_from_libgen']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.8.0,<0.9.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'lxml>=4.8.0,<5.0.0',
 'requests-html>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'grab-fork-from-libgen',
    'version': '3.1.0',
    'description': 'A fork of grab-convert-from-libgen',
    'long_description': '# grab-fork-from-libgen\nA fork of grab-convert-from-libgen, which is an easy API/wrapper for searching and downloading books from Libgen.\n\n## A disclaimer  \nFirst and foremost, this library makes no effort in rate-limiting itself.  \nWhile using it, you need to know that you are using a free "API", that requires no API key.  \nUse it with care.  \n\nThere\'s a lot of ratelimiting options for Python out there.  \n[ratelimit](https://github.com/tomasbasham/ratelimit) is a good starting point.  \n\n## Before Installing\n\n**If you want to download books, be sure that you have installed Calibre and have added the necessary `ebook-convert` command to your path!**\n\n[calibre](https://calibre-ebook.com/) is "a powerful and easy to use e-book manager". It\'s also free, open-source, and super easy to use.\n\nYou can install an calibre executable, through MacOS Homebrew, compile from source... pick your poison. They only thing you need to be sure of \nis the command `ebook-convert` is in your PATH.\n\nIf you choose not to do so, you can still use this library for searching on LibraryGenesis and scraping metadata.\n\n## Install\n\nInstall by \n\n```\npip install grab-fork-from-libgen\n```\n\n### Migrating\nIf you already have `grab-convert-from-libgen` installed, run this:  \n```\npip uninstall grab-convert-from-libgen\n```\n\nAnd then:\n\n```python\n# Change\nfrom grab_fork_from_libgen import *\n# To\nfrom grab_fork_from_libgen import *\n```\nThat\'s it. Your code will still work as expected, and you can implement the new features as you go.\n\n### Fork Overview\nA possible merging with the original repo is on the works, but i will keep this repo open because i may need to push some changes when i need it.\nFor now, every new feature is exclusive to this fork, but when the merging happens, only the features exclusive to this will be listed here.\n\n### v3 Overview\n\nThis new version includes these new features:\n\nNew async classes.  \nNew filtering option.  \nYou can now get a book\'s cover. (from 3lib or LibraryRocks)  \nYou can now get a book\'s direct download links. (from LibraryLol)  \nYou can now get a book\'s description (if it has one) (also from LibraryLol).  \nYou can now get pagination info (Check how many pages and if there\'s a next page in your search.)  \nFixed "page" query in Fiction search.  \nSome small fixes for edge cases.  \n\nIn this version, every entry has these new properties attached:  \nIt\'s md5 (e.g.: `B86D006359AD3939907D951A20CB4EF1`)  \nIt\'s topic (either `fiction` or `sci-tech`)  \nAnd now fiction results also have `extension` and `size` to improve consistency.\n\n**PS**: Pagination is slower. You are adding the extra overhead of rendering javascript, so expect longer wait times.\n\nIf you were using this fork before, and is migrating to v3, please pay attention to this:  \n*If not, just jump to the documentation*  \n\nAs of v3, `Metadata.get_metadata()` actually returns relevant metadata.\nThe `description` value should be more consistent, since we are now scraping the main libgen website.\nSee the `Metadata` class docs below for more info.\n\nThe download links scraping has been moved to `Metadata.get_download_links()` and now only returns download links.\n\n## Quickstart\n\nThe example below shows how to grab the first book returned from a search and save it to your current working directory as a pdf.\n\n```python\nfrom grab_fork_from_libgen import LibgenSearch\n\nres = LibgenSearch(\'sci-tech\', q=\'test\')\n\nres.first(convert_to=\'pdf\')\n```\n\nThis is an example that gets and downloads the first book that matches the given filter(s).\n\n```python\nfrom grab_fork_from_libgen import LibgenSearch\n\nres = LibgenSearch(\'fiction\', q=\'test\')\n\nres.get(title=\'a title\', save_to=\'.\')\n# Or\nres.get(language="English", save_to=\'.\')\n```\n\nThis one shows basic search usage (with pagination on).\n\n```python\nfrom grab_fork_from_libgen import LibgenSearch\n\n# Refer to the documentation below to learn more about query filters.\nlibgen = LibgenSearch(\'sci-tech\', q=\'test\', res=100)\n# True as an argument means you opt-in in pagination info.\nlibgen_search = libgen.get_results(True)\n\npagination_info = libgen_search["pagination"]\nlibgen_results = libgen_search["data"]\n```\n\nAnd for the async versions:\n\n```python\nfrom grab_fork_from_libgen import AIOLibgenSearch\n\n\nasync def libgen():\n    # Refer to the documentation below to learn more about query filters.\n    libgen = AIOLibgenSearch(\'fiction\', q=\'test\', language=\'English\', criteria="title")\n    # We opt-out of pagination info this time...\n    # So the function returns your results directly\n    libgen_results = await libgen.get_results()\n\n```\n\nYou must specify a `topic` when creating a search instance. Choices are `fiction` or `sci-tech`.\n\n## Documentation\n\nOnly search parameters marked as required are needed when searching.\n\n### Libgen Non-fiction/Sci-tech\n#### Search Parameters\n\n`q`: The search query (required)\n\n`sort`: Sort results. Choices are `def` (default), `id`, `title`, `author`, `publisher`, `year`\n\n`sortmode`: Ascending or descending. Choices are `ASC` or `DESC`\n\n`column`: The column to search against. Choices are `def` (default), `title`, `author`, `publisher`, `year`, `series`, `ISBN`, `Language`, or `md5`.\n\n`phrase`: Search with mask (word*). Choices are `0` or `1`.\n\n`res`: Results per page. Choices are `25`, `50`, or `100`.\n\n`page`: Page number.\n\n### Libgen Fiction\n#### Search Parameters\n\n`q`: The search query (required)\n\n`criteria`: The column to search against. Choices are `title`, `authors`, or `series`.\n\n`language`: Language code\n\n`format`: File format\n\n`wildcard`: Wildcarded words (word*). Set to `1`.\n\n`page`: Page number\n\n\n### LibgenSearch\n#### get_results\n\n`get_results(self, pagination: Optional[bool]) -> OrderedDict[int, SearchEntry] | Dict`\n\nCaches and returns results based on the search parameters the `LibgenSearch` objects was initialized with. \nTakes one optional boolean argument.\n\nIf it\'s **True**: \nReturns a dict, with two values, the first one being:  \n```\npagination = {\n    "current_page": `int`\n    "total_pages": `int`\n    "has_next_page": either `True` or `False`\n}\n```\nAnd the second one being an ordered dict, which is your search results:\n```\ndata = {\n    0: "{first_book_title, first_book_md5, ...}"\n    1: "{second_book_title, second_book_md5, ...}"\n    ...\n}\n```\nIf the user sets pagination to **False** or doesn\'t provide any value, this OrderedDict is the only result returned.\n\nPlease refer to `Quickstart` for a quick guide.\n\nResults are ordered in the same order as they would be displayed on libgen itself with the book\'s id serving as the key.\n\nYou can also import the `SearchEntry` model to see which values are present in each search result entry.\n\nThe async version and pagination info is powered by [requests-html](https://github.com/psf/requests-html)\n\n**Notice**:  \nUsing pagination will download Chromium to your home folder on your first run. e.g.: "~/.pyppeteer/".\nThis only happens once. This happens because LibraryGenesis pagination uses javascript, \nwhich is not rendedered by default in the HTML, to render its pagination system.  \nBecause of this, the pagination system is generally slower than its counterpart.\n\nIt\'s important to pay attention to this if you use services (like Heroku Free Tier) with limited storage space and low timeouts.\n\n**Notice 2**:  \nFor now, there\'s a `\'file\'` attribute on fiction results that may seem redundant when you have `\'extension\'` and\n`\'size\'`. That\'s because these are only available on this fork, and i didn\'t want to break people\'s logic, regex etc\nwhen migrating.  \nThis probably will be removed in a distant future, just ignore it for now.\n\n#### first\n\n`first(save_to: str = None, convert_to: str = None) -> Dict`\n\nReturns the first book (as a dictionary) from the cached or obtained results.\nYou can provide a `save_to: str` value if you want to download the book.\nAnd you can convert it using `convert_to: str`. Only `pdf`, `epub` and `mobi` are allowed. \nIf you want to get a specific book based on filters, please refer to `get`.\n\nThe async version is powered by [aiofiles](https://github.com/Tinche/aiofiles)\n\n#### get\n\n`get(save_to: str = None, convert_to: str = None, **filters) -> Dict`\n\nReturns the first book (as a dictionary) from the cached or obtained results that match any given filter parameter.\nYou can provide a `save_to: str` value if you want to download the book.\nAnd you can convert it using `convert_to: str`. Only `pdf`, `epub` and `mobi` are allowed.\n\nThe filters can be anything that\'s inside a book entry.\nFor example:\n````python\nfilters = {\n    "author(s)": "Adams, Jennifer",\n    "language": "English"\n}\n````\nThis method returns a book if it\'s match **ANY** of the filters, that means it will return even if it doesn\'t match \n**all** of them.\n\nIf you want to match more than one book or have more strict filtering, refer to `get_all`.\n\nThe async version is powered by [aiofiles](https://github.com/Tinche/aiofiles)\n\n#### get_all\n\n`get_all(**filters) -> Dict`\n\nThis method returns all books that match the given filters.  \n\nIt differs from `get` in two ways:  \nFirst, it will return **all** books that match, not just the first one.  \nSecond, a book will only be matched if **all** of the filters match.\n\n#### **Why can\'t i save the books directly?**\nThis would go directly against what was mentioned about API rates.  \nDownloading, say, 30 books on one go would probably mean a block from either LibraryGenesis or Librarylol (the main download\nprovider).  \nIt\'s also harder to implement rate limiting in a method like this.\n\nOf course, you are free to implement your own logic using `get`.\n\n### Metadata\nThis class holds the methods responsible for metadata scraping.\n\n#### Quickstart:\n\n```python\n# First, import the Metadata class from grab_fork_from_libgen.\nfrom grab_fork_from_libgen import LibgenSearch, Metadata\n\n# ...\n# pagination=True means you opt-in for pagination info.\nmy_results = LibgenSearch.get_results(pagination=True)\n\n# Get the values from your search results\nsearch_results = my_results["data"]\n\n# Get the info from the first entry in the results.\nmd5 = search_results[0]["md5"]\ntopic = search_results[0]["topic"]\n\n# Instantiate a new Metadata class.\n# Please read the timeout documentation on the official requests library docs.\nmeta = Metadata(timeout=(9, 18))\n\n# And use the respective methods.\ncover = meta.get_cover(md5)\nd_links_and_desc = meta.get_metadata(md5, topic)\n\n```\n#### Metadata - Class\nThe `Metadata` class takes one being optional argument:\\\n\n`timeout (optional)` = Either `int`, `tuple` or `None`. Defaults to `None`, which equals to infinite timeout.\\\n\nPlease read more about using tuples in the official `requests` \n[docs](https://docs.python-requests.org/en/latest/user/advanced/#timeouts).\n\nIt\'s good practice to always provide a timeout value. As both the cover and metadata providers can be down or\nslow at any given moment.\\\nIf they take too long, your code will hang.\n\nYou can expect a `MetadataError` if something goes wrong.\n\n#### Metadata - Methods\n\n`get_cover(md5: str) -> str`  \nThe return string is a valid image url, corresponding to a file cover.  \n\n`get_metadata(md5: str, topic: str) -> dict`\nThis method will scrape the main libgen website for relevant info about a specific file in a specific topic.  \nThis further improves on the metadata that you receive from search results.  \nThis is the dictionary schema:  \n**All values are either `str` or `None`**  \n`title`  \n`authors`\n`edition`\n`language`\n`year`\n`publisher`\n`isbn`\n`extension`\n`size`\n`description`\n\n`get_download_links(md5: str, topic: str) -> dict`  \n\nThis will return valid direct download links for a given md5 in a given topic.  \n\n*This used to be part of `.get_metadata()`, but is now on it\'s on method because we are scraping a different url.*  \n\nThrows a `MetadataError` if no download link is found.\nIf no description is found, returns `None` on the second value instead.\n\nPlease do note that none of these methods are rate-limited. If you abuse them, you will get blocked.  \nFrom personal experience, `1500ms-2000ms` between each call is probably safe.\n\nIf something you believe should exist, doesn\'t, please make sure you are using a valid md5 and the topic provided corresponds to it.  \nIf it\'s still not working as expected, please open an issue describing the issue and we will look into it asap.\n\n### Async Classes\n#### AIOLibgenSearch\nThis class is now truly async, even the file operations.\nConverting books itself (using Calibre) is still synchronous until further testing.\n\nAsync I/O is provided by `aiofiles` and `requests-html`.\n\n#### AIOMetadata\nAsync methods in this classes are made using `requests-html`.',
    'author': 'Lamarcke',
    'author_email': 'cassiolamarcksilvafreitas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Lamarcke/grab-fork-from-libgen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

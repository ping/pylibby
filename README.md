# PyLibby, a CLI for Libby

This tool lets you borrow, download and return (audio)books from [Libby](https://libbyapp.com) (OverDrive). 
You can download audiobooks without the extra step of getting the ODM file first.


## How to run PyLibby
You can use pipenv, first install the stuff in the Pipfile (you only need to do this the first time):
```bash
pipenv install
```
Then run PyLibby like this
```bash
pipenv run python pylibby.py -h
```

<pre>CLI for Libby

options:
  -h, --help            show this help message and exit
  -id path, --id-file path
                        Path to id JSON (which you get from '--code'. Defaults to ./config/id.json).
  -c 12345678, --code 12345678
                        Login with code.
  -o path, --output path
                        Output dir, will output to current dir if omitted.
  -s "search query", --search "search query"
                        Search for book in your libraries.
  -sa "search query", --search-audiobook "search query"
                        Search for audiobook in your libraries.
  -se "search query", --search-ebook "search query"
                        Search for ebook in your libraries.
  -ls, --list-loans     List your current loans.
  -lsc, --list-cards    List your current cards.
  -lsh, --list-holds    List your current holds.
  -b id, --borrow-book id
                        Borrow book from the first library where it's available.
  -r id, --return-book id
                        Return book. If the same book is borrowed in multiple libraries this will only return the first one.
  -ho id, --hold-book id
                        Hold book from the library with the shortest wait.
  -ch id, --cancel-hold id
                        Cancel hold. If the same book is held in multiple libraries this will only return the first one.
  -dl id, --download id
                        Download book or audiobook by title id. You need to have borrowed the book.
  -f id, --format id    Which format to download with -dl.
  -dla format, --download-all format
                        Download all loans with the specified format. Does not consider -f.
  -odm                  Download the ODM instead of directly downloading mp3's for 'audiobook-mp3'.
  -si, --save-info      Save information about downloaded book.
  -i id, --info id      Print media info (JSON).
  -a path, --archive path
                        Path to archive file. The archive keeps track of what is already downloaded. Defaults to ./config/archive.json
  -j, --json            Output verbose JSON instead of tables.
  -e, --embed-metadata  Embeds metadata in MP3 files, including chapter markers.
  -opf, --create-opf    Create an OPF file with metadata when downloading a book.
  -dlo id, --download-opf id
                        Generate an OPF file by title id.
  -ofs string, --output-format-string string
                        Format string specifying output folder(s), default is "%a/%y - %t".
                        %a = Author(s).
                        %n = Narrator(s).
                        %i = ISBN.
                        %o = Overdrive ID.
                        %p = Publisher.
                        %s = Series.
                        %s{STRING} = Will place STRING in folder name if book is in series, else nothing.
                        %S = Subtitle.
                        %S{STRING} = Will place STRING in folder name if book has a subtitle, else nothing.
                        %t = Title.
                        %v = Volume (book in series).
                        %y = Year published.
  -rs, --replace-space  Replace spaces in folder path with underscores.
  -t TIMEOUT, --timeout TIMEOUT
                        Download timeout interval (seconds).
  --retry {0,1,2,3,4,5}
                        Maximum download retry attempts.
  -v, --version         Print version.
</pre>

Alternatively you can run PyLibby without pipenv, but make sure you have 
installed the requirements, "requests", "tabulate", "dicttoxml" and "mutagen". Minimum Python version is 3.10.


You need to log in before you can start using PyLibby. 
You can do this by logging in to Libby on any device and
going to Settings->Copy To Another Device.
You will get a code there which you can use like this:

```bash
python pylibby.py -c 12345678
```

To check if you are logged in you can try listing your loans like this:
```bash
python pylibby.py -ls
```
<pre>+--------+-----------+---------------------+-----------+----------+--------------+--------------+---------------+
|     Id | Type      | Formats             | Library   |   CardId | Authors      | Title        | Narrators     |
+========+===========+=====================+===========+==========+==============+==============+===============+
| 123456 | ebook     | ebook-overdrive     | name1     | 87654321 | Mary Shelley | Frankenstein |               |
|        |           | ebook-epub-adobe    |           |          |              |              |               |
|        |           | ebook-epub-open     |           |          |              |              |               |
+--------+-----------+---------------------+-----------+----------+--------------+--------------+---------------+
| 654321 | audiobook | audiobook-overdrive | name2     | 12345678 | Bram Stoker  | Dracula      | Tavia Gilbert |
|        |           | audiobook-mp3       |           |          |              |              | J. P. Guimont |
+--------+-----------+---------------------+-----------+----------+--------------+--------------+---------------+
</pre>

To download a book you need to specify the format and output path. 
For audiobooks the format will always be "audiobook-mp3".
```bash
python pylibby.py -dl 654321 -f audiobook-mp3 -o /home/username/books
```

When downloading a book, you can specify the output format using a custom
format string. Substitutions include:

%t - title  
%a - author  
%s - series  
%S - subtitle  
%v - volume (book in series)  
%p - publisher  
%y - year published  
%n - narrator  
%i - ISBN  
%o - Overdrive ID  

Additionally, you can include text, but make it conditional on if the book is in
a series. To do so, simply include:

%s{/}

Which will render to / if there is a series, but if the book is not in a series,
will just disappear.

This similarly works on subtitle existence with %S{STRING}

Use -rs to change spaces in folder names to "_".

Thus, an example is:
```bash
python pylibby.py -dl 654321 -f audiobook-mp3 -ofs "%a/%t"
```

Which will result in a folder structure like:

Jane Austen/Pride and Prejudice/file.mp3

You can search for books like this:
```bash
python pylibby.py -s "moby dick"
```
<pre>+---------+-----------+---------------------+------------------------+-----------------+-----------+------------------+
|      Id | Type      | Formats             | Libraries              | Authors         | Title     | Narrators        |
+=========+===========+=====================+========================+=================+===========+==================+
| 1234567 | audiobook | audiobook-overdrive | name3: available       | Herman Melville | Moby Dick | Pete Cross       |
|         |           | audiobook-mp3       |                        |                 |           |                  |
+---------+-----------+---------------------+------------------------+-----------------+-----------+------------------+
|  654321 | ebook     | ebook-overdrive     | name1: available       | Herman Melville | Moby Dick |                  |
|         |           | ebook-epub-adobe    | name2: unavailable     |                 |           |                  |
|         |           | ebook-epub-open     | name3: unavailable     |                 |           |                  |
|         |           | ebook-pdf-adobe     | name4: available       |                 |           |                  |
|         |           | ebook-pdf-open      |                        |                 |           |                  |
+---------+-----------+---------------------+------------------------+-----------------+-----------+------------------+
| 1111111 | ebook     | ebook-kindle        | name1: available       | Herman Melville | Moby Dick |                  |
|         |           | ebook-overdrive     |                        |                 |           |                  |
|         |           | ebook-epub-adobe    |                        |                 |           |                  |
|         |           | ebook-kobo          |                        |                 |           |                  |
+---------+-----------+---------------------+------------------------+-----------------+-----------+------------------+
</pre>

You can chain together multiple arguments like this:
```bash
python pylibby.py -b 87654321 -b 12345678 -ls -dl 12345678 -f audiobook-mp3 -r 12345678 -ls
```

## Environment variables
PyLibby can take some environment variables. These are:
* CODE - code that you get from the Libby app
* DOWNLOAD_ALL - format
* SAVE_INFO - save json information about downloaded books, value can be anything
* EMBED_METADATA - embed metadata in mp3 files, value can be anything
* CREATE_OPF - create metadata opf when downloading, value can be anything
* OUTPUT_FORMAT_STRING - output format string
* ARCHIVE - path to archive.json
* ID - path to id.json
* OUTPUT - output path
* RETRY - maximum download retry attempts (max 5, anything over = 0)
* TIMEOUT - download timeout in seconds

These can be used like this:
```bash
CODE=12345678 DOWNLOAD_ALL=audiobook-mp3 EMBED_METADATA=yes CREATE_OPF=yes ARCHIVE="./config/archive.json" OUTPUT="./Books" python pylibby.py
```

## Docker and cron
You can schedule --download-all with cron so that you always have your books ready.
To make this easier you can use the provided docker-compose file.
Open docker-compose.yml in any text editor and edit it to suit your needs.
When you are done, go into the Libby app on your phone or in the browser and get a new code.
Enter the code where it says CODE=00000000 in the file, then quickly(!) run:
```bash
docker-compose up -d
```
You have to be fast or else the code will expire.


## Doesn't work?
As I mainly use Libby for audiobooks this tool is focused on that. 
If you want to download ebooks your best bet is to try the "ebook-epub-adobe"-format
and use something like [Knock](https://web.archive.org/web/20221016154220/https://github.com/BentonEdmondson/knock).
Unfortunately it was removed from GitHub, but you can still download it [here](https://web.archive.org/web/20221020182238/https://github.com/BentonEdmondson/knock/releases).
Most other formats will just print out a link you can open in your browser.

This tool has only been tested on Linux and macOS (thanks [dhnyny](https://github.com/dhnyny)).

You can try --timeout and --retry if you're having connection issues.

## Info
* There's a swagger API with documentation [here](https://thunder-api.overdrive.com/docs/ui/index), but I couldn't get everything to work.
* "ebook-overdrive"-format (Libby web reader) is mostly a regular epub. The book is base64encoded in .xhtml files which we can get. I think most of the toc.ncx file can be reconstructed from openbook.json. Every book could in theory be downloaded this way, then we wouldn't need to bother with acsm's and so on.
* "ebook-kobo"-format is often/always listed as available even if it isn't...? I don't have a device I can test with and I don't know how it works.
* You can still get an ODM file by using ```-odm```


## Thanks to
* Overdrive for their service.
* The Norwegian libraries that are a part of Overdrive.
* [Naleo Hyde](https://github.com/naleo/)
* [ping](https://github.com/ping/)


## Legal
This program is not authorized by Overdrive/Libby. It does not intentionally circumvent any 
restrictions in Overdrive's or Libby's services, 
but instead works in the same way as their own software. 
This means that you will need a valid library card and also a license for 
each book you download (you need to have "borrowed" them). 
PyLibby does not remove DRM from files it downloads.


## License
Copyright © 2022 Raymond Olsen.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/

---
#### Donation
If this software was helpful to you, you may donate any amount here.  
Thank you!

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/donate?hosted_button_id=HCETPXTC7Y4GA)

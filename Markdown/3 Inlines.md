<a id=Emphasis></a>

# Emphasis

SSSSS _em HTML tag_ SSSSS

[//]: # (Equivalent)

SSSSS *em HTML tag* SSSSS

SSSSS \*em HTML tag\* SSSSS

SSSSS **strong HTML tag** SSSSS

[//]: # (Equivalent)

SSSSS __strong HTML tag__ SSSSS

SSSSS ~~x HTML tag~~ SSSSS

This is a `code text`

# Table

| 1   | 2   | 3   |
|-----|-----|-----|
| 4   | 5   | 6   |
| 7   | 8   | 9   |

# Links

## Same file Anchor

Go to Emphasis [Emphasis](#Emphasis).

## Local file Anchor

+ Use %20 to represent space into file name
+ Case sensitive
+ specify .md
+ To aim section, all minimise letter with - as space

[Link to local file](1%20Syntax.md) 1 Syntax.md

[Link to local file section](2%20Tags.md#bulleted-lists) 2 Tags.md#bulleted-lists

<!-- ##  [sub-section](./1 Syntax.md) -->

## Link url

This is the [Markdown](https://en.wikipedia.org/wiki/Markdown "Markdown Wikipedia")'s Wikipedia.

[This link](http://example.net/) has no title attribute.

# Link label

[//]: # (Anchors)

[foo1]: http://example.com/  "Optional Title"

[foo2]: <http://example.com/>  'Optional Title'

[foo3]: http://example.com/
(Optional Title)

[md_wiki]: https://en.wikipedia.org/wiki/Markdown  "Markdown Wikipedia"

[Google]: http://google.com/

[Google]: http://google.com/

[rplace_img]: rplace2022.webp

[rplace_url]: https://rplace-community.github.io/visualization/assets/img/loadingscreen/rplace_logo.png

* example.com [foo1 link][foo1]
* example.com [foo2 link][foo2]
* example.com [foo3 link][foo3]
* This is the [Markdown's Wikipedia][md_wiki]
* [Google][]

# Images

![rplace_url]

Image not founded ![Alt text](img.jpg "Optional title")

<img src="https://upload.wikimedia.org/wikipedia/en/0/01/RPlace2022.png" height="100" width="100" alt="rplace"/>

![rplace_img]


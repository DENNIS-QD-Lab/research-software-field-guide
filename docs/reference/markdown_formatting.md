# Markdown Formatting

Markdown is the text format used for `.md` files, GitHub PR descriptions, GitHub issue comments, and notebook markdown cells. This reference covers what you'll actually use.

To see markdown rendered in VS Code: right-click a `.md` file tab and choose "Open Preview," or press `Cmd+Shift+V` (Mac) / `Ctrl+Shift+V` (Windows). To make preview the default instead of toggling it every time, see [Markdown preview](../onboarding/02_using_vs_code.md#markdown-preview).

## Headers

````markdown
# Header 1 (the page title)
## Header 2
### Header 3
#### Header 4
````

Use `#` levels to create hierarchy, not for size. Skip levels sparingly: H1 → H2 → H3, not H1 → H3.

## Text emphasis

````markdown
*italic* or _italic_
**bold** or __bold__
***bold italic***
~~strikethrough~~
`inline code`
````

Use bold for emphasis on key terms. Use inline code for filenames, variable names, command names, and any text the reader will type literally.

## Lists

````markdown
- bullet
- another bullet
  - nested bullet (indent by 2 spaces)
  - another nested

1. numbered
2. numbered
3. numbered
````

Markdown auto-numbers, so `1. 1. 1.` renders as `1. 2. 3.`. This is helpful when reordering: you don't have to renumber.

## Links

````markdown
[link text](https://example.com)
[link to a file](path/to/file.md)
[link to a section in another file](path/to/file.md#section-header)
````

Section anchors are lowercased with hyphens replacing spaces: `## My Section` becomes `#my-section`.

## Images

````markdown
![alt text](path/to/image.png)
````

Same syntax as links but with a leading `!`. The alt text appears if the image fails to load and is read aloud by screen readers.

## Code blocks

Inline code uses backticks: `` `like this` ``.

Code blocks use triple backticks with an optional language for syntax highlighting:

````markdown
```python
def show_keys(path: str) -> None:
    with h5py.File(path, "r") as f:
        for key in f.keys():
            print(key)
```
````

Common language tags: `python`, `bash`, `yaml`, `json`, `markdown`. Use the language tag — GitHub and VS Code both colorize accordingly, which makes code far more readable.

## Block quotes

````markdown
> A quoted passage.
> Multi-line quotes use a `>` on every line.
````

Useful for quoting other docs, error messages, or example output. Also commonly used in PR descriptions to quote a previous comment when responding.

## Tables

````markdown
| Column A | Column B | Column C |
|---|---|---|
| value 1 | value 2 | value 3 |
| value 4 | value 5 | value 6 |
````

The separator row (`|---|---|---|`) is required. You can align columns with colons:

````markdown
| Left | Center | Right |
|:---|:---:|---:|
| a | b | c |
````

Tables are good for reference content (like keyboard shortcut tables) but cumbersome to maintain. For most prose, lists or paragraphs read better.

## Horizontal rule

````markdown
---
````

Three or more hyphens on their own line. Use sparingly to break a doc into major sections; headers are usually a better choice.

## Task lists (GitHub)

````markdown
- [ ] unchecked task
- [x] completed task
````

GitHub renders these as actual checkboxes you can click to toggle. Useful in PR descriptions and issues.

## Things markdown doesn't do well

**Two columns.** Markdown is single-column. If you need columns, you need HTML, and at that point you're probably better off using a different tool.

**Footnotes.** GitHub supports `[^1]` footnote syntax, but rendering is inconsistent across tools. Avoid for shared docs.

**Math.** GitHub renders LaTeX math between `$...$` (inline) or `$$...$$` (block). Some other tools don't. Test before relying on it.

**Comments in the source that won't render.** There's a trick using `[//]: # (this is a comment)`, but it's awkward. Easier to just not write things you don't want rendered.

## When in doubt

The fastest way to learn markdown is to write some and preview it. Start a scratch `.md` file, try a syntax, hit `Cmd+Shift+V` to see the result, adjust. You'll have it internalized in an afternoon.
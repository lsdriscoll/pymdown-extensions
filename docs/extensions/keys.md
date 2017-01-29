## Overview

Keys is an extension to make entering and styling keyboard key presses easier. Syntactically, Keys is built around the `+` symbol.  A key or combination of key presses is are surrounded by `++` with each key press separator with a single `+`.  For instance, if we wanted to represent `Ctrl + Alt + Delete`, we could just format our keys like this: `++ctrl+alt+delete++` --> ++ctrl+alt+delete++.

## Formatting

By default, Keys outputs keys in the form (separator `span`s will be omitted if a separator is not provided via the [options](#options)):

```html
<span class="keys">
  <kbd class="key-ctrl">Ctrl</kbd>
  <span>+</span>
  <kbd class="key-alt">Alt</kbd>
  <span>+</span>
  <kbd class="key-delete">Delete</kbd>
</span>
```

Notice the wrapper `span` as the class `keys` applied to it.  This is so you can target it or the elements under it. Each recognized key press has it's special key class assigned to it in the form `key-<key name>`. These individual key clases are great if you want to show special modifier key symbols before the key text (which is done in this documentation). The wrapper `keys` class can be customized with options, and the individual key classes are generated from the [key-map index](#key-map-index).

If you would like to generate a key which isn't in the key index, you can extend the key map via special a special [option](#extendingmodifying-key-map-index).  But if you don't need a key with a special class generated, or you need a way to quickly enter a one time special key, you can just insert it directly by quoting the text you want displayed instead of a key name: `++ctrl+alt+"My Special Key"++` --> ++ctrl+alt+"My Special Key"++. You can also enter HTML entities: `++ctrl+alt+"&Uuml;"++` --> ++ctrl+alt+"&Uuml;"++.

## Strict `KBD` Output

According to HTML5 spec on [`kbd`](https://dev.w3.org/html5/spec-preview/the-kbd-element.html), a literal key input, is represented by `kbd` wrapping the other `kbd`s:

```html
<kbd class="keys">
  <kbd class="key-ctrl">Ctrl</kbd>
  <span>+</span>
  <kbd class="key-alt">Alt</kbd>
  <span>+</span>
  <kbd class="key-delete">Delete</kbd>
</kbd>
```

This is not how many people use it, but if you are a stickler for rules, feel free to enable the `strict` option to enable a more "proper" format.

## Key-Map Index

By default, Keys provides a key-map index for English US keyboards. The key-map index is a dictionary that provides all supported key names (which are used as the class in output class `key-<name>`), with their corresponding display text.  There is also a separate alias dictionary which maps some aliases to entries in the key-map index.

### Keys

--8<-- "key-map.md"

### Key Aliases

--8<-- "key-aliases.md"

## Extending/Modifying Key-Map Index

If you want to add additional keys, or override text of existing keys, you can feed in your keys via the `key_map` option. The `key_map` parameter takes a simple dictionary with *key names* that are represented by lowercase alphanumeric characters and hyphens (`-`). The values of the dictionary represent the the text that is displayed for the key in the HTML output.

So if you wanted to add a custom key, you could do this: `#!py {"custom": "Custom Key"}`.  If you wanted to override the output of the `option` key and change it from `Option` to `Opt`, you could do this: `#!py {"option": "Opt"}`.

## Options

Option       | Type       | Default       | Description
------------ | ---------- | ------------- | -----------
`separator`  | string     | `#!py '+'`    | Define a separator.
`strict`     | bool       | `#!py False`  | Use strict HTML5 output for keyboard key input.
`class`      | string     | `#!py 'keys'` | Defines a class(es) to apply to the HTML wrapper element.
`camel_case` | bool       | `#!py False`  | Allow the use of camel case for key names `PgUp` --> `pg-up`.
`key_map`    | dictionary | `#!py {}`     | Add additional keys to the key-map index or override output of existing outputs. See [Extending/Modifying Key-Map Index](#extendingmodifying-key-map-index) for more info.

## Examples

```
To copy, press ++ctrl+alt+c++ for Windows or Linux or ++cmd+alt+c++ for OSX.
```

To copy, press ++ctrl+alt+c++ for Windows or Linux or ++cmd+alt+c++ for OSX.

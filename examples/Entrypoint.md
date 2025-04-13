# hi!

markdown headers and formatting work.

*italics*, **bold**, and even inline html for <sub>small text.</sub>


### Markup Documentation

most commands, outside of direct javascript injection are wrapped in

```
`$command args` (<------ replace the body here.)
```

on a line of its own.

```
target: 
  | node name
  | 'continue' (can have offset, e.g. continue+x or continue-x)
    - break to a new page and increment the next node
  | 'fallthrough' (can have offset)
    - target next node but don't instantly break the page here
```


commands

* `$link target [link text here]`
	* Create a link to a specified `target` -- see above on target definition.
* `$textentry target | [desired player text] | [Link text] | <optional: threshold>`
	* Shorthand for "make the player type the word" - threshold is for mistyping tolerance
* `$snap`
	* play snap sound effect on node entry
* `$debuff debuff_name [overrides]`
	* `debuff_name` - defined in `shared.ts` or anywhere else that writes to story state.
	* `overrides`: js object key-value pairs with no wrapping braces to override parts of the base debuff
* `$item item_name [overrides]`
	* same as debuff but for existing items
* `$fixed_roll stat value modifier`
	* stat, value, modifier are all strings - non-fixed roll (random at runtime) support hasn't been finished but works

javascript injection:
add a markdown codeblock with the language as `javascript` and it'll get flung at the top of the svelte component

`$link continue See more.`

as far as code block injection, it's how i handle things like buffs and sheet interactions. 


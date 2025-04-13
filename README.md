# storyrender

wip twine-like story engine.

halfway between something that's fit for only one purpose and generic. i'd love to make this more generic soon.

general workflow: 

each node or page is through ![mdsvex](https://mdsvex.pngwn.io/) and gets thrown in the story directory, included at compile time, and built into something fully static.

a preprocessor turns inline markdown commands into js scripts injected into the finalized mdsvex nodes. ideally this would be a build plugin but i have spent about a week with vite total.


```md
# hi!

markdown headers and formatting work.

*italics*, **bold**, and even inline html for <sub>small text.</sub>

`$link continue Next page.`

This is a new node.

Text goes here.

`$link fallthrough This target goes to the same place...`

`$link continue ...as the one below it.`

Other injected JS can be done in page, too, like setting the background.

hard to nest in documentation: use the below like a 'real' codeblock.

` ` `javascript
state.ui.background.spiralOpacity = 0.04;
state.character.stats.willpower = 0;
state.ui.theme = "awake";
` ` `

these fire on page load.

`$link continue Next page, and so on.`
```


test for building documentation: check `entrypoint.md` in `examples`

`$ ./svxPreprocessory.py ./examples ./src/lib/story && npm run dev`

publishing: `$ npm run build`


```
#!/bin/bash
cp -r ~/.obsidian/story_folder ./md_temp
rm ./src/lib/story/*
./svxPreprocessor.py ./story_folder ./src/lib/story
rm -r ./md_temp

cp ./src/lib/story-wrapper/* ./src/lib/story/
```
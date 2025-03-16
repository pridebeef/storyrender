#!/usr/bin/python

# this should really be a vite or svelte preprocessor plugin.
# text templating is a big "when you have a hammer..." 

# the end goal of this is just shorthand for pointing at a bunch of markdown in a folder
# and creating multiple svelte components out of one file, which seems tricky with the current setup.
# could be cleaned up, but, it's quick.

import os, sys

if len(sys.argv) != 3:
    print('usage: svxPreprocessor.py source_directory target_directory')
    sys.exit(0)

# not formatted - no {{ }} escapes!
IMPORT_BLOCK = """
<script>
    import TextboxLink from '../components/TextboxLink.svelte';
    import Link from '../components/Link.svelte';
    let { state = $bindable(), navigate } = $props();
</script>

"""

# scary quote escapes that map to {` inserted text `} to do inline js template strings
LINK_BLOCK = """
<Link 
    label={{`{}`}}
    bind:state 
    stateCallback={{(state) => navigate("{}")}} 
/>
"""

TEXT_ENTRY_BLOCK = """
<TextboxLink label={{`{}`}} goal={{`{}`}}>
    <Link 
        label={{`{}`}}
        bind:state 
        stateCallback={{(state) => navigate("{}")}} 
    />
</TextboxLink>
"""

source_files = os.listdir(sys.argv[1])
target_dir = sys.argv[2]
if len(os.listdir(target_dir)) != 0:
    print(f'warning: target dir is not empty. using {target_dir}_ ({os.listdir(target_dir)})') 
    #TODO: make folder
    target_dir = f'{target_dir}_'

for file in source_files:
    filepath = f"{sys.argv[1]}/{file}"
    filebase = '.'.join(file.split('.')[:-1])
    with open(filepath, 'r') as source:
        lines = source.readlines()
        if len(lines) < 1:
            print(f'info: empty file {filepath}')
            continue
        # not really a fan of file-by-file state just thrown around 
        # but this is a quick hack anyway
        transformed = '';
        if not lines[0].strip()[0:8].startswith('<script>'):
            print(f'info: adding default imports to {file}')
            transformed += IMPORT_BLOCK
        
        append = ''
        next_subfile = 1
        def write(outfile):
            # i hate this
            global transformed, append, next_subfile
            outfile.write(transformed)
            append = next_subfile 
            next_subfile += 1
            transformed = IMPORT_BLOCK

        within_codeblock = False 
        codeblock_contents = ''
        for line in lines:
            if within_codeblock:
                # inject lines / reset state on codeblock completion
                if line.strip().startswith('```'):
                    within_codeblock = False
                    transformed_lines = transformed.split('\n')
                    transformed_lines_stripped = list([l.strip() for l in transformed_lines])
                    close_tag = '</script>'
                    if close_tag not in transformed_lines_stripped:
                        print("error: no close script in processed lines. this shouldn't happen.")
                        sys.exit(1)
                    close_idx = transformed_lines_stripped.index(close_tag)
                    transformed_lines[close_idx:close_idx] = ['// begin inject'] + codeblock_contents.split('\n') ['// end inject']
                    transformed = '\n'.join(transformed_lines)
                    continue
                codeblock_contents += line 
                continue 
            if line.strip().startswith('`$') and line.strip().endswith('`'):
                command = line.strip()[2:-1]
                print(f'info: command: {command}')
                
                # syntax: `$link Story1 this is a link to Story1`
                # syntax: `$link continue The rest of the story continues under this header.`
                if command.startswith('link'):
                    target, text = command.split(' ', 2)[1:]
                    if target.strip() == 'continue':
                        transformed += LINK_BLOCK.format(text.strip(), f'{filebase}{next_subfile}.svx')
                        with open(f'{target_dir}/{filebase}{append}.svx', 'w') as outfile:
                            write(outfile)
                            continue
                    transformed += LINK_BLOCK.format(text.strip(), target)
                
                # syntax: `$textentry threshold | target | writing goal phrase | link text`
                # syntax: `$textentry target | writing goal phrase | link text`
                if command.startswith('textentry'):
                    body = command.split(' ', 1)[1]
                    args = body.split('|')
                    
                    if len(args) == 3:
                        threshold = None 
                        target, goal, text = args 
                    elif len(args) == 4:
                        threshold, target, goal, text = args
                    else: 
                        print(f'error: invalid $textentry: got {len(args)}, not 3 or 4: raw args: {args}')
                        sys.exit(1)
                    if target.strip() == 'continue':
                        transformed += TEXT_ENTRY_BLOCK.format(
                            goal.strip(), 
                            goal.strip(), 
                            text.strip(), 
                            f'{filebase}{next_subfile}.svx'
                        )
                        with open(f'{target_dir}/{filebase}{append}.svx', 'w') as outfile:
                            write(outfile)
                            continue
                    transformed += TEXT_ENTRY_BLOCK.format(
                        goal.strip(), 
                        goal.strip(), 
                        text.strip(), 
                        target.strip()
                    )
            # syntax: ```javascript {arbitrary content/newlines} ```
            # md codeblock for js dumped into import block header 
            elif line.strip().startswith('```javascript'):
                within_codeblock = True;
            else: 
                transformed += f'{line}'
        with open(f'{target_dir}/{filebase}{append}.svx', 'w') as outfile:
            write(outfile)

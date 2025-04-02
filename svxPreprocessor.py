#!/usr/bin/python

# this should really be a vite or svelte preprocessor plugin.
# text templating is a big "when you have a hammer..." 

# the end goal of this is just shorthand for pointing at a bunch of markdown in a folder
# and creating multiple svelte components out of one file, which seems tricky with the current setup.
# could be cleaned up, but, it's quick.

import os, sys, re

nodes = 0

if len(sys.argv) != 3:
    print('usage: svxPreprocessor.py source_directory target_directory')
    sys.exit(0)

# not formatted - no {{ }} escapes!
IMPORT_BLOCK = """
<script>
    import TextboxLink from '../components/TextboxLink.svelte';
    import Link from '../components/Link.svelte';
    import Debuff from '../components/Debuff.svelte';
    import Roll from '../components/Roll.svelte';
    import { debuffs, roll } from '../shared.ts';
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

# two interpolations: one for the shallow clone of base debuff 
# and the next for a string of ', override: value' pairs
DEBUFF_BLOCK = """
<Debuff
    debuff={{ {{ ...debuffs.{}{} }} }}
/>
"""

# not-actually-random at all
FIXED_ROLL_BLOCK = """
<Roll 
    roll={{roll('{}','{}','{}')}}
/>
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
            global transformed, append, next_subfile, nodes 
            nodes += 1
            outfile.write(transformed)
            append = next_subfile 
            next_subfile += 1
            transformed = IMPORT_BLOCK

        within_codeblock = False 
        codeblock_contents = ''
        for line in lines:
            # quotes are substituted with the asymmetrical quote characters
            # and since `` is a js template literal AND a markdown codeblock
            # we want the final output to be \`text\` which requires escaping the slash.
            line = re.sub(
                r'%([A-Z][a-z0-9]+)', 
                r'{ state.replace(state, \\`\1\\`, [\\`capitalize\\`]) }', 
                line
            )
            line = re.sub(
                r'%([A-Z0-9]+)', 
                r'{ state.replace(state, \\`\1\\`, [\\`uppercase\\`]) }', 
                line
            )
            line = re.sub(
                r'%([a-z0-9]+)', 
                r'{ state.replace(state, \\`\1\\`, [\\`lowercase\\`]) }', 
                line
            )

            # pre-parse hook for ignoring internal code to gather (stateful)
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
                    transformed_lines[close_idx:close_idx] = ['// begin inject'] + codeblock_contents.split('\n') + ['// end inject']
                    transformed = '\n'.join(transformed_lines)
                    continue
                codeblock_contents += line 
                continue 
            
            # command parsing
            if line.strip().startswith('`$') and line.strip().endswith('`'):
                command = line.strip()[2:-1]
                print(f'info: command: {command}')
                
                # syntax: `$link Story1 this is a link to Story1`
                # syntax: `$link continue The rest of the story continues under this header.`
                # syntax: `$link fallthrough continue without making a new page!`
                # syntax: `$link fallthrough+2 continue without making a new page!`
                # syntax: `$link continue+2 skip two sections here!`
                if command.startswith('link'):
                    target, text = command.split(' ', 2)[1:]
                    if target.strip().startswith('fallthrough'):
                        args = target.strip().split('+')
                        if len(args) > 1:
                            offset = args[1]
                            transformed += LINK_BLOCK.format(text.strip(), f'{filebase}{int(next_subfile) + int(offset)}.svx')
                            continue
                        args = target.strip().split('-')
                        if len(args) > 1:
                            offset = args[1]
                            story_index = int(next_subfile) - int(offset)
                            story_index = str(story_index) if story_index > 0 else ''
                            transformed += LINK_BLOCK.format(text.strip(), f'{filebase}{story_index}.svx')
                            continue
                        transformed += LINK_BLOCK.format(text.strip(), f'{filebase}{next_subfile}.svx')
                        continue
                    if target.strip().startswith('continue'):
                        args_p = target.strip().split('+')
                        if len(args_p) > 1: 
                            offset = args_p[1]
                            transformed += LINK_BLOCK.format(text.strip(), f'{filebase}{int(next_subfile) + int(offset)}.svx')
                        args_m = target.strip().split('-')
                        if len(args_m) > 1: 
                            offset = args_m[1]
                            story_index = int(next_subfile) - int(offset)
                            story_index = str(story_index) if story_index > 0 else ''
                            transformed += LINK_BLOCK.format(text.strip(), f'{filebase}{story_index}.svx')
                        if len(args_p) == 1 and len(args_m) == 1:
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

                # syntax: `$debuff base {js object key value pairs}`
                if command.startswith('debuff'):
                    print(f'info: command: {command}')
                    base = command.split(' ')[1].strip()
                    optargs = command.split(' ', 2)[1:]
                    optargs = f", {optargs[1]}" if len(optargs) != 1 else ''
                    transformed += DEBUFF_BLOCK.format(
                        base,
                        optargs
                    )

                # syntax: `$fixed_roll roll_stat value modifier`
                if command.startswith('fixed_roll'):
                    print(f'info: command: {command}')
                    roll, value, modifier = [part.strip() for part in command.split(' ', 4)[1:]]
                    transformed += FIXED_ROLL_BLOCK.format(roll, value, modifier)

            # syntax: ```javascript {arbitrary content/newlines} ```
            # md codeblock for js dumped into import block header 
            elif line.strip().startswith('```javascript'):
                within_codeblock = True;
            else: 
                transformed += f'{line}'
        with open(f'{target_dir}/{filebase}{append}.svx', 'w') as outfile:
            write(outfile)

print(f"{nodes} nodes created.")
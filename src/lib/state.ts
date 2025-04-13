import { debuffs, type DebuffType, type ItemType } from "./shared";

// a lot of this should probably be in the form of 
// classes rather than types + a default to splat/copy construct
// in order to be idiomatic but i didn't take the time in my single day of reading svelte 5 docs
// to realize classes weren't reactive out of the box so i lazily just left this as-is

export type InterfaceView = 'read' | 'inventory' | 'characterSheet';

export type InterfaceTheme = 'in-story' | 'awake' | 'awake-spiral' | 'blurred';

type AudioContainer = { [audioName in string]: HTMLAudioElement };

export type InterfaceAudio = {
    muted: boolean;
    tracks: AudioContainer;
    oneshots: AudioContainer;
    register_oneshot: (o: AudioContainer, name: string, file: string) => void;
    play_oneshot: (mute: boolean, o: AudioContainer, name: string) => void;
}

export const DefaultInterfaceAudio: InterfaceAudio = {
    muted: false,
    tracks: {},
    oneshots: {},
    register_oneshot(o: { [audioName in string]: HTMLAudioElement }, name: string, file: string) {
        o[name] = new Audio(file);
    },
    play_oneshot(mute: boolean, o: { [audioName in string]: HTMLAudioElement }, name: string) {
        if (mute) return;
        o[name].currentTime = 0;
        o[name].play();
    }
}

export type InterfaceState = {
    view: InterfaceView;
    audio: InterfaceAudio;
    background: {
        spiralOpacity: number;
    };
    theme: InterfaceTheme;
};

const DefaultInterfaceState: InterfaceState = {
    view: 'read',
    background: {
        spiralOpacity: 0.0
    },
    audio: { ...DefaultInterfaceAudio },
    theme: 'in-story'
};

export type EditableField = "willpower" | "class"

export type Character = {
    name: string,
    pronouns: 'he' | 'she' | 'they',
    stats: { [key in string]: number }
    class: { name: string, level: number }[]
    health: {
        current: number,
        max: number
    }
    // these should be lists but onMount rerender adds the item/buff again.
    // tomorrow's problem!
    buffs: { [key in string]: DebuffType }
    other: { [key in string]: number | string | object }
    unlockEditable: { [key in EditableField]?: boolean }
    inventory: { [key in string]: ItemType }
}

export type ReplaceFlags = "lowercase" | "capitalize" | "uppercase"

export type StoryState = {
    character: Character,
    currentPage: string,
    ui: InterfaceState,
    dictionary: { [key in string]: object | string }
    replace: (state: StoryState, target: string, flags: ReplaceFlags[]) => string
};

const DefaultDictionary = {
    pronouns: {
        // default m-form -> lookup by character selection
        'he': {
            'he': 'he',
            'she': 'she',
            'they': 'they'
        },
        'him': {
            'he': 'him',
            'she': 'her',
            'they': 'them'
        },
        'his': {
            'he': 'his',
            'she': 'her',
            'they': 'their'
        },
        'hes': {
            'he': "he's",
            'she': "she's",
            'they': "they're"
        }
    },
    diminutive: {
        'he': 'boy',
        'she': 'girl',
        'they': 'toy'
    }
}

export const DefaultStoryState: StoryState = {
    character: {
        name: 'name',
        pronouns: 'he',
        stats: {
            'strength': 16,
            'dexterity': 12,
            'constitution': 16,
            'willpower': 14,
            'intelligence': 12,
            'charisma': 16
        },
        class: [
            {
                name: 'paladin',
                level: 5
            }
        ],
        health: {
            max: 27,
            current: 27,
        },
        buffs: {},
        other: {},
        unlockEditable: {},
        inventory: {}
    },
    currentPage: "Entrypoint",
    ui: { ...DefaultInterfaceState },
    dictionary: { ...DefaultDictionary },
    replace: (state, t, flags) => {
        const target = t.toLowerCase().trim();

        let replacement = "";
        if (target === 'name') {
            replacement = state.character.name
        }
        if (target === (state.dictionary.diminutive as any)['he']) {
            replacement = (state.dictionary.diminutive as any)[state.character.pronouns]
        }
        const pronounTargets = ['he', 'him', 'his', 'hes'];
        if (pronounTargets.includes(target)) {
            replacement = (state.dictionary.pronouns as any)[target][state.character.pronouns]
        }

        if (replacement === "") {
            replacement = state.dictionary[target] as string;
        }

        if (flags.includes('lowercase')) {
            replacement = replacement.toLowerCase();
        } else if (flags.includes('uppercase')) {
            replacement = replacement.toUpperCase();
        } else if (flags.includes('capitalize')) {
            replacement = replacement[0].toUpperCase() + replacement.slice(1);
        }

        return replacement;
    }
}
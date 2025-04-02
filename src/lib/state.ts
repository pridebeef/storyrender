import { debuffs, type DebuffType } from "./shared";

export type InterfaceView = 'read' | 'inventory' | 'characterSheet';

export type InterfaceState = {
    view: InterfaceView;
    audioTrack?: undefined;
    background: {
        spiralOpacity: number;
    };
    theme?: undefined;
};

const DefaultInterfaceState: InterfaceState = {
    view: 'read',
    background: {
        spiralOpacity: 0.0
    }
};

export type Character = {
    name: string,
    pronouns: 'he' | 'she' | 'they',
    stats: { [key in string]: number },
    class: { name: string, level: number }[]
    health: {
        current: number,
        max: number
    }
    buffs: DebuffType[]
    other: { [key in string]: number | string | object }
}

export type ReplaceFlags = "lowercase" | "capitalize" | "uppercase"

export type StoryState = {
    progression: {
        characterSheet: boolean,
        inventory: boolean
    },
    character: Character,
    characterFlags: {
        [key in string]: number | string | object
    },
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
        }
    },
    diminutive: {
        'he': 'boy',
        'she': 'girl',
        'they': 'toy'
    }
}

export const DefaultStoryState: StoryState = {
    progression: {
        characterSheet: false,
        inventory: false,
    },
    character: {
        name: 'myname',
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
        buffs: [
            { ...debuffs.test }
        ],
        other: {}
    },
    characterFlags: {},
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
        const pronounTargets = ['he', 'him', 'his'];
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
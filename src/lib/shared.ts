import { Backpack, Circle, Icon as IconType, Shell } from 'lucide-svelte';

export type RollType = {
    name: string,
    modifier: string,
    value: string
    color: string,
}

export const defaultRoll = { color: '#e6e6e6' }
export const roll = (name: string, value: string, modifier: string) => ({
    ...defaultRoll,
    name,
    modifier,
    value,
})

export type DebuffType = {
    name: string;
    duration: string;
    description: string;
    icon: typeof IconType;
    color: string;
};

export const debuffs: { [key in string]: DebuffType } = {
    hypnotized: {
        name: "Hypnotized",
        duration: "3 hours",
        color: "#ff00ff",
        icon: Shell,
        description: "Treat statements from the target as if they were true."
    },
    brainwashed: {
        name: "Brainwashed",
        duration: "indefinite",
        description: "You've been under so many times you've allowed him to leave suggestions indistinguishable from your thoughts. Your purpose is to serve him. This is who you are now.",
        color: "#990099",
        icon: Shell
    }
}

export type ItemType = {
    name: string;
    description: string;
    icon: typeof IconType;
    color: string;
}

export const items: { [key in string]: ItemType } = {
    stuff: {
        name: "Everyone's Stuff",
        color: "#ffffff",
        description: "Be a good servant and carry it for us, will you?",
        icon: Backpack,
    },
    bag: {
        name: "Marath's Bag",
        color: "#31384d",
        icon: Backpack,
        description: "Thanks a ton, thrall! I could get used to this.~"
    },
    collar: {
        name: "Collar",
        color: "#ffffff",
        description: "It looks so good on you!",
        icon: Circle,
    }
}
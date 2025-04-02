import { Icon as IconType, Shell } from 'lucide-svelte';

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
    }
}
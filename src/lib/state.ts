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

export type StoryState = {
    progression: {
        characterSheet: boolean,
        inventory: boolean
    },
    characterSheet: {
        [key in string]: number | string | object
    },
    characterFlags: {
        [key in string]: number | string | object
    },
    currentPage: string,
    ui: InterfaceState
};

export const DefaultStoryState: StoryState = {
    progression: {
        characterSheet: false,
        inventory: false,
    },
    characterSheet: {},
    characterFlags: {},
    currentPage: "Entrypoint",
    ui: { ...DefaultInterfaceState }
}
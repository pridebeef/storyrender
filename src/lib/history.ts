import { type StoryState } from './state'

export type HistoryActionType = 'event' | 'marker';
export type HistoryAction = {
    type: HistoryActionType,
    state: StoryState
}
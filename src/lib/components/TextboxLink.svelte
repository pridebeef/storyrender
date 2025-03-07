<script lang="ts">
	import type { StoryState } from '$lib/state';
	import { tick, type Snippet } from 'svelte';
	import Link from './Link.svelte';

	let {
		target,
		label,
		goal,
		linkType = 'page',
		// guessing at this for "feel"
		threshold = 3,
		stateCallback = (_) => {},
		storyState = $bindable(),
		children
	}: {
		target: string;
		label: string;
		goal: string;
		linkType: string;
		threshold: number;
		stateCallback?: (_: object) => void;
		storyState?: StoryState;
		children?: Snippet;
	} = $props();

	// https://www.30secondsofcode.org/js/s/levenshtein-distance/
	const levenshteinDistance = (s: string, t: string) => {
		if (!s.length) return t.length;
		if (!t.length) return s.length;
		const arr = [];
		for (let i = 0; i <= t.length; i++) {
			arr[i] = [i];
			for (let j = 1; j <= s.length; j++) {
				arr[i][j] =
					i === 0
						? j
						: Math.min(
								arr[i - 1][j] + 1,
								arr[i][j - 1] + 1,
								arr[i - 1][j - 1] + (s[j - 1] === t[i - 1] ? 0 : 1)
							);
			}
		}
		return arr[t.length][s.length];
	};

	let value = $state('');

	const ld = (s: string, t: string, threshold: number) =>
		levenshteinDistance(
			s.replace(/[^A-Za-z0-9]/g, '').toLowerCase(),
			t.replace(/[^A-Za-z0-9]/g, '').toLowerCase()
		) < threshold;

	$effect(() => {
		if (ld(value, goal, threshold)) {
			// we probably revealed stuff, show it
			tick().then(() => {
				document.querySelector('.content')?.scrollBy(0, 200);
			});
			if (stateCallback !== undefined && storyState !== undefined) {
				console.error('shouldn.');
				stateCallback(storyState);
			}
		}
	});
</script>

<div class="textbox-link">
	<input bind:value placeholder={label} />
	{#if ld(value, goal, threshold)}
		{@render children?.()}
	{/if}
</div>

<style>
	.textbox-link {
		display: flex;
		flex-direction: column;
		input {
			margin-bottom: calc(1ex / 0.36);
			font-size: 1em;
			background-color: var(--bg-1);
			border: 1px solid var(--bg-3);
			color: var(--fg);
		}
	}
</style>

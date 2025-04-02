<script lang="ts">
	import type { StoryState } from '$lib/state';
	import { tick } from 'svelte';

	const pages = Object.fromEntries(
		Object.entries(import.meta.glob('../story/*.svx', { eager: true })).map(([path, component]) => [
			path.split('/').pop(),
			component
		])
	);
	let {
		storyState = $bindable(),
		navigate
	}: { storyState: StoryState; navigate: (page: string) => void } = $props();
	const pageName = $derived(
		storyState.currentPage.endsWith('.svx')
			? storyState.currentPage
			: `${storyState.currentPage}.svx`
	);

	let opacity = $state(1);
	const Page = $derived((pages?.[pageName] ? pages?.[pageName] : pages?.['Error.svx'])?.default);
	$effect(() => {
		Page;
		opacity = 0;
		tick().then(() => {
			opacity = 1;
			document.querySelector('.content')?.scroll(0, 0);
		});
	});
</script>

<div class={{ 'reading-body': true, 'opacity-curve': opacity > 0 }} style="opacity: {opacity};">
	<Page bind:state={storyState} {navigate} />
</div>

<style>
	:global(.opacity-curve) {
		transition: opacity ease-in 0.15s;
	}
	:global(.reading-body) {
		z-index: 2;

		font-size: 1.2rem;
		margin: auto;
		margin-top: 0px;
		padding-left: 1em;
		padding-right: 1em;
		display: flex;
		flex-direction: column;

		max-width: 70ch;
		width: 100%;
		:global(p) {
			line-height: calc(1ex / 0.32);
			margin: 0 0 calc(1ex / 0.36) 0;

			text-align: justify;
			/* hyphens: auto; */
			:global(&:nth-child(1)) {
				margin-top: calc(1ex / 0.36);
			}
		}
		:global(blockquote) {
			border-left: 0.25em solid var(--bg-3);
			padding-left: 2em;
			margin: 0;
			max-width: calc(70ch - 2em);
			:global(p) {
				margin-top: 0;
				margin-bottom: 0;
			}
			margin-bottom: 1em;
		}
	}

	:global(span.fakelink) {
		text-decoration: underline;
		:global(&:hover) {
			color: rgb(255, 235, 200);
			cursor: pointer;
		}
		:global(&:active) {
			color: rgb(255, 165, 0);
		}
		color: rgb(255, 220, 155);
		margin-bottom: calc(1ex / 0.36);
	}
</style>

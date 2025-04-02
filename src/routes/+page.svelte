<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import { DefaultStoryState, type StoryState } from '$lib/state';
	import { type HistoryAction } from '$lib/history';
	import { ArrowRight, ArrowLeft, CircleUserRound, RotateCcw, NotepadText } from 'lucide-svelte';
	import { onMount, tick } from 'svelte';
	import { PocketShader } from '@braebo/pocket-shader';
	import ReaderView from '$lib/components/ReaderView.svelte';
	import CharacterSheetView from '$lib/components/CharacterSheetView.svelte';

	let storyState: StoryState = $state(DefaultStoryState);
	let history = $state([] as HistoryAction[]);
	let historyBack = $state(0);

	const navigate = (page: string) => {
		if (historyBack > 0) {
			history = history.slice(0, -(historyBack + 1));
			historyBack = 0;
		}
		history.push({
			type: 'event',
			state: $state.snapshot(storyState) as StoryState
		});
		storyState.currentPage = page;
	};

	const enableBack = $derived(history.filter((e) => e.type !== 'marker').length > historyBack);
	const enableForward = $derived(historyBack > 0);

	$inspect(history, historyBack);

	const back = () => {
		historyBack += 1;
		if (history[history.length - 1].type !== 'marker') {
			history.push({
				type: 'marker',
				state: $state.snapshot(storyState) as StoryState
			});
		}
		storyState = history.toReversed()[historyBack].state;
	};
	const forward = () => {
		historyBack -= 1;
		storyState = history.toReversed()[historyBack].state;
		if (historyBack === 0) {
			history.pop();
		}
	};
	const restart = () => {
		if (window.confirm('Are you sure you want to restart?')) {
			history = [];
			historyBack = 0;
			storyState = $state.snapshot(DefaultStoryState) as StoryState;
		}
	};

	onMount(() => {
		new PocketShader('#canvas-target', {
			fragment: `
				uniform float u_time;
				uniform vec2 u_resolution;
				const float pi = 3.141592654;

				const float a = 8.;
				const float b = 6.;
				const float c = 2.;
				const float d = 1.;

				in vec2 vUv;
				out vec4 color;

				void main() {
					vec2 p = (vUv.xy - 0.5) * (u_resolution * 0.001);
					float r = length(p);
    				float theta = atan(p.y, p.x);   

					color = vec4(a * cos(b * theta + c * pi * (b * r - d * u_time)));
				}
			`,
			autoStart: true
		});
	});
</script>

<div class="main-page">
	<div class="header">
		<div class="header-left">
			<Button icon={ArrowLeft} disabled={!enableBack} onclick={back} />
			<Button icon={ArrowRight} disabled={!enableForward} onclick={forward} />
			<Button icon={RotateCcw} disabled={false} onclick={restart} />
		</div>
		<div class="header-center">
			<h2>Tabletop</h2>
		</div>
		<div class="header-right">
			<Button
				icon={NotepadText}
				disabled={storyState.ui.view === 'read'}
				onclick={() => {
					storyState.ui.view = 'read';
				}}
			/>
			<Button
				icon={CircleUserRound}
				disabled={storyState.ui.view === 'characterSheet'}
				onclick={() => (storyState.ui.view = 'characterSheet')}
			/>
		</div>
	</div>
	<div class="content">
		{#if storyState.ui.view === 'read'}
			<ReaderView bind:storyState {navigate}></ReaderView>
		{:else if storyState.ui.view === 'characterSheet'}
			<CharacterSheetView bind:character={storyState.character}></CharacterSheetView>
		{/if}
	</div>
	<div class="footer"></div>
</div>
<div
	id="canvas-target"
	style="overflow: hide; opacity: {storyState.ui.background.spiralOpacity};"
></div>

<style>
	:global(:root) {
		--bg: hsl(0, 0%, 11%);
		--bg-1: hsl(0, 0%, 13%);
		--bg-3: hsl(0, 0%, 20%);
		--bg-4: hsl(0, 0%, 28%);
		--fg: hsl(0, 0%, 90%);
		--purple: rgb(144, 62, 174);
	}

	:global(body, html) {
		margin: 0;
		font-size: 16px;
	}

	:global(*) {
		box-sizing: border-box;
	}

	.content {
		display: flex;
		flex-direction: column;
		width: 100%;
		justify-content: flex-start;
	}

	.main-page {
		height: 100vh;
		background-color: var(--bg);
		color: var(--fg);
		display: flex;
		flex-direction: column;

		z-index: 0;
	}

	.header {
		display: flex;
		flex-direction: row;
		flex: 0 0 auto;
		height: 3em;
		background-color: var(--bg-1);
		border-bottom: 1px solid var(--bg-3);

		z-index: 2;

		margin: auto;
		width: 100%;
		justify-content: space-between;
		align-items: center;
		align-content: center;

		.header-left {
			display: flex;
			flex-direction: row;
			flex: 0 0 auto;
			margin: auto;
			margin-left: 0.25rem;

			justify-content: flex-start;
		}

		.header-center {
			margin: auto;
			flex: 1 1 auto;
			display: flex;
			h2 {
				margin: auto;
			}
		}

		.header-right {
			display: flex;

			flex-direction: row;
			margin: auto;
			flex: 0 0 auto;
			margin-right: 0.25rem;
			justify-content: flex-end;
		}
	}

	.content {
		flex: 1;
		overflow: auto;
	}

	#canvas-target {
		position: fixed !important;
		height: 100vh;
		width: 100vw;
		inset: 0px;
		z-index: 0;

		background-color: #ffa500;
		transition: opacity 1s linear;
	}
</style>

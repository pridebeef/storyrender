<script lang="ts">
	import { type RollType } from '$lib/shared';
	import { Dices } from 'lucide-svelte';

	const { roll }: { roll: RollType } = $props();
</script>

<div class="roll-wrapper" style="border-color: {roll.color};">
	<span class="roll-icon">
		<Dices size={32} color={roll.color} />
	</span>
	<div class="roll-contents">
		<span class="roll-title">
			<span class="roll-name">
				{roll.name ?? 'SKILL'}
			</span>
		</span>
		<span class="roll-value">
			<span class="roll-main">
				{roll.value ?? '21'}
			</span>
			<span class="roll-modifier">
				({roll.modifier ?? '+3'})
			</span>
		</span>
	</div>
</div>

<style>
	.roll-wrapper {
		display: flex;
		padding: 0.5rem;
		border: 2px solid;
		border-radius: 8px;
		flex-direction: row;
		width: fit-content;
		margin-bottom: calc(1ex / 0.32);
	}

	.roll-icon {
		margin: auto 0.5rem auto 0rem;
		:global(.lucide-icon) {
			margin: auto;
		}
	}

	.roll-contents {
		display: flex;
		flex-direction: column;
	}

	.roll-value {
		display: flex;
		flex-direction: row;
		gap: 0.25rem;
		justify-content: flex-start;
	}

	.roll-title {
		display: flex;
		flex-direction: row;
	}

	.roll-main {
		font-size: 1.5rem;
		font-weight: 600;
	}

	.roll-modifier {
		margin: auto 0;
		font-size: 0.9rem;
		color: hsl(0, 0%, 80%);
	}

	.roll-name {
		text-transform: uppercase;
		font-weight: 600;
		font-size: 0.9rem;
		color: hsl(0, 0%, 80%);
	}
</style>

<script lang="ts">
	import type { Character, EditableField } from '$lib/state';
	import { Heart } from 'lucide-svelte';
	import Debuff from './Debuff.svelte';
	import Item from './Item.svelte';

	let { character = $bindable() as Character } = $props();
</script>

<div class="sheet-view">
	<div class="sheet-wrapper">
		<div class="sheet-current">
			<div class="sheet-title">
				<span>
					<span class="sheet-title-header"> Name </span>
					<span class="sheet-horiz-mini"></span>
					<input type="text" bind:value={character.name} class="name" />
				</span>
				<span class="sheet-vert"></span>
				<span>
					<span class="sheet-title-header">Species</span>
					<span class="sheet-horiz-mini"></span>

					<input type="text" bind:value={character.species} class="name" />
				</span>
				<span class="sheet-vert"></span>
				<span>
					<span>Classes</span>
					<span class="sheet-horiz-mini"></span>
					<span class="classes">
						{#each character.class as { name, level }}
							<span>{name} ({level})</span>
						{/each}
					</span>
				</span>
			</div>
		</div>
		<div class="sheet-stats">
			{#each Object.entries(character.stats) as [name, value]}
				<div class="sheet-stat">
					<span class="sheet-label">
						{name}
					</span>
					{#if character.unlockEditable?.[name as EditableField]}
						<input
							type="text"
							bind:value={character.stats[name]}
							class="sheet-stat-value input-stat-value"
						/>
					{:else}
						<span class="sheet-stat-value">
							{value}
						</span>
					{/if}
				</div>
			{/each}
		</div>
		<div class="sheet-horiz"></div>
		<div class="sheet-health">
			<span class="sheet-label sheet-health-label"> HEALTH </span>
			<div>
				<Heart></Heart>
				<span class="sheet-health-current">{character.health.current}</span>
				<span class="sheet-health-divider"> / </span>
				<span class="sheet-health-max">{character.health.max}</span>
			</div>
		</div>
		<div class="sheet-horiz"></div>
		<span class="subheader">Status</span>
		<div class="sheet-debuffs">
			{#each Object.entries(character.buffs) as [name, value]}
				<Debuff debuff={value}></Debuff>
			{/each}
			{#if Object.keys(character.buffs).length === 0}
				<span>Everything's perfectly normal.</span>
			{/if}
		</div>
		<div class="sheet-horiz"></div>
		<span class="subheader">Inventory</span>
		<div class="sheet-inventory">
			{#each Object.entries(character.inventory) as [name, value]}
				<Item item={value}></Item>
			{/each}
			{#if Object.keys(character.buffs).length === 0}
				<span>Emptyhanded, except for your usual gear.</span>
			{/if}
		</div>
	</div>
</div>

<style>
	input[type='text'] {
		height: 50px;
		-webkit-appearance: none;
		appearance: none;
		margin: 18px 0;
		width: 200px;

		color: var(--fg);
		background-color: var(--bg-1);

		border: 1px solid var(--bg-3);
		outline: none;
		box-shadow: none;
		&.input-stat-value {
			margin: 0px;
			width: 50px;
			height: 2rem;
			border: 1px solid rgb(255, 220, 155);
			:global(&:hover) {
				border: 1px solid rgb(255, 235, 200);
			}
			:global(&:active) {
				border: 1px solid rgb(255, 165, 0);
			}
		}
	}

	.sheet-title {
		text-transform: uppercase;
		font-weight: 500;
		margin-bottom: 1.5rem;
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		.name {
			font-size: 1.5rem;
			color: hsl(0, 0%, 90%);
		}
		.divider {
			font-size: 1.5rem;
			color: hsl(0, 0%, 50%);
		}
		> span {
			/*margin: auto 0;*/
			display: flex;
			flex-direction: column;
			gap: 0rem;
			input {
				margin-bottom: 0;
				margin-top: 0;
			}
		}
		flex-wrap: wrap;
	}

	.classes {
		display: flex;
		flex-direction: column;
		gap: 0.2rem;
		input {
			margin-bottom: 0;
			margin-top: 0;
		}
	}

	.subheader {
		text-transform: uppercase;
		font-weight: 500;
		margin-bottom: 1.5rem;
	}

	.sheet-view {
		margin-top: 1rem;
		z-index: 2;
	}

	.sheet-wrapper {
		font-size: 1.2rem;
		display: flex;
		flex-direction: column;
		margin: auto;
		width: calc(100% - 4rem);
		max-width: 70ch;

		border-radius: 8px;
		border: 2px solid var(--bg-4);
		padding: 2rem;
	}

	.sheet-stats {
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		justify-content: space-between;
		gap: 0.4rem;
	}
	.sheet-stat {
		display: flex;
		flex-direction: column;
		border-radius: 8px;
		border: 2px solid var(--bg-3);
		padding: 0.5rem;
		flex: 1 1;
	}
	.sheet-label {
		text-transform: uppercase;
		font-weight: 500;
		font-size: 0.9rem;
		color: hsl(0, 0%, 80%);
	}
	.sheet-stat-value {
		font-weight: 700;
		font-size: 1.3rem;
	}

	.sheet-horiz {
		height: 2px;
		background-color: var(--bg-1);
		border-radius: 8px;
		margin: 1rem 0rem;
	}

	.sheet-horiz-mini {
		height: 2px;
		background-color: var(--bg-1);
		border-radius: 8px;
		margin: 0.4rem 0rem;
	}

	.sheet-health {
		display: flex;
		flex-direction: column;
		border-radius: 8px;
		border: 2px solid var(--bg-3);
		padding: 0.5rem;
		width: fit-content;
	}
	.sheet-health-label {
		font-size: 1.1rem;
		margin-bottom: 0.25rem;
		margin-top: 0rem;
	}
	.sheet-health div {
		display: flex;
		flex-direction: row;
		justify-content: flex-start;
		align-items: center;
		gap: 0.4rem;
		> * {
			margin: auto unset;
		}
		> span {
			font-size: 1.4rem;
			&.sheet-health-current {
				font-weight: 700;
			}
		}
	}
</style>

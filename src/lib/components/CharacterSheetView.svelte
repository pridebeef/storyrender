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
				<span class="name">{character.name}</span>
				<span class="divider">|</span>
				<span class="species">species</span>
				<span class="divider">|</span>
				<span class="classes">
					{#each character.class as { name, level }}
						<span>{name} ({level})</span>
					{/each}
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
						<input bind:value={character.stats[name]} class="sheet-stat-value" />
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
			margin: auto 0;
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

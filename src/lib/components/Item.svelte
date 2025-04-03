<script lang="ts">
	import { type ItemType } from '$lib/shared';

	const { item }: { item: ItemType } = $props();

	const Icon = item.icon;
</script>

<div class="item-wrapper" style="border-color: {item.color};">
	<span class="item-icon">
		<Icon size={32} color={item.color} />
	</span>
	<div class="item-contents">
		<span class="item-title">
			<span class="item-name">
				{item.name ?? 'item name'}
			</span>
		</span>
		<span class="item-description">
			{item.description ?? 'Fill this out!'}
		</span>
	</div>
</div>

<style>
	.item-wrapper {
		display: flex;
		padding: 0.5rem;
		border: 2px solid;
		border-radius: 8px;
		flex-direction: row;
		margin-bottom: calc(1ex / 0.32);
		width: fit-content;
	}

	.item-icon {
		margin: auto 0.5rem auto 0;
		display: flex;
		:global(.lucide-icon) {
			margin: auto;
		}
	}

	.item-contents {
		display: flex;
		flex-direction: column;
	}

	.item-title {
		display: flex;
		flex-direction: row;
		gap: 0.25rem;
		align-items: center;
	}

	.item-name {
		text-transform: uppercase;
		font-weight: 500;
		font-size: 1rem;
		color: hsl(0, 0%, 90%);
		margin-right: 0.5rem;
	}

	.item-description {
		font-style: italic;
	}
</style>

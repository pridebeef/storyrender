<script lang="ts">
	import { type DebuffType } from '$lib/shared';

	const { debuff }: { debuff: DebuffType } = $props();

	const Icon = debuff.icon;
</script>

<div class="debuff-wrapper" style="border-color: {debuff.color};">
	<span class="debuff-icon">
		<Icon size={32} color={debuff.color} />
	</span>
	<div class="debuff-contents">
		<span class="debuff-title">
			<span class="debuff-name">
				{debuff.name ?? 'Debuff name'}
			</span>
			<span class="debuff-details">
				({debuff.duration ?? '?? turns'})
			</span>
		</span>
		<span class="debuff-description">
			{debuff.description ?? 'Fill this out!'}
		</span>
	</div>
</div>

<style>
	.debuff-wrapper {
		display: flex;
		padding: 0.5rem;
		border: 2px solid;
		border-radius: 8px;
		flex-direction: row;
		margin-bottom: calc(1ex / 0.32);
		width: fit-content;
	}

	.debuff-icon {
		margin: auto 0.5rem auto 0;
		display: flex;
		:global(.lucide-icon) {
			margin: auto;
		}
	}

	.debuff-contents {
		display: flex;
		flex-direction: column;
	}

	.debuff-title {
		display: flex;
		flex-direction: row;
		gap: 0.25rem;
		align-items: center;
	}

	.debuff-details {
		margin: auto auto auto 0;
		font-size: 0.9rem;
		color: hsl(0, 0%, 80%);
	}

	.debuff-name {
		text-transform: uppercase;
		font-weight: 500;
		font-size: 1rem;
		color: hsl(0, 0%, 90%);
		margin-right: 0.5rem;
	}

	.debuff-description {
		font-style: italic;
	}
</style>

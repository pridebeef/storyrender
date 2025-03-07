<script lang="ts">
	const {
		onclick = undefined,
		icon = undefined,
		label = '',
		tooltip = '',
		disabled = false
	} = $props();
	const iconOnly = $derived(label === '' && icon !== undefined);
</script>

<button
	class={{
		'icon-button': true,
		'icon-only': iconOnly,
		'icon-button-enabled': !disabled,
		'icon-button-disabled': disabled
	}}
	onclick={disabled ? () => {} : onclick}
	aria-label="label"
>
	{#if icon !== undefined}
		{@const Icon = icon}
		<Icon class="button-icon" />
	{/if}
</button>

<style>
	.icon-button {
		border: none;
		background-color: var(--bg-1);
		outline: solid 2px var(--bg-3);
		border-radius: 4px;
		aspect-ratio: 1/1;
		padding: 4px;
		display: flex;
		margin: 0 0.25rem 0 0.25rem;
	}

	.icon-button-enabled {
		&:hover {
			outline-color: var(--bg-4);
		}
		&:active {
			outline-color: var(--bg-0);
		}
		color: var(--fg);
	}

	.icon-button-disabled {
		color: var(--bg-4);
		outline: solid 2px var(--bg-1);
	}
</style>

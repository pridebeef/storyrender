<script lang="ts">
	let {
		target,
		label,
		linkType = 'page',
		stateCallback = undefined,
		altStyle = undefined,
		storyState = $bindable()
	} = $props();
</script>

<span
	class="fakelink {altStyle !== undefined ? `fakelink-${altStyle}` : ''}"
	onclick={() => {
		stateCallback(storyState);
	}}
	onkeydown={() => {
		stateCallback(storyState);
	}}
	role="link"
	tabindex="0"
>
	{label}
</span>

<style>
	.fakelink {
		text-decoration: underline;
		&:hover {
			color: var(--orange-3);
			cursor: pointer;
		}
		&:active {
			color: var(--orange1);
		}
		color: var(--orange2);
		margin-bottom: calc(1ex / 0.36);
	}
	span.fakelink-b {
		&:hover {
			color: var(--steel-3);
			cursor: pointer;
		}
		&:active {
			color: var(--steel1);
		}
		color: var(--steel2);
	}
</style>

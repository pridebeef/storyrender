<script lang="ts">
	let {
		target,
		label,
		linkType = 'page',
		stateCallback = undefined,
		storyState = $bindable()
	} = $props();
</script>

<span
	class="fakelink"
	onclick={() => {
		stateCallback(storyState);
	}}>{label}</span
>

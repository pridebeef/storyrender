<script lang="ts">
</script>

<div class="sheet-view">
	<div class="sheet-header"></div>
	<div class="sheet-current">
		<h4>Character Sheet</h4>
		<span>Level 5 Paladin</span>
	</div>
	<div class="sheet-stats"></div>
	<div class="sheet-debuffs"></div>
	<div class="sheet-inventory"></div>
</div>

<style>
	h4 {
		font-weight: 500;
	}

	.sheet-view {
		z-index: 2;

		font-size: 1.2rem;
		margin: auto;
		margin-top: 0px;
		padding-left: 1em;
		padding-right: 1em;
		display: flex;
		flex-direction: column;
		:global(p) {
			line-height: calc(1ex / 0.32);
			margin: 0 0 calc(1ex / 0.36) 0;

			max-width: 60ch;
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
			max-width: calc(60ch - 2em);
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

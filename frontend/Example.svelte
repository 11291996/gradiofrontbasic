<!-- value that will be displayed-->
<!-- type will select gallery or table-->
<!-- selected will adjust example when the users selects other input for defined example-->
<!-- samples_dir will lead to the server directory input-->
<!-- index shows the index of the selected value-->
<script lang="ts">
	export let value: string;
	export let type: "gallery" | "table";
	export let selected = false;
</script>

<div
	class:table={type === "table"}
	class:gallery={type === "gallery"}
	class:selected
>
	{value}
</div>

<style>
	.gallery {
		padding: var(--size-1) var(--size-2);
	}
</style>

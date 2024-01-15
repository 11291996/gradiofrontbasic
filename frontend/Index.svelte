<svelte:options accessors={true} />

<!-- elem_id and elem_classes allow other users to style the component -->
<!-- scale and min_width allow others to control spacing of the component-->
<!-- loading status allow displayment of the output-->
<!-- mode will define the default would interactive or not-->
<!-- use gradio to dispatch events explained in test_components.py in backend-->

<script lang="ts">
	import type { LoadingStatus } from "@gradio/statustracker";
    import { Block } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { Gradio } from "@gradio/utils";
	
	export let gradio: Gradio<{
		event_1: never;
		event_2: never;
	}>;

    export let value = "";
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus | undefined = undefined;
    export let mode: "static" | "interactive";
</script>

<Block
	visible={true}
	{elem_id}
	{elem_classes}
	{scale}
	{min_width}
	allow_overflow={false}
	padding={true}
>
	{#if loading_status}
		<StatusTracker
			autoscroll={gradio.autoscroll}
			i18n={gradio.i18n}
			{...loading_status}
		/>
	{/if}
    <p>{value}</p>
</Block>

<!-- handling the input files. npm functions will do it. they will turn os files to FileData python type-->
<!-- The prepare_files function will convert the browser’s File datatype to gradio’s internal FileData type. You should use the FileData data in your component to keep track of uploaded files.

The upload function will upload an array of FileData values to the server.

The normalise_file function will generate the correct URL for your component to fetch the file from and set it to the data property of the FileData.
-->

<!-- the example-->
<!-- root will define the directory for the files to be stored-->
<script lang="ts">

    import { upload, prepare_files, normalise_file, type FileData } from "@gradio/client";
    export let root; 
    export let value;
    let uploaded_files;

    $: value: normalise_file(uploaded_files, root)

    async function handle_upload(file_data: FileData[]): Promise<void> {
        await tick();
        uploaded_files = await upload(file_data, root);
    }

    async function loadFiles(files: FileList): Promise<void> {
        let _files: File[] = Array.from(files);
        if (!files.length) {
            return;
        }
        if (file_count === "single") {
            _files = [files[0]];
        }
        let file_data = await prepare_files(_files);
        await handle_upload(file_data);
    }

    async function loadFilesFromUpload(e: Event): Promise<void> {
		const target = e.target;

		if (!target.files) return;
		await loadFiles(target.files);
	}
</script>

<input
    type="file"
    on:change={loadFilesFromUpload}
    multiple={true}
/>

<!-- using WASM support-->

<script lang="ts">
    import { getContext } from "svelte";
    const upload_fn = getContext<typeof upload_files>("upload_files");

    async function handle_upload(file_data: FileData[]): Promise<void> {
        await tick();
        await upload(file_data, root, upload_fn);
    }
</script>

<!-- using existing components-->
<script>
	import { type FileData, normalise_file, Upload, ModifyUpload } from "@gradio/upload";
	import { Empty, UploadText, BlockLabel } from "@gradio/atoms";
</script>

<BlockLabel Icon={File} label={label || "PDF"} />
{#if value === null && interactive}
    <Upload
        filetype="application/pdf"
        on:load={handle_load}
        {root}
        >
        <UploadText type="file" i18n={gradio.i18n} />
    </Upload>
{:else if value !== null}
    {#if interactive}
        <ModifyUpload i18n={gradio.i18n} on:clear={handle_clear}/>
    {/if}
    <iframe title={value.orig_name || "PDF"} src={value.data} height="{height}px" width="100%"></iframe>
{:else}
    <Empty size="large"> <File/> </Empty>	
{/if}
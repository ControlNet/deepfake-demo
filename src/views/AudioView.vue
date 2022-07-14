<script setup lang="ts">
import { onMounted, onUnmounted, reactive, ref } from "vue";
import type { Ref } from "@vue/reactivity";
import WaveSurfer from "wavesurfer.js";
import { BButton, BFormTextarea } from "bootstrap-vue-3";
import { useSelectedFileStore } from "@/stores/selectedFile";
import type { ReactiveVariable } from "vue/macros";
import type { AudListJson } from "@/index";

const wavFiles: ReactiveVariable<string[]> = reactive([])
const globalSelectedFiles = useSelectedFileStore()
const selectedRefAudio: Ref<string> = ref(globalSelectedFiles.selectedRefAudio)

let wavRef: Ref<WaveSurfer | null> = ref(null);

function updateWaveformRef(): void {
  if (wavRef.value === null) {
    wavRef.value = WaveSurfer.create({
      container: "#waveform-ref",
      waveColor: "violet",
      progressColor: "purple",
    })
  }
  if (selectedRefAudio.value != "Select a pre-recorded audio") {
    wavRef.value.load(`http://localhost:7111/static/${selectedRefAudio.value}`);
  } else {
    wavRef.value?.empty()
  }
  globalSelectedFiles.setSelectedRefAudio(selectedRefAudio.value)
}

const playRef = () => wavRef.value?.playPause()
const pauseRef = () => wavRef.value?.pause()

const inputText: Ref<string> = ref(globalSelectedFiles.inputText)
const generatedAudio: Ref<string> = ref(globalSelectedFiles.selectedGenAudio)

function generate() {
  fetch(`http://localhost:7111/api/run_rtvc?speaker_audio=${selectedRefAudio.value}&text=${inputText.value}`, {
    headers: {
      "Content-Type": "text/plain"
    }
  })
      .then(res => res.text())
      .then(text => generatedAudio.value = text)
      .then(updateWaveformGenerated)
}
let wavGen: Ref<WaveSurfer | null> = ref(null);

function updateWaveformGenerated(): void {
  if (wavGen.value === null) {
    wavGen.value = WaveSurfer.create({
      container: "#waveform-generated",
      waveColor: "lightgreen",
      progressColor: "darkgreen",
    })
  }
  if (generatedAudio.value !== "") {
    wavGen.value.load(`http://localhost:7111/static/${generatedAudio.value}`);
  }
  globalSelectedFiles.setSelectedGenAudio(generatedAudio.value)
}

const playGen = () => wavGen.value?.playPause()
const pauseGen = () => wavGen.value?.pause()

// init page
onMounted(() => {

  fetch("http://localhost:7111/api/aud_list")
      .then(async res => await res.json() as AudListJson)
      .then(json => json.audios)
      .then(audios => wavFiles.push(...audios))

  if (selectedRefAudio.value !== "Select a pre-recorded audio") {
    updateWaveformRef()
  }

  if (generatedAudio.value !== "") {
    updateWaveformGenerated()
  }
})

// save the states
onUnmounted(() => {
  globalSelectedFiles.setInputText(inputText.value)
  globalSelectedFiles.setSelectedRefAudio(selectedRefAudio.value)
  globalSelectedFiles.setSelectedGenAudio(generatedAudio.value)
})
</script>

<template>
  <section class="p-2">
    <h2>Step 1: Select reference speech</h2>
    <select class="form-select w-25 d-inline-block" aria-label="Default select example" v-model="selectedRefAudio"
            @change="updateWaveformRef">
      <option selected>Select a pre-recorded audio</option>
      <option v-for="wavFile in wavFiles" :value="wavFile">{{ wavFile.slice(8) }}</option>
    </select>
    <b-button class="m-2 d-inline-block" style="display: flex" variant="danger">Record</b-button>
    <div id="waveform-ref" class="w-50"/>
    <div v-if="wavRef !== null">
      <b-button class="m-2" variant="success" @click="playRef">Play</b-button>
      <b-button class="m-2" variant="warning" @click="pauseRef">Pause</b-button>
    </div>
  </section>
  <section class="p-2" v-if="wavRef !== null">
    <h2>Step 2: Input some text</h2>
    <b-form-textarea
        class="w-50"
        v-model="inputText"
        placeholder="Input some text here..."
        rows="5"
        max-rows="5"/>
  </section>
  <section class="p-2" v-if="inputText !== '' || wavGen !== null">
    <h2>Step 3: Generate audio</h2>
    <b-button class="m-2" variant="primary" @click="generate">Generate</b-button>
    <div id="waveform-generated" class="w-50"/>
    <div v-if="wavGen !== null">
      <b-button class="m-2" variant="success" @click="playGen">Play</b-button>
      <b-button class="m-2" variant="warning" @click="pauseGen">Pause</b-button>
    </div>
  </section>
</template>

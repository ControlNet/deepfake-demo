<script setup lang="ts">
import type { Ref } from "@vue/reactivity";
import { computed, onMounted, onUnmounted, reactive, ref } from "vue";
import { useSelectedFileStore } from "@/stores/selectedFile";
import { BButton } from "bootstrap-vue-3";
import type { AudListJson, FaceListJson } from "@/index";
import WaveSurfer from "wavesurfer.js";
import Recorder from "@/components/Recorder.vue";


const globalSelectedFiles = useSelectedFileStore()
const selectedRefImage: Ref<string> = ref(globalSelectedFiles.selectedRefImage)
const faceFiles: string[] = reactive([])
const selectedRefImageUrl = computed(() => {
  if (selectedRefImage.value != "Select a reference face") {
    return `http://localhost:7112/static/${selectedRefImage.value}`
  } else {
    return ""
  }
})
const refImageSelected: Ref<boolean> = computed(() => {
  return selectedRefImageUrl.value !== ""
})

const selectedRefAudio: Ref<string> = ref(globalSelectedFiles.selectedRefWav2LipSpeech)
const wavFiles: string[] = reactive([])
const selectedRefAudioUrl = computed(() => {
  if (selectedRefAudio.value != "Select an audio") {
    return `http://localhost:7111/static/${selectedRefAudio.value}`
  } else {
    return ""
  }
})

const refAudioSelected: Ref<boolean> = computed(() => {
  return selectedRefAudioUrl.value !== ""
})

let wavRef: Ref<WaveSurfer | null> = ref(null);

function updateWaveformRef(): void {
  if (wavRef.value === null) {
    wavRef.value = WaveSurfer.create({
      container: "#waveform-ref",
      waveColor: "violet",
      progressColor: "purple",
    })
  }
  if (selectedRefAudio.value != "Select an audio") {
    wavRef.value.load(selectedRefAudioUrl.value);
  } else {
    wavRef.value?.empty()
  }
  globalSelectedFiles.setSelectedRefWav2LipSpeech(selectedRefAudio.value)
}

const generatedAudio: Ref<string> = ref(globalSelectedFiles.selectedGenAudio)
const generatedVideo: Ref<string> = ref(globalSelectedFiles.selectedGenVideo)

const playRef = () => wavRef.value?.playPause()
const pauseRef = () => wavRef.value?.pause()

onMounted(async () => {
  const taskGetFaces = fetch("http://localhost:7112/api/face_list")
      .then(async res => await res.json() as FaceListJson)
      .then(json => json.faces)
      .then(faces => faceFiles.push(...faces))

  const taskGetAudios = fetch("http://localhost:7111/api/aud_list")
      .then(async res => await res.json() as AudListJson)
      .then(json => json.audios)
      .then(audios => wavFiles.push(...audios))

  await Promise.all([taskGetFaces, taskGetAudios])
  if (refImageSelected.value) {
    updateWaveformRef()
  }
})

onUnmounted(() => {
  globalSelectedFiles.setSelectedRefImage(selectedRefImage.value)
})

function updateSelectedImage() {
  globalSelectedFiles.setSelectedRefImage(selectedRefImage.value)
}

function generate() {
  generatedVideo.value = ""
  fetch(`http://localhost:7112/api/run_wav2lip?face=${selectedRefImage.value}&audio=${selectedRefAudio.value}`, {
    headers: {
      "Content-Type": "text/plain"
    }
  })
      .then(res => res.text())
      .then(text => generatedVideo.value = text)
      .then(updateGeneratedVideo)
}

function updateGeneratedVideo() {
  globalSelectedFiles.setSelectedGenVideo(generatedVideo.value)
}

const generatedVideoUrl = computed(() => {
  if (generatedVideo.value != "") {
    return `http://localhost:7112/static/${generatedVideo.value}`
  } else {
    return ""
  }
})

const videoIsGenerated = computed(() => {
  return generatedVideoUrl.value !== ""
})

const option = {
  controls: ["play"]
}

</script>

<template>
  <section class="p-2">
    <h2>Step 1: Select reference face</h2>
    <select class="form-select w-25 d-inline-block" aria-label="Default select example" v-model="selectedRefImage"
            @change="updateSelectedImage">
      <option selected>Select a reference face</option>
      <option v-if="globalSelectedFiles.hasRecVideo" :value="globalSelectedFiles.selectedRecVideo">Recorded Face</option>
      <option v-for="faceFile in faceFiles" :value="faceFile">{{ faceFile.slice(8) }}</option>
    </select>
    <Recorder type="video"/>
    <p/>
    <img :src="selectedRefImageUrl" alt="" v-if="refImageSelected" style="width: 150px">
  </section>

  <section class="p-2" v-if="refImageSelected">
    <h2>Step 2: Select speech audio</h2>
    <select class="form-select w-25 d-inline-block" aria-label="Default select example" v-model="selectedRefAudio"
            @change="updateWaveformRef">
      <option selected>Select an audio</option>
      <option v-if="globalSelectedFiles.hasGenAudio" :value="generatedAudio">Generated Audio</option>
      <option v-if="globalSelectedFiles.hasRecAudio" :value="globalSelectedFiles.selectedRecAudio">Recorded Audio
      </option>
      <option v-for="wavFile in wavFiles" :value="wavFile">{{ wavFile.slice(8) }}</option>
    </select>
    <Recorder type="audio"/>
    <div id="waveform-ref" class="w-50"/>
    <div v-if="wavRef !== null">
      <b-button class="m-2" variant="success" @click="playRef">Play</b-button>
      <b-button class="m-2" variant="warning" @click="pauseRef">Pause</b-button>
    </div>
  </section>

  <section class="p-2" v-if="refAudioSelected">
    <h2>Step 3: Generate lip-synced video</h2>
    <b-button class="m-2" variant="primary" @click="generate">Generate</b-button>
    <div v-if="videoIsGenerated" id="video-in-wav2lip">
      <vue-plyr :options="option">
        <video>
          <source :src="generatedVideoUrl" type="video/mp4"/>
        </video>
      </vue-plyr>
    </div>
  </section>
</template>

<style>
div#video-in-wav2lip > div.plyr {
  width: 150px;
  min-width: 150px;
}
</style>

<script setup lang="ts">
import { BButton } from "bootstrap-vue-3";
import { computed, ref } from "vue";
import type { Ref } from "@vue/reactivity";
import axios from "axios";
import { useSelectedFileStore } from "@/stores/selectedFile";

let device: MediaStream | null = null
const recorder: Ref<MediaRecorder | null> = ref(null)
const isRecording: Ref<boolean> = ref(false)
const globalSelectedFiles = useSelectedFileStore()
const fileName = ref(globalSelectedFiles.selectedRecAudio)

async function requestDevice() {
  device = await navigator.mediaDevices.getUserMedia({audio: true})
}

async function uploadAudio(blob: Blob) {
  const formData = new FormData()
  formData.append("file", blob)

  return await axios.post("http://localhost:7111/api/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
      "Accept": "application/json"
    }
  }).then(res => res.data.file_name)
}

let collectResult = false

async function start() {
  if (device === null) {
    await requestDevice()
  }
  recorder.value = new MediaRecorder(device!)
  isRecording.value = true
  recorder.value!.ondataavailable = async (e) => {
    if (collectResult) {
      fileName.value = await uploadAudio(e.data)
      globalSelectedFiles.setSelectedRecAudio(fileName.value)
      collectResult = false
    }
  }
  recorder.value!.start()
}

function stop() {
  collectResult = true
  recorder.value?.stop()
  isRecording.value = false
}

function cancel() {
  collectResult = false
  recorder.value?.stop()
  isRecording.value = false
}

async function startOrStop() {
  if (isRecording.value) {
    stop()
  } else {
    await start()
  }
}

const recordButtonContent = computed(() => {
  if (isRecording.value) {
    return "Stop"
  } else {
    return "Record"
  }
})

</script>

<template>
  <b-button class="m-2 d-inline-block" style="display: flex" variant="danger" @click="startOrStop">
    {{ recordButtonContent }}
  </b-button>
  <b-button class="m-2 d-inline-block" style="display: flex" @click="cancel" v-if="isRecording">Cancel</b-button>
</template>

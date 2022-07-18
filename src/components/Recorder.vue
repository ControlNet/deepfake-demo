<script setup lang="ts">
import { BButton } from "bootstrap-vue-3";
import { computed, ref } from "vue";
import type { Ref } from "@vue/reactivity";
import axios from "axios";
import { useSelectedFileStore } from "@/stores/selectedFile";

interface Props {
  type: "audio" | "video";
}

const props = defineProps<Props>()

let device: MediaStream | null = null
const recorder: Ref<MediaRecorder | null> = ref(null)
const isRecording: Ref<boolean> = ref(false)
const globalSelectedFiles = useSelectedFileStore()
let fileName: Ref<string> = ref("")
switch (props.type) {
  case "audio":
    fileName.value = globalSelectedFiles.selectedGenAudio
    break;
  case "video":
    fileName.value = globalSelectedFiles.selectedGenVideo
    break;
}

const enableVideoView = ref(false)

async function requestDevice() {
  switch (props.type) {
    case "audio":
      device = await navigator.mediaDevices.getUserMedia({audio: true})
      break;
    case "video":
      device = await navigator.mediaDevices.getUserMedia({video: true})
      break;
  }
}

let uploadUrl = ""
switch (props.type) {
  case "audio":
    uploadUrl = "http://localhost:7111/api/upload"
    break;
  case "video":
    uploadUrl = "http://localhost:7112/api/upload"
    break;
}

async function upload(blob: Blob) {
  const formData = new FormData()
  formData.append("file", blob)

  return await axios.post(uploadUrl, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
      "Accept": "application/json"
    }
  }).then(res => res.data.file_name)
}

let collectResult = false
const videoElement: Ref<HTMLVideoElement | null> = ref(null)
const canvasElement: Ref<HTMLCanvasElement | null> = ref(null)

async function start() {
  if (device === null) {
    await requestDevice()
  }
  recorder.value = new MediaRecorder(device!)
  isRecording.value = true
  if (props.type === "audio") {
    recorder.value!.ondataavailable = async (e) => {
      if (collectResult) {
        fileName.value = await upload(e.data)
        globalSelectedFiles.setSelectedRecAudio(fileName.value)
        collectResult = false
      }
    }
    recorder.value!.start()
  } else {
    enableVideoView.value = true;
    videoElement.value!.srcObject = device
    videoElement.value!.hidden = false
  }
}

function stopRecorder() {
  if (props.type === "audio") {
    recorder.value?.stop()
  } else {
    if (videoElement.value !== null) {
      videoElement.value.pause()
      videoElement.value.hidden = true
    }
    enableVideoView.value = false
  }
}

function stop() {
  collectResult = true
  if (props.type === "video" && canvasElement.value !== null) {
    canvasElement.value!.width = videoElement.value!.videoWidth
    canvasElement.value!.height = videoElement.value!.videoHeight
    canvasElement.value!.getContext("2d")!.drawImage(videoElement.value!, 0, 0)
    canvasElement.value!.toBlob(async (blob) => {
      fileName.value = await upload(blob!)
      globalSelectedFiles.setSelectedRecVideo(fileName.value)
    }, "image/png")
  }
  stopRecorder()
  isRecording.value = false
}

function cancel() {
  collectResult = false
  stopRecorder()
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
    switch (props.type) {
      case "audio":
        return "Stop"
      case "video":
        return "Screenshot"
    }
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
  <p v-if="isRecording"/>
  <video autoplay hidden="hidden" ref="videoElement"/>
  <canvas ref="canvasElement" hidden/>
</template>

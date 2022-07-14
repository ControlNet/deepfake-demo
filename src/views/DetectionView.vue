<script setup lang="ts">

import { onMounted, reactive } from "vue";
import type { RealSamplesJson } from "@/index";
import DetectionVideo from "@/components/DetectionVideo.vue";
import { BButton, BCardGroup } from "bootstrap-vue-3";
import { useSelectedFileStore } from "@/stores/selectedFile";

class VideoData {
  video: string
  label: string
  prob: number | null

  constructor(video: string, label: string) {
    this.video = video
    this.label = label
    this.prob = null
  }
}

const videos: VideoData[] = reactive([])
const selectedFiles = useSelectedFileStore()

onMounted(async () => {
  await fetch("http://localhost:7113/api/real_samples")
      .then(async response => await response.json() as RealSamplesJson)
      .then(json => json.samples)
      .then(samples => samples.forEach(sample => {
        videos.push(new VideoData(sample, "REAL"))
      }))
  if (selectedFiles.hasGenVideo) {
    videos.push(new VideoData(selectedFiles.selectedGenVideo, "FAKE"))
  }
});

function detect() {
  for (const d of videos) {
    const videoPath = d.label === "REAL" ? d.video : `../wav2lip/${d.video}`

    fetch(`http://localhost:7113/api/detect?video=${videoPath}`, {
      headers: {
        "Content-Type": "text/plain"
      }
    }).then(response => response.text())
        .then(prob => d.prob = Number(Number(prob).toFixed(4)))
  }
}
</script>

<template>
  <div class="p-2">
    <h2>Deepfake Detection</h2>
    <b-card-group>
      <DetectionVideo v-for="d in videos" :video="d.video" :label="d.label" :prob="d.prob"/>
    </b-card-group>
  </div>

  <div style="text-align: center">
    <b-button class="m-2 w-25" variant="primary" @click="detect">Detect</b-button>
  </div>

</template>

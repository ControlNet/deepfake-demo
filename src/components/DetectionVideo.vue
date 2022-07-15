<script setup lang="ts">
import { BButton, BCard, BCardText } from "bootstrap-vue-3";
import { computed } from "vue";

interface Props {
  video: string
  label: string
  prob: number | null
}

const props = defineProps<Props>()

const videoUrl = computed(() => {
  if (props.label === "REAL") {
    return `http://127.0.0.1:7113/static/${props.video}`
  } else {
    return `http://127.0.0.1:7112/static/${props.video}`
  }
})

const labelColor = computed(() => {
  if (props.label === "REAL") {
    return "text-success"
  } else {
    return "text-danger"
  }
})

const labelClass = computed(() => labelColor.value + " fw-bold")

const probColor = computed(() => {
  if (props.prob === null) {
    return ""
  } else if (props.prob < 0.5) {
    return "text-success"
  } else {
    return "text-danger"
  }
})

const probClass = computed(() => probColor.value)
const probStr = computed(() => props?.prob ?? "N/A")

const option = {
  controls: ["play"]
}

</script>

<template>
  <b-card class="text-center">
    <b-card-text>
      <vue-plyr :options="option">
        <video>
          <source :src="videoUrl" type="video/mp4"/>
        </video>
      </vue-plyr>
    </b-card-text>
    <b-card-text>
      <h2 :class="labelClass">
        {{ label }}
      </h2>
    </b-card-text>
    <b-card-text>
      <h4 :class="probClass">
        {{ probStr }}
      </h4>
    </b-card-text>
  </b-card>
</template>

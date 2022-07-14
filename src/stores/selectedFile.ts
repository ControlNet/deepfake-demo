import { defineStore } from 'pinia'

export const useSelectedFileStore = defineStore({
    id: 'selectedFile',
    state: () => ({
        selectedRefAudio: "Select a pre-recorded audio",
        selectedGenAudio: "",
        selectedRecAudio: "",
        selectedRefWav2LipSpeech: "Select an audio",
        selectedGenVideo: "",
        selectedRefImage: "Select a reference face",
        inputText: ""
    }),
    getters: {
        hasGenAudio: state => state.selectedGenAudio !== "",
        hasRecAudio: state => state.selectedRecAudio !== "",
        hasGenVideo: state => state.selectedGenVideo !== "",
    },
    actions: {
        setSelectedRefAudio(value: string) {
            this.selectedRefAudio = value
        },
        setSelectedGenAudio(value: string) {
            this.selectedGenAudio = value
        },
        setSelectedRefImage(value: string) {
            this.selectedRefImage = value
        },
        setSelectedRecAudio(value: string) {
            this.selectedRecAudio = value
        },
        setSelectedRefWav2LipSpeech(value: string) {
            this.selectedRefWav2LipSpeech = value
        },
        setSelectedGenVideo(value: string) {
            this.selectedGenVideo = value
        },
        setInputText(value: string) {
            this.inputText = value
        }
    }
})

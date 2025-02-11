// Registering the custom node in the ComfyUI frontend
app.registerExtension({
    name: "ZonosTTS.Node",
    registerCustomNodes: function () {
        // Node's appearance and behavior
        class ZonosTTSNode {
            constructor() {
                // Node title and category
                this.title = "Zonos TTS";
                this.category = "audio";
                this.description = "Generate speech using Zyphra/Zonos-v0.1-hybrid model.";
                this.version = "1.0.0";

                // Define input and output slots
                this.addInput("text", "STRING");
                this.addInput("speaker_audio", "AUDIO", { optional: true });
                this.addOutput("audio", "AUDIO");
                this.addOutput("metadata", "JSON");

                // Custom UI elements
                this.language = "en-us";
                this.emotion = "neutral";
                this.pitch = 0.0;
                this.speaking_rate = 1.0;

                // Create dropdown for language selection
                this.languageDropdown = this.addWidget(
                    "combo",
                    "Language",
                    this.language,
                    (value) => {
                        this.language = value;
                        this.onLanguageChange(value);
                    },
                    {
                        values: ["en-us", "ja", "zh", "fr", "de"],
                    }
                );

                // Create dropdown for emotion selection
                this.emotionDropdown = this.addWidget(
                    "combo",
                    "Emotion",
                    this.emotion,
                    (value) => {
                        this.emotion = value;
                        this.onEmotionChange(value);
                    },
                    {
                        values: ["neutral", "happiness", "anger", "sadness", "fear"],
                    }
                );

                // Create slider for pitch adjustment
                this.pitchSlider = this.addWidget(
                    "slider",
                    "Pitch",
                    this.pitch,
                    (value) => {
                        this.pitch = value;
                        this.onPitchChange(value);
                    },
                    {
                        min: -1.0,
                        max: 1.0,
                        step: 0.1,
                    }
                );

                // Create slider for speaking rate adjustment
                this.speakingRateSlider = this.addWidget(
                    "slider",
                    "Speaking Rate",
                    this.speaking_rate,
                    (value) => {
                        this.speaking_rate = value;
                        this.onSpeakingRateChange(value);
                    },
                    {
                        min: 0.5,
                        max: 2.0,
                        step: 0.1,
                    }
                );

                // Add a button to preview audio
                this.previewButton = this.addWidget(
                    "button",
                    "Preview Audio",
                    () => {
                        this.onPreviewAudio();
                    }
                );
            }

            // Event handlers for UI changes
            onLanguageChange(value) {
                console.log("Language changed to:", value);
            }

            onEmotionChange(value) {
                console.log("Emotion changed to:", value);
            }

            onPitchChange(value) {
                console.log("Pitch changed to:", value);
            }

            onSpeakingRateChange(value) {
                console.log("Speaking rate changed to:", value);
            }

            // Handle audio preview
            onPreviewAudio() {
                console.log("Previewing audio...");
                // Send a request to the backend to generate and preview audio
                app.queuePrompt({
                    inputs: {
                        text: this.inputs[0].value,
                        language: this.language,
                        emotion: this.emotion,
                        pitch: this.pitch,
                        speaking_rate: this.speaking_rate,
                        speaker_audio: this.inputs[1]?.value,
                    },
                    outputs: {
                        audio: this.outputs[0],
                        metadata: this.outputs[1],
                    },
                });
            }
        }

        // Register the node in the ComfyUI interface
        LiteGraph.registerNodeType("ZonosTTS/Node", ZonosTTSNode);
    },
});
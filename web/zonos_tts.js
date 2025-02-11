import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

// Settings for the extension
const EXTENSION_NAME = "zonos.tts";

app.registerExtension({
    name: EXTENSION_NAME,
    async setup() {
        // Add settings for the TTS node
        const settings = [
            {
                id: "zonos.tts.preview_audio",
                name: "Preview audio after generation",
                type: "boolean",
                defaultValue: true,
            },
            {
                id: "zonos.tts.default_language",
                name: "Default language",
                type: "combo",
                defaultValue: "en-us",
                options: ["en-us", "ja", "zh", "fr", "de"],
            }
        ];
        
        // Add settings to ComfyUI
        for (const setting of settings) {
            app.ui.settings.addSetting(setting);
        }
    },

    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // Only modify our node type
        if (nodeData.name !== "ZonosTTSNode") {
            return;
        }

        // Store the original onNodeCreated
        const onNodeCreated = nodeType.prototype.onNodeCreated;

        // Override node creation
        nodeType.prototype.onNodeCreated = function() {
            const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

            // Add preview button to node
            this.addWidget("button", "Preview", null, () => {
                // Only preview if we have audio data
                if (this.audioData) {
                    this.previewAudio(this.audioData);
                }
            });

            return r;
        };

        // Add custom widget handling
        const onExecuted = nodeType.prototype.onExecuted;
        nodeType.prototype.onExecuted = function(message) {
            const r = onExecuted ? onExecuted.apply(this, arguments) : undefined;

            // Store audio data for preview
            if (message?.audio?.waveform) {
                this.audioData = message.audio;
                
                // Auto-preview if enabled in settings
                if (app.ui.settings.getSettingValue("zonos.tts.preview_audio", true)) {
                    this.previewAudio(this.audioData);
                }
            }

            return r;
        };

        // Add right-click menu options
        const getExtraMenuOptions = nodeType.prototype.getExtraMenuOptions;
        nodeType.prototype.getExtraMenuOptions = function(_, options) {
            getExtraMenuOptions?.apply(this, arguments);
            
            options.push(
                null, // Add separator
                {
                    content: "Play Latest Audio",
                    callback: () => {
                        if (this.audioData) {
                            this.previewAudio(this.audioData);
                        }
                    }
                }
            );
        };

        // Add preview audio method
        nodeType.prototype.previewAudio = function(audioData) {
            // Convert audio data to format suitable for playback
            // This is a placeholder - implement based on your audio format
            console.log("Playing audio:", audioData);
        };
    }
});
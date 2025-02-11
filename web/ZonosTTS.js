import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

app.registerExtension({
    name: "Comfy.ZonosTTS",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "ZonosTTSNode") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                this.addInput("text", "STRING");
                this.addInput("speaker_audio", "AUDIO");
                this.addOutput("audio", "AUDIO");
                this.addOutput("metadata", "JSON");
                
                ComfyWidgets.STRING(this, "text", ["STRING", { multiline: true }], app);
                ComfyWidgets.COMBO(this, "language", ["COMBO", { values: ["en-us", "ja", "zh", "fr", "de"] }], app);
                ComfyWidgets.COMBO(this, "emotion", ["COMBO", { values: ["neutral", "happiness", "anger", "sadness", "fear"] }], app);
                ComfyWidgets.FLOAT(this, "pitch", ["FLOAT", { default: 0.0, min: -1.0, max: 1.0 }], app);
                ComfyWidgets.FLOAT(this, "speaking_rate", ["FLOAT", { default: 1.0, min: 0.5, max: 2.0 }], app);
                
                return r;
            };
        }
    }
});
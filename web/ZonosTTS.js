import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "Zonos.TTS",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "ZonosTTSNode") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                return r;
            };
        }
    }
});
import { LMStudioPlugin } from "./provider/lmstudio.js"
import { OllamaPlugin } from "./provider/ollama.js"
import { StrataPlugin } from "./provider/strata.js"
import { VLLMPlugin } from "./provider/vllm.js"
import type { PluginInternal } from "./internal.js"

// Keep upstream implementations in the tree but do not activate hosted providers.
export const ProviderPlugins: PluginInternal.InternalPlugin[] = [
  StrataPlugin,
  LMStudioPlugin,
  OllamaPlugin,
  VLLMPlugin,
]

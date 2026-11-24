import { Effect, Schema } from "effect"
import { createLocalProviderPlugin } from "./local.js"

// OpenAI-compatible local inference. Discovery does not assume vision or tool
// support from a model name; explicit model configuration can override these.
const RemoteModel = Schema.Struct({
  id: Schema.String,
  name: Schema.optional(Schema.String),
  context_length: Schema.optional(Schema.Int),
  capabilities: Schema.optional(Schema.Struct({
    vision: Schema.optional(Schema.Boolean),
    tools: Schema.optional(Schema.Boolean),
  })),
})
const Response = Schema.Struct({ data: Schema.Array(RemoteModel) })

export const make = createLocalProviderPlugin({
  id: "oddityagent.provider.strata",
  providerID: "strata",
  name: "Strata",
  origin: "http://127.0.0.1:8080",
  discover: (client) =>
    Effect.gen(function* () {
      const response = yield* client.getJson("/v1/models", Response)
      return response.data.filter((model) => model.id.trim().length > 0)
    }),
  model: (item) => ({
    id: item.id,
    name: item.name,
    context: item.context_length,
    vision: item.capabilities?.vision,
    tools: item.capabilities?.tools,
  }),
})

export const StrataPlugin = make()

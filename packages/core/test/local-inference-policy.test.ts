import { expect, test } from "bun:test"
import { isLocalInferenceURL } from "../src/effect/local-inference-policy.js"

test("allows loopback and private inference servers", () => {
  for (const url of ["http://localhost:8080/v1", "http://127.0.0.1:11434", "http://10.0.0.60:8080/v1", "https://172.31.0.1", "http://192.168.1.2", "http://[::1]:8000"]) {
    expect(isLocalInferenceURL(url)).toBe(true)
  }
})
test("rejects public, malformed and credential-bearing endpoints", () => {
  for (const url of ["https://api.openai.com/v1", "https://opencode.ai", "http://8.8.8.8", "http://172.32.0.1", "http://192.169.0.1", "http://localhost.evil.test", "http://localhost@evil.test", "http://user:pass@127.0.0.1", "file:///tmp/model", "not a URL"]) {
    expect(isLocalInferenceURL(url)).toBe(false)
  }
})

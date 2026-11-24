// OddityAgent inference endpoint policy. Deliberately require literal private
// addresses (or localhost); arbitrary DNS names can resolve to public hosts.
export function isLocalInferenceURL(value: string): boolean {
  try {
    const url = new URL(value)
    if (!["http:", "https:", "ws:", "wss:"].includes(url.protocol)) return false
    if (url.username || url.password) return false
    const host = url.hostname
    if (host === "localhost" || host === "[::1]") return true
    const octets = host.split(".")
    if (octets.length !== 4 || octets.some((part) => !/^\d+$/.test(part) || Number(part) > 255)) return false
    const [a, b] = octets.map(Number)
    return a === 127 || a === 10 || (a === 172 && b >= 16 && b <= 31) || (a === 192 && b === 168)
  } catch {
    return false
  }
}

export const localProviderIDs: ReadonlySet<string> = new Set(["strata", "ollama", "lmstudio", "vllm"])

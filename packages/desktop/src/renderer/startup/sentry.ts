import pkg from "../../../package.json"

export function desktopVersion() {
  return import.meta.env.OPENCODE_VERSION ?? pkg.version
}

// In-house builds never initialize the upstream crash reporting service.
export async function initializeSentry(_version: string) {}

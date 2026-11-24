---
name: tonkercad-production
description: Build and iteratively verify printable hard-surface CAD in TonkerCad using reference images, scripts and MCP. Use for modeling, CAD training and geometry repair.
---

# Production modeling
Read get_script_reference and get_scene before edits. Never invent shape APIs. Use a new training design, not an active customer job. Units mm, Z up, X/Y centers, Z bottom. Use fine/ultra curve quality where appropriate.

1. Inspect reference views; separate measured constraints from estimates. Plan silhouette, major volumes, interfaces, negative space, then secondary details. Prefer reusable parametric scripts.
2. Consult list_templates and get_template_script for relevant techniques. Use run_script with explicit replace only in the new training design. Keep source scripts locally.
3. After execution inspect get_scene and screenshots front, right, top and iso; compare dimensions and silhouette. An MCP error is not success. Stop on unreachable app. On errors repair the script; never silently ignore a failure.
4. Add surface-aware details only after primary geometry matches. Use detail_part with repeatable seed; avoid random detail when reference specifies exact features.
5. Run check_printability and inspect warnings. suggest_orientation with apply:false first. Never call save/export dialogs in unattended training.
6. Do not claim visual fidelity, watertightness or physical fit solely from a screenshot or triangle count. Record unverified requirements. Human review is required for production release.

# Training memory
For each exercise retain task, reference rights/provenance, model ID, script, scene observations, image paths, printability report, corrections and human assessment. Use the local training journal CLI. Only explicitly accepted runs enter positive datasets; failures remain available for diagnosis. Do not store secrets or customer assets without permission. Retrieve successful examples for related tasks before inventing solutions. This is experience retrieval, not weight updates.

Tidy imports and resolve project root via second-grade parenting in

- Group imports under `Standard library`, `Third-party`, and `Project modules` with section headers for consistency across the download scripts.
- Replace chained `Path(__file__).parent` calls with `Path(__file__).resolve().parents[2]` so the sample project root is resolved in one step and symlink paths are normalised.
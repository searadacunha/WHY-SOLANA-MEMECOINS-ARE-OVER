# DARK-MAGA historical research archive

This content-addressed archive preserves the source repository's reachable commit graph and historical file versions, including branches that were not merged into the published case study. It is separate from the current [investigation](../dark-maga/README.md).

- [Source refs](refs.json)
- [Archive inventory](summary.json)
- [Commit graph and file changes](commits.jsonl)
- [Blob inventory and publication hashes](blobs.jsonl)
- [Source issues, pull requests and comments](github-metadata.json)

Restore a historical version to an empty directory:

```sh
python investigations/dark-maga-history/restore.py heads/main ./dmaga-restored
```

The archive uses the original Git object identifiers and records the publication hash of each available blob. Potential credentials and local identifying paths are redacted. Some objects may be excluded under the publication gate; the original commit graph is not a byte-identical Git clone. Do not interpret old branches as current conclusions. Before removing the source repository, retain a private original mirror or bundle if exact history is needed. Public issue and pull request metadata and comments are preserved separately; review events, external data archives, GitHub discussions and untracked files are not included.

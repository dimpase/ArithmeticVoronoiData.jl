# Historical archives

These immutable archives were imported from
[arithmetic_voronoi at ab845e4](https://github.com/dimpase/arithmetic_voronoi/tree/ab845e44ab33d9e46d88f27c33a795ae09b0fbef).
Their payloads and checksum manifests are unchanged. Paths inside the archives
and historical receipts describe the original delivery. The engine never
selects these archives automatically.

| Directory | Contents |
| --- | --- |
| `dataset/` | Sealed five-field C++ dataset, including certificates and its verifying software snapshot (9 MB compressed) |
| `fixtures/` | D5/D8 geometric regression certificates (761 KB compressed) |

Install Git LFS, then clone and verify this repository:

```sh
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/dimpase/ArithmeticVoronoiData.jl.git
cd ArithmeticVoronoiData.jl
git lfs install --local
git lfs pull
python3 scripts/verify_archives.py
```

For local Julia development, run `using Pkg; Pkg.develop(path="/absolute/path/to/ArithmeticVoronoiData.jl")`
in your client environment. Neither archive is required by `load_presentation`.

To unpack the sealed dataset from this checkout:

```sh
tar -xzf archives/dataset/arithmetic_groups_dataset_v1.tar.gz -C archives/dataset
julia --startup-file=no --project=archives/dataset/arithmetic_groups_dataset_v1/software \
  -e 'using Pkg; Pkg.instantiate(;allow_autoprecomp=false)'
julia --startup-file=no --project=archives/dataset/arithmetic_groups_dataset_v1/software \
  archives/dataset/arithmetic_groups_dataset_v1/software/scripts/verify_dataset.jl \
  archives/dataset/arithmetic_groups_dataset_v1
```

Add `--complete` to the last command to replay geometric certificates and
Tietze maps. Neither verification mode needs a C++ executable. Keep extracted
files unchanged so the dataset manifest remains valid. See the engine's
[dataset schema](https://github.com/dimpase/arithmetic_voronoi/blob/main/DATASET_SCHEMA.md)
for the strength of each verification mode.

To restore the D5/D8 fixtures for the optional engine integration tests, run
from the **engine** checkout (Python 3.12+):

```sh
python3 scripts/restore_fixtures.py --data-root /absolute/path/to/ArithmeticVoronoiData.jl
```

The script checks the manifest and every file hash, and refuses to overwrite
different data. Restoration is explicit; new engine computations do not use
these fixtures. Engine integration tests are documented in its
[user guide](https://github.com/dimpase/arithmetic_voronoi/blob/main/USER_GUIDE.md#tests).

# SnapBATCH

### Install 
```
pip install snapbatch
```

### Usage
```
snapbatch [-J your_job_name] [OPTIONS(1)...] [ : [OPTIONS(N)...]] script(0) [args(0)...]
```

`snapbatch` is a replacement of `sbatch` to create a snapshot of current working directory, and submit the command to `sbatch`.\n
This command simply:
1. commits the dirty changes of files monitored by git AND all untracked .py/.sh to a new branch. 
2. copies this branch to the path of environment `SNAP_BATCHES`, default to `~/snapbatches`.
3. runs `sbatch --chdir /copied_path/relative/path {--arg xxx ...} (the following args to snapbatch)`

Author: mingding.thu dot gmail.com

### Purge branches
```
snapbatch_purge [n]
```
Run under the git working directory. Keep the last n snapbatch branches, default 0.


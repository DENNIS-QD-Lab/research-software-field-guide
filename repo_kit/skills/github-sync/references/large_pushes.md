# Large pushes that fail partway

A push uploads every commit, tree, and file that the remote does not have yet, as one compressed
pack over one connection. When that pack is tens of megabytes, the connection is open long enough
for something between the computer and GitHub to cut it: a network proxy, a firewall, or a dropped
HTTP/2 stream. The error appears after git reports `Writing objects: 100%`, and names the cut rather
than the cause (`RPC failed; curl 55`, `Broken pipe`, `unexpected disconnect while reading sideband
packet`, `the remote end hung up unexpectedly`). Nothing is lost: the commits are still local.

## Measure what the push would send

The survey script reports the new file data per branch. To see which commits carry it, list each
unpushed commit with the size of the files it adds or changes:

```bash
for c in $(git rev-list --reverse origin/<branch>..<branch>); do
  kb=$(git diff-tree -r --no-commit-id --diff-filter=AM --name-only "$c" |
       while read -r f; do git cat-file -s "$c:$f"; done |
       awk '{s += $1} END {printf "%d", s / 1024}')
  echo "$(git log -1 --format='%h %s' "$c" | cut -c1-60)  ${kb} KB"
done
```

For a branch that has never been pushed, compare against the default branch instead
(`origin/main..<branch>`). Large commits are usually regenerated binaries: figure images, PDFs, or
data files committed again each time they are remade.

## Work down this list

1. **Retry once or twice.** These cuts are often intermittent; the same push can fail several times
   and then go through unchanged.
2. **Force HTTP/1.1** for the repository: `git config http.version HTTP/1.1`. Large uploads to
   GitHub over HTTP/2 are a common source of these resets.
3. **Push in stages, one stretch of commits at a time.** Pushing a commit sends only what the remote
   lacks up to that commit, so stepping through the branch keeps each upload small. Choose stage
   boundaries from the measurement above so each stage stays under the size that has been getting
   through.

   ```bash
   for c in <commit1> <commit2> <commit3> <branch-tip>; do
     ok=no
     for try in 1 2 3; do
       if git push origin "${c}:refs/heads/<branch>"; then ok=yes; break; fi
       echo "push of $c failed (try $try)"; sleep 60
     done
     [ "$ok" = yes ] || { echo "stuck at $c"; break; }
   done
   git branch --set-upstream-to=origin/<branch> <branch>
   git ls-remote origin <branch>
   ```

   Two details matter. Write `"${c}:refs/…"` with braces: in zsh, an unbraced `$c:r…` is read as a
   filename modifier and the commit id is mangled. And when resuming after a stage fails, start the
   list at the first commit the remote does not have (check with `git ls-remote`). Pushing a commit
   older than the remote's tip is a rewind, which the remote rejects.
4. **When a single commit is too large to get through.** A commit cannot be split without rewriting
   it, which changes the id of every commit after it, so it has to go up whole. Try, in order:
   - another network, such as a phone hotspot or a different wired or wireless connection, since
     the cut is usually made by something on the network path;
   - SSH instead of HTTPS, if the person has an SSH key on GitHub (`ssh -T git@github.com` greets
     them by username):
     `git push git@github.com:<owner>/<repo>.git "<commit>:refs/heads/<branch>"`;
   - a background retry loop that keeps trying for an hour or more and logs to a file, so the
     terminal is free. Use the staged loop above with more tries and longer waits, wrapped in
     `nohup zsh -c '…' > ~/push.log 2>&1 &` (or `bash -c`).

## What does not help

- **Raising `http.postBuffer`.** It fixes some HTTP 400 and 411 errors on older setups, not a
  connection cut partway through an upload.
- **Sending the files ahead on a temporary branch.** When choosing what to send, git skips the
  objects reachable from commits that the pushed branch shares with the remote. Files that reached
  GitHub on an unrelated branch are uploaded again, so the final push is just as large.
  This was measured, by packing the push locally, before being ruled out.
- **A spurious "Everything up-to-date".** After a failed `git push -u`, the branch's upstream can
  be left pointing somewhere wrong, and a later bare `git push` may report nothing to do. Push with
  an explicit `<commit>:refs/heads/<branch>` refspec and check `git ls-remote`.

## Preventing large pushes

What makes a push large is usually the same binary files committed again and again: a figure
regenerated at full resolution for each revision, for example. Ways to keep pushes small:

- Commit a modest-resolution preview image for viewing on GitHub, and keep the full-resolution
  version as a vector PDF or regenerate it from the code.
- Commit figures only when they are promoted for the manuscript, not at every draft.
- Track the folders that hold large binaries with Git LFS, which stores them outside the normal
  history.

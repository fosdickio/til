# Useful Git Snippets

## Syncing with an Upstream Branch

### Create a New Branch
```bash
git fetch upstream && git checkout upstream/master
```

### Use the Current Branch
```bash
git fetch upstream && git reset --hard upstream/master
```

---

## Rebase
```bash
git fetch upstream && git rebase upstream/master
```

---

## Merge and Squash Commits
```bash
git merge --squash <branch_name>
```

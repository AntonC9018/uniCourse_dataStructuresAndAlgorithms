# Lab 7

Topic: **Git and version control**.

[Accompanying video](https://www.youtube.com/watch?v=fcxFAW1EE_A&list=PL4sUOB8DjVlVVw9Yx_tUO7fRPDYeaACXD&index=3)

## Concepts

- Git repository
- staging area (`git add`)
- commit, commit hash, commit log (commit history)
- branch
- checkout
- remote
- .git folder
- .gitignore file
- `git config` vs `git config --global`
- rebase, merge
- PR (Pull Request)
- `git push`, `git pull`

## Questions

- How can you obtain a copy of a Git repository from GitHub, including its full history, on another computer?
> <details>
> <summary>Answer</summary>
>
> You could create a new repository on the other computer, link it to the remote repository on GitHub, and run `git pull`.
> Another option is to use `git clone`, which also automatically checks out the correct default branch.
> </details>

- How can you create a Pull Request using Git (not GitHub)?
> <details>
> <summary>Answer</summary>
> You cannot. The concept of a Pull Request does not exist in Git.
> </details>

- You created a branch for feature1 based on the main branch and worked on it.
  Then you created a branch for feature2, also based on the main branch, and worked on it.
  You opened a PR and merged feature1 into the main branch. You then updated your local main branch with `git pull`.
  How should you now correctly merge feature2 into the main branch?
> <details>
> <summary>Answer</summary>
> You can open a PR directly from feature2 into the main branch. If there are no conflicts, the PR can be merged.
>
> If there are conflicts, the best approach is to run `git rebase master` while on the feature2 branch,
> resolve the conflicts locally in the affected files,
> and use `git rebase --continue` after resolving them.
> 
> Then update the branch on GitHub using `git push --force` or `git push --force-with-lease`
> (`--force` is needed because rebasing rewrites the branch's commit history).
> The PR will update automatically and will no longer show conflicts (a PR is always relative to the branch's current state, not its initial state).
> </details>

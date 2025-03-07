Git Mirror Updater
====

This script is used to clone a git repo and push it with all branches to another target repo.
In SUTURO, we use this to fully mirror our Code on the GitHub Repositories to a local Git server.

The git_updater script expects a textfile which maps from the source to the target repos.
Every line in the textfile represents one mapping.
It has to be in the following format:
git@github.com:SUTURO/REPONAME.git,git@ANOTHERHOST:ANOTHERORG/REPONAME.git

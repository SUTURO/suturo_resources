#!/bin/bash

# Check if the input file is provided
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <repos-list-file>"
  exit 1
fi

# Read the input file
repos_list_file=$1

# Loop through each line in the file
while IFS=, read -r source_repo remote_repo; do
  if [ -z "$source_repo" ] || [ -z "$remote_repo" ]; then
    echo "Invalid entry: $source_repo, $remote_repo"
    continue
  fi

  # Extract the repository name from the source repository URL
  repo_name=$(basename "$source_repo" .git)

  echo "Processing $repo_name ..."

  # Step 1: Clone the repository with all branches and tags
  git clone --mirror "$source_repo" "$repo_name"

  # Step 2: Change to the cloned repository directory
  cd "$repo_name" || { echo "Failed to change directory to $repo_name"; exit 1; }

  # Step 3: Add the new remote repository if it doesn't exist already
  if ! git remote | grep -q origin; then
    git remote add origin "$remote_repo"
  else
    git remote set-url origin "$remote_repo"
  fi

  # Step 4: Fetch all branches and tags from the source repository
  git fetch --all

  # Step 5: Push all branches and tags to the new remote repository
  git push --mirror

  # Step 6: Move back to the parent directory
  cd ..

  # Step 7: Remove the cloned repository to save space
  rm -rf "$repo_name"

  echo "Finished processing $repo_name."
done < "$repos_list_file"

echo "All repositories processed."

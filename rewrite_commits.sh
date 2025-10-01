#!/bin/bash

# Rewrite commit messages using git filter-branch
git filter-branch -f --msg-filter '
case "$GIT_COMMIT" in
    # Map old commit hashes to new messages (we'll use the content to identify)
    *)
        # Get the current commit message
        cat
        ;;
esac
' --all

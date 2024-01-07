#
# Applies the file-prepare-commit-msg hook to all Git repositories accessible from the current directory.
# This hook prepends the commit message with the branch name.
# To use the script, run it with no parameters to add the hook or 'remove' to remove the hook.
#

HOOK_URL="https://gist.githubusercontent.com/wolf6101/f1857a41f5898328b7e5eef2686974b9/raw/7abf19169c8c6d36144ab5d84f371854958135f0/prepare-commit-msg"

iterate_directories() {
    callback=$1
    callback_run=false

    # Iterate over all directories and its subdirectories in the current directory
    for dir in $(find . -type d)
    do
        dir=${dir%/} # Remove the trailing slash from the directory name

        # Check if the directory is a Git repository
        if [ -d "$dir/.git" ]
        then
            "$callback" "$dir"
            callback_run=true
        fi
    done

    if [ "$callback_run" = false ]
    then
        echo "No git repositories found."
    fi
}

remove_hook() {
    dir=$1

    rm "$dir/.git/hooks/prepare-commit-msg"
    echo "Removed hook from $dir/.git/hooks/prepare-commit-msg"
}

add_hook() {
    dir=$1

    # Creates hooks folder if doesn't exists
    mkdir -p "$dir/.git/hooks"

    cp hook "$dir/.git/hooks/prepare-commit-msg"
    echo "Added hook to $dir/.git/hooks/prepare-commit-msg"
}

remove_hooks() {
    iterate_directories remove_hook
}

add_hooks() {
    curl -s "$HOOK_URL" -o hook
    chmod +x hook # Make the hook executable
    iterate_directories add_hook
    rm hook # Remove the temporary hook file
}

if [ "$1" = "remove" ]
then
    remove_hooks
else
    add_hooks
fi
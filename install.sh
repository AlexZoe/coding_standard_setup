#!/bin/bash

SCRIPT_DIR="$(dirname "$(realpath "$0")")"
WORK_DIR=$(pwd)
REPO_DIR=""

print_help() {
  echo "USAGE: ./install.sh -r git-repository"
  echo ""
  echo "OPTIONS"
  echo "  -h, --help    display this message and exit"
  echo "  -r, --repo    path to git repository to set up"
  echo "  -l, --lint    setup clang-format (only required once)"
  echo ""
}

while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    -h|--help)
      PRINT_HELP=1
      shift
      ;;
    -r|--repo)
      REPO_DIR="$2"
      shift
      shift
      ;;
    -l|--lint)
      SETUP_LINTER=1
      shift
      ;;
    *)
      shift
      ;;
  esac
done

if [[ $PRINT_HELP || ( ! $SETUP_LINTER && ! $REPO_DIR ) ]]; then
  print_help
  exit 0
fi

if [[ $SETUP_LINTER ]]; then
  ln -sf $SCRIPT_DIR/dot-files/clang-format $HOME/.clang-format
fi

if [[ $REPO_DIR ]]; then
  # Adjust path to be relative to the directory containing this script
  if [[ "$REPO_DIR" != /* ]]; then
    REPO_DIR=$WORK_DIR/$REPO_DIR
  fi
  cd $REPO_DIR

  if [[ $(git status &> /dev/null; echo $?) != 0 ]]; then
    echo "$REPO_DIR is not a git repository"
    exit 1
  fi

  git config commit.template "$SCRIPT_DIR/dot-files/gitmessage"
  for hook in $(ls $SCRIPT_DIR/git-hooks); do
    ln -sf $SCRIPT_DIR/git-hooks/$hook .git/hooks/
  done
fi

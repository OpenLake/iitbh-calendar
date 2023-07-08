#!/usr/bin/env sh

_help(){
  printf "usage: ./deploy.sh -u <USERNAME> [-r <REPO>] [-d <DOMAIN>] [-h] [-y]\n"
  printf "\t -d Custom domain name\n"
  printf "\t -h Display this help\n"
  printf "\t -r GitHub repo name\n"
  printf "\t -u GitHub username (Required)\n"
  printf "\t -v Be verbose\n"
  printf "\t -y Do not ask confirmation\n"
  exit 1
}
# abort on errors
set -e

while getopts "yvhd:u:r:" opt; do
  case $opt in
    d) DOMAIN="$OPTARG"
    ;;
    u) USERNAME="$OPTARG"
    ;;
    r) REPO="$OPTARG"
    ;;
    y) YES="YES"
    ;;
    v) VERBOSE="YES"
    ;;
    h)
      _help
    ;;
    \?)
      _help
    ;;
  esac
done

if [ -z "$USERNAME" ]; then
  echo "User is required" >&2
  _help
fi

# Remove existing build directory if it exists
if [ -d "dist" ]; then
  if [ "$YES" ]; then
    printf "'dist' directory already exists.\nOverwriting it"
    rm -rf dist
  else
    printf "'dist' directory already exists.\n"
    read -p "Do you want to overwrite it [y/N]" ANS
    case $ANS in
      [Yy]* )
        rm -rf dist
        ;;
      * )
        printf "Aborting\n"
        exit
        ;;
    esac
  fi
fi

# build
if [ -z "$VERBOSE" ]; then
  printf "Building..."
  npm run build > /dev/null 2>&1
  printf "\n"
else
  npm run build
fi

# navigate into the build output directory
cd dist

# if you are deploying to a custom domain
if [ -n "$DOMAIN" ]; then
  echo $DOMAIN > CNAME
fi

if [ -z "$VERBOSE" ]; then
  git init > /dev/null
  git checkout -b main > /dev/null 2>&1
  git add -A > /dev/null
  git commit -m 'deploy' > /dev/null 2>&1
else
  git init
  git checkout -b main
  git add -A
  git commit -m 'deploy'
fi

if [ -z "$REPO" ]; then
  # if you are deploying to https://<USERNAME>.github.io
  printf "Running\n\tgit push -f git@github.com:${USERNAME}/${USERNAME}.github.io.git main\n"

  if [ -z "$VERBOSE" ]; then
    git push -f git@github.com:${USERNAME}/${USERNAME}.github.io.git main > /dev/null 2>&1
  else 
    git push -f git@github.com:${USERNAME}/${USERNAME}.github.io.git main
  fi

  printf "Your instance is live at: https://${USERNAME}.github.io\n"
else
  # if you are deploying to https://<USERNAME>.github.io/<REPO>
  printf "Running\n\tgit push -f git@github.com:${USERNAME}/${REPO}.git main:gh-pages\n"

  if [ -z "$VERBOSE" ]; then
    git push -f git@github.com:${USERNAME}/${REPO}.git main:gh-pages > /dev/null 2>&1
  else
    git push -f git@github.com:${USERNAME}/${REPO}.git main:gh-pages
  fi

  printf "Your instance is live at: https://${USERNAME}.github.io/${REPO}\n"
fi

cd -

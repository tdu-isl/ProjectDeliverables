#!/usr/bin/env bash

set -eu
source utils.sh
clear

declare answer=''
declare -a array=()
declare -r MAIN_REPO_DIR=$(get_current_script_dir)
declare -r REPO_DIR_NAME=$(echo $MAIN_REPO_DIR | awk -F/ '{print $NF}')

cd $MAIN_REPO_DIR/

while true; do
    read_line info "成果物リポジトリ名を入力してください" tip '例: sub-repo'
    if git remote | grep -sq $answer; then
        color_print warn "リモート名$answerはすでに存在しています"
    else
        break
    fi
done
declare -r repo_name=$answer

read_line info '成果物リポジトリのURLを入力してください' tip '例: https://github.com/ユーザ名/リポジトリ.git'
declare -r sub_repo_url=$answer

while true; do
    read_line info "作業用ブランチ名を入力してください" tip '例: add-sub-repo'
    if git branch | grep -sq $answer; then
        color_print warn "ブランチ$answerはすでに存在しています"
    else
        break
    fi
done
declare -r work_branch=$answer

read_line info "管理用リポジトリ${REPO_DIR_NAME}のどこに置きますか?" tip '例: 2021/GroupA'
declare -r sub_repo_dir=$answer

########## ########## ########## ########## ########## ########## ########## ########## ########## ##########
echo ''; print_divider; echo ''

color_print info "ローカルリポジトリ${REPO_DIR_NAME}を更新します"
git pull
color_print info "作業ブランチ${work_branch}を作ります"
git switch -c $work_branch
color_print info "成果物リポジトリを${repo_name}という名前で参照します"
git remote add $repo_name $sub_repo_url
color_print info '成果物リポジトリからデータを取得します'
git fetch $repo_name
color_print info 'データをマージします'
git merge -s ours --no-commit --allow-unrelated-histories "$repo_name/main"

mkdir -p "$MAIN_REPO_DIR/$sub_repo_dir"
cmd="git read-tree --prefix=$sub_repo_dir/ -u $repo_name/main"
eval "$cmd"

read_line info 'commitメッセージを入力してください'
git commit -m "$answer"

color_print info "参照するリモートリポジトリ${repo_name}を削除します"
git remote rm $repo_name
color_print info "========== 管理用リポジトリ${REPO_DIR_NAME}の状況 =========="
color_print -p info '関連付けたリモート:'
git remote -v
color_print -p info '全てのブランチ:'
git branch -a

########## ########## ########## ########## ########## ########## ########## ########## ########## ##########
echo ''; print_divider; echo ''

color_print info "これまでの作業内容を、リモート管理リポジトリの${work_branch}ブランチにプッシュします。"
git push -u origin $work_branch

color_print info "プッシュが完了しました。"
color_print info "mainブランチに切り替え、ローカルの作業ブランチ${work_branch}を削除します"
git switch main
git branch -D $work_branch
# git push origin --delete add-sub-repo

color_print info 'これからは、Githubで手動でPull Requestを作成してください'
color_print info 'マージが終わったら、リモートの作業用ブランチを削除してください(Pull Requestの画面でも削除できます)'

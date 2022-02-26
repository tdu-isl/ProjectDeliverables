# ProjectDeliverables

## このリポジトリについて

このリポジトリは、P講習などの成果物を管理するため作られたものです。  
個人またはチームで作ったものを、コピーという形でここに取り入れます。
- 管理リポジトリ: このリポジトリ`ProjectDeliverables`を指します
- 成果物リポジトリ: 管理リポジトリに統合するリポジトリのこと

統合作業をする前に、成果物リポジトリのURLを取得してください。
成果物リポジトリは、publicになっているか、自分がアクセスできるようにしてください。
成果物リポジトリのコミット履歴はそのまま残ります。

## リポジトリ統合のやり方(説明なし)

ブランチ名`add-sub-repo`、リモートリポジトリの別名`sub-repo`は適宜変更してよい
```shell
cd 管理リポジトリProjectDeliverablesのパス
git pull

git switch -c add-sub-repo
git remote add sub-repo 成果物リポジトリのURL
git fetch sub-repo
git merge -s ours --no-commit --allow-unrelated-histories sub-repo/main
mkdir -p 成果物を置くディレクトリ
git read-tree --prefix=sub-dir/ -u sub-repo/main
git commit -m "コミットメッセージ"
git remote rm sub-repo

git remote -v
git branch -a
git push -u origin add-sub-repo

問題なくできたら、Githubでadd-sub-repoブランチからPull Requestを作成して、mainブランチへマージしてください

最後に、作業用のブランチを削除
git branch -D add-sub-repo              # ローカルの方を強制削除
git push origin --delete add-sub-repo   # リモートの方を削除
```

## リポジトリ統合のやり方(説明つき)

```shell
cd 管理リポジトリProjectDeliverablesのパス
git pull

git switch -c 作業用ブランチ名
    # 「git checkout -b　ブランチ名」もOKです
    # 例として、作業用ブランチ名を「add-sub-repo」とします

git remote add 統合元を表す任意の名前 統合元のURL
    # URLは.gitで終わるものです。リポジトリのページ -> 緑色のCodeボタン -> HTTPから見れます
    # 例として、リモート名をsub-repoとします

git fetch sub-repo
    # ここでいつくかの新しいリモート追跡用のブランチが生成されます。こういう感じです　↓
    # * [new branch]      main       -> sub-repo/main
    # 新しく生成されたものから１つ選びます
    # git branch -rで、もう一度リモート追跡用のブランチを確認できます

git merge -s ours --no-commit --allow-unrelated-histories sub-repo/main
    # sub-repo/mainの内容を取り入れます
    # 「-s ours」 オプションについては参考サイの２つ目を見てください
    # 問題がなければ、「Automatic merge went well; stopped before committing as requested」と出力されます

mkdir 統合元リポジトリを置くディレクトリ
    # 例として、ディレクトリ名をsub-dirとします

git read-tree --prefix=sub-dir/ -u sub-repo/main
    # ２カ所を適宜置き換えてください：ディレクトリ名、ブランチ名

git commit -m "コミットメッセージ"
    # コミットすることでマージが完了になります

git remote rm sub-repo
    # 適宜置き換えましょう
    # 一番最初に追加したリモートを削除します（fetchで取得したリモート追跡ブランチも勝手に削除されます）

# 登録しているリモートや、ブランチを確認して、push！
git remote -v
git branch -a
git push -u origin add-sub-repo
# ブランチ名を適宜置き換えましょう
# 最後に作業用ブランチを、mainブランチにマージします（Pull Request利用）
# Githubのリポジトリページで行います。マージ完了時に作業用ブランチも削除してください。

最後に、作業用のブランチを削除
git branch -D add-sub-repo              # ローカルの方を強制削除
git push origin --delete add-sub-repo   # リモートの方を削除

########## ########## ########## ########## ########## ##########
# (Pull Request利用することがおすすめ)
# PRを利用せずに、ローカルのmainブランチにmergeしてから、リモートのmainブランチにpushしてもOKです。
# git switch main または git checkout main
# git merge add-sub-repo
# git push -u origin main
```

### スクリプトを利用

作業を簡単にするために、Linux/MacOS用のShellScriptを作りました。  
使い方は以下の通りです。指示に従って入力すればOKです。
```shell
cd 管理リポジトリProjectDeliverablesのパス
./merge_sub_repo.sh
```

### その他のやり方

`git merge`の`subtree`オプションや、`git subtree`を使っても同じことができます。  
詳しくは参考の２つ目＆５つ目６つ目のサイトを参照してください。

## 参考サイト

- [Gitのサブツリーのマージについて - Github Docs](https://docs.github.com/ja/get-started/using-git/about-git-subtree-merges)
- [Git のマージ戦略のオプションとサンプル](https://www.atlassian.com/ja/git/tutorials/using-branches/merge-strategy)
- [2つのGITリポジトリを統合する方法](https://progzakki.sanachan.com/develop-software/maintenance/integrate-git-repositories/)
- [複数のGitリポジトリを一つにまとめる](https://qiita.com/hellscare/items/bad5021964f529d6f690)
- [gitリポジトリの統合](https://qiita.com/CORNER/items/2e608f1091f305794f0a)
- [git subtree の使い方メモ](https://coffee-nominagara.com/git-subtree-memo)

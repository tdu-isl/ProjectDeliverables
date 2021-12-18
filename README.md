# ProjectDeliverables

## このリポジトリについて

このリポジトリは、P講習などの成果物を管理するため作られたものです。  
個人またはチームで作ったものを、コピーという形でここに取り入れます。

## リポジトリの統合のやり方

このリポジトリを一度ローカルにクローンしてから作業を進めます。  
また、統合元のリポジトリは、URLのみ取得すればよく、クローン＆forkなどの操作は必要ないです。  
なお、統合元のリポジトリのコミット履歴はそのまま残ります。

```shell
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
# Githubのリポジトリページで行います

# PRを利用せずに、ローカルのmainブランチにmergeしてから、リモートのmainブランチにpushしてもOKです。
# git switch main または git checkout main
# git merge add-sub-repo
# git push -u origin main
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

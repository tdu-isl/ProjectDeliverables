# P講習課題

## 環境構築

pipenvを使って仮想のPython環境を入れています。  
まずPythonをインストールしてから、下のコマンドでローカルに開発環境を作ってください。

```shell
pip install pipenv   # pipenvをインストール

cd リポジトリを保存する場所
git clone https://github.com/yechentide/p-course.git
cd p-course
pipenv install
```

## 作業について

基本的に`main`ブランチで作業しない方がいいでしょう。  
環境を用意できたら、作業用のローカルブランチに切り替えてコードを書きます。  
作業が一段落したら、このローカルブランチをプッシュしましょう。  
例：

```shell
cd リポジトリのルートディレクトリ
git checkout -b 適当なブランチ名
git branch   # 今いるブランチを確認

コーディング

git status   # 今の状況を確認
git add -n .   # git addの前に、一度何が追加されるかを確認
git add .   # 1行上で表示されるものは問題なければ、これを実行
git commit -m "適切なメッセージ(作業内容とか)"

# git add, git commitを複数回やったあと、一気にpushしてもOK
git push origin 先ほど作ったローカルブランチ
```

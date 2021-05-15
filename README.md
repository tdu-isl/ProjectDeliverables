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

### 仮想環境について

pipでライブラリとかを直接インストールできますが、グローバルインストールなので、  
それを避けてプロジェクトごとにインストールしたい。そのためにpipenvを使っています。  
デフォルトの仮想環境の場所は：

- Windowsは`%userprofile%\.virtualenvs`
- LinuxやMacOSは`$HOME/.local/share/virtualenvs`

となっています。  
場所を変えたければ、[こちら](https://qiita.com/y-tsutsu/items/54c10e0b2c6b565c887a#%E4%BB%AE%E6%83%B3%E7%92%B0%E5%A2%83%E9%96%A2%E9%80%A3%E3%81%AE%E6%93%8D%E4%BD%9C)を参照してください。

### 実行の仕方

`fe`と`be`は、Pipfileファイルの中で定義したものです

```shell
pipenv run fe
pipenv run be
```

## 作業について

適当にやろう  
~~基本的に`main`ブランチで作業しない方がいいでしょう。~~  
~~環境を用意できたら、作業用のローカルブランチに切り替えてコードを書きます。~~  
~~作業が一段落したら、このローカルブランチをプッシュしましょう。~~  
~~例：~~

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

## ディレクトリ構造

```shell
p-course
├── Pipfile             # Python仮想環境用
├── Pipfile.lock        # Python仮想環境用
├── README.md
├── ssl
│   ├── fullchain1.pem  # 証明書
│   └── privkey1.pem    # SSL 秘密鍵
├── backend
│   ├── api.py
│   ├── db
│   │   └── db.sqlite3
│   └── routers
│       └── auth.py
└── frontend
    ├── css
    ├── main.py
    └── templates
        └── login.html
```

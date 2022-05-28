# 構成
```
├── README.md
├── chrome-customize  chrome専用拡張機能
└── html_prototype    アプリ本体
    ├── app
    └── run.py        実行スクリプト
```

# 環境設定
### バージョン
下記バージョンは参考程度で、必ずしも一致させる必要はありません。

python: `3.9.7`

flask: `2.0.2`

Flask-SQLAlchemy: `2.5.1`

SQLite3: `3.36.0`

### 拡張機能設定
クローン後、google chrome の拡張機能管理画面からデベロッパーモードを有効にして「パッケージ化されていない拡張機能を読み込む」から `psemi_GroupC/chrome-customize` を選択する。

### 構築方法
**SQLite3 と python のインストール方法は省略**

前提としてターミナルから
```
$ sqlite3 --version
$ python --version
```
でバージョン情報が表示されていればOK

1.
パッケージのインストール
```
$ pip install flask-sqlalchemy
```
または
```
$ pipenv install flask-sqlalchemy
```
で `flask-sqlalchemy` をインストール

2. 環境ごとにDBの設定を行う（最初の一回だけでOK）
`psemi_GroupC/html_prototype/app/` のディレクトリで下記の通り実行
```
$ python
>>> from app.app import db
>>> db.create_all()
```
3. アプリを実行
```
$ python run.py
```

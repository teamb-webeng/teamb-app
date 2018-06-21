# teamb-app

## 使い方

レポジトリをcloneした後、DB接続の設定ファイル(main/config.py)を作成する。
よくわかんないけどKeyとか公開するのはあれなので、config.pyはgitの管理から外してある。
config.pyの中身はslackで送ります。

ターミナルでpythonをインタラクティブモードで立ち上げる。

```bash:terminal
python
```

立ち上がったら以下を実行。

```bash:terminal
from main.models import init_db
init_db()
```

これでDBが作成される。
デフォルトで管理者ユーザーが作成されるようにしてある。
管理者ユーザーの情報は以下の通り。

```
username : administrator
email : admin@example.com
password : admin
```

以上が終わったら、ターミナルで`teamb-app`ディレクトリに入って以下を実行。

 ```bash:terminal
python manage.py
 ```
これでブラウザで`localhost:5000`を見に行くとアプリが立ち上がっているのが確認できる。


## ライブラリ

requirements.txtに必要なライブラリ一覧が記載されている。
pipでインストールする場合には以下を実行。

```bash:terminal
pip install -r requirements.txt
```

自分で新しくライブラリを追加した場合にはここに追記してください。

## ディレクトリ構成

* main
    * static(css,JS)
    * templates(html)
    * utils(問題生成用スクリプト置き場)
    * __init.py__(application,dbの初期化)
    * models.py(モデル)
    * views.py(ルーティング、コントローラ)
    * config.py(各自で作成)
* manage.py(アプリ実行用スクリプト)
* requirements.txt(ライブラリ一覧)

内部の仕組みは次の通り。

1. main.__init__.pyでappとdbの初期化
1. このappをviews.pyで読んでルーティング
1. ルーティングしたappをmanage.pyで実行

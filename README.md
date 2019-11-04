# 漢方のセイシンドー

## 開発環境

```shell
# 仮想環境の有効化
$ source myenv/bin/activate

# 仮想環境の無効化
(myenv) $ deactivate
```

アプリケーションサーバーの起動 (with auto-reload)

```shell
$ FLASK_DEBUG=1 python -m flask run
```

## 全体TODO
* [x] アクセスページの作成
* [x] 病気のご相談ページの作成
* [x] 症状一覧
* [x] リンクが無かったページに対してリンクを貼る (30min)
* [ ] 問診票の実装 http://www.tcm-jp.com/ivs/itvs.html
  * [ ] 画面の実装 (3hour)
  * [ ] 問診票記入後は、メールを送る。(30min)
  * 問診票は、お客さんから相談があったとき、メールにURLを貼り付けて送っています。(直リンク不要)
  * 問診票から、原因や使用する漢方薬・価格を診断結果としてメールで送ります。
  * 管理用のページは必要なし。(カルテで管理)
* [ ] 購入ページ (1.5hour) http://www.tcm-jp.com/odf/odrpc.html
  * 購入される方には、「注文書」のURLを貼り付けて再度メールを送ります。
  * そこで、代引きや代引きカード払いとか、オンラインカード決済を選んで貰い、オンラインカード決済の場合のみ再度決済会社のURLを送って決済を済ませて貰います。
* [ ] https化 (2hour)
  * http -> https のリダイレクト
* [ ] ドメインの設定
* [ ] CircleCIからのデプロイ処理 (2hour)
* [ ] 「アクセス」のところで「お車でお越しの場合」の項を全て削除して貰えますか？これを書いた時点と今とでは、状況が目まぐるしく変わっているので、「電車でお越しの方」のみの掲載にしようと思います。
* [ ] 購入後に送るページ http://www.seisindo.com/kanryou.htm
* [ ] 問診票送信完了ページ http://www.seisindo.com/sousin.htm

## 方向転換後

`./pug` にすべてが入っている。

### 開発時
```
$ pwd
/Users/showwin/Develop/Python/seisindo/pug/src

$ cp -r ./static ../dist

$ pug -w . -o ../dist -P
# ↑でwatchしてdistに吐き出す
```


Pythonでホスティングしなくなったので、PugでHTMLを出力してそれを渡すようにする。
* [x] 「アクセス」のところで「お車でお越しの場合」の項を全て削除して貰えますか？これを書いた時点と今とでは、状況が目まぐるしく変わっているので、「電車でお越しの方」のみの掲載にしようと思います。
* [ ] 購入後に送るページ http://www.seisindo.com/kanryou.htm
* [ ] 問診票送信完了ページ http://www.seisindo.com/sousin.htm
* [x] SPになったときにMENUのトグルが動かない

## 相談箇所
* [ ] サイドバーの病気一覧をいい感じにグルーピングしてもらう

## サーバーの中
IP: 18.176.140.126

```shell
$ nohup sudo FLASK_DEBUG=1 python3 -m flask run --port 80 --host 0.0.0.0 &
```

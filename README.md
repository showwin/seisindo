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


## リンクさせていないけど使っているHTML

* s/notice.html
* info003.htm


## サーバーの中

```shell
$ nohup sudo FLASK_DEBUG=1 python3 -m flask run --port 80 --host 0.0.0.0 &
```

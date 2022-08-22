# reCAPTCHA-Practice

## how to start

1. 手元に落としてきて、次のコマンドを実行する ※1

```sh
$ python -m recaptcha_practice
```

2. `http:localhost:8080` にアクセスする

※1  
`recaptcha_practice/.sitekey` と `recaptcha_practice/.secretkey` がないとエラーになります。  
ローカルで動かす場合は、ご自身で [google](https://www.google.com/recaptcha/admin/create) からキーを取得し、次のように保存してください。
- サイトキー -> `recaptcha_practice/.sitekey`
- シークレットキー -> `recaptcha_practice/.secretkey`

# README

## TODO

- D: actionflow単体
- D: cloud-fundion(v2) with terraform
- cloud-run with terraform
- gke with terraform
- gke with terraform and actionflow(CI/CD)
- yamaha config CI/CD
- create slack app

## slack からの API 自動化フロー(IF: http/slack/hogehoge/... を slack に集約できる)

```bash
slack
-> cloud function/cloud run（関数ベースとコンテナベースの違い　いずれも terraform でデプロイ可能）
-> github api(認証/認可は github apps)[github api "create a workflow dispatch event" workflow_id=hoge.yml]
-> github actions（cloud function で inputs の POST パラメータで環境変数指定）

slack
-> microsoft graph api

slack/kintone
-> cloud function/cloud run
-> jira api
```

## ドキュメント管理

```bash
docmentbranch - workbranch
```

- workbranch で作業をする
- documentbranch へ PR を送る

## デプロイ自動化(NW コンフィグ設定やら IaC やら)

```bash
deploybranch - workbranch
```

- workbranch でコマンドを作る
- deploybranch へ PR
- 承認されると自動デプロイ

## 生成 UI(Azure API over chatgpt 3.5)を利用した slack bot

api 経由でないと chatgpt 使えないし作りましょう

## 勉強

- <https://zenn.dev/tmknom/articles/github-apps-token>
- <https://developers.bookwalker.jp/entry/2023/03/15/110000>
- <https://tech.ginco.io/post/ginco-engineer-meetup-2018-cloud-functions/#cold-start%E3%81%AE%E6%94%B9%E5%96%84>
- <https://blog.g-gen.co.jp/entry/using-terraform-via-github-actions>
- <https://getbetterdevops.io/google-cloud-functions-with-terraform/>
- <https://engineering.nifty.co.jp/tag/slack>
- <https://engineering.nifty.co.jp/blog/18967>

## slack 2nd generation platform

slack deploy だけで typescript をデプロイ可能

- <https://api.slack.com/automation/cli/CI-CD-setup>

どうやら slack app の trigger がいろいろあるらしい
その中でも event trigger の app_mensioned を理よすると @myapp とかで workflow がスタートする
webhook や Link、schedule などもある

## やること

あ

# ベストプラクティス

- S3/GCS に tfstate ファイルを保存するための terraform コードは別で管理する
- provider.tf, version.tf, backend.tf については、最低限分けて書く
- variables.tf に変数をまとめる terraform.tfvars は自動で読み込まれる
- plan で出力される変数については、output.tf で指定される

## 環境ごとのフォルダ構成

環境ごとに Project やアカウントを変えること

```bash
-- SERVICE-DIRECTORY/
   -- OWNERS
   -- modules/
      -- <service-name>/
         -- main.tf
         -- variables.tf
         -- outputs.tf
         -- provider.tf
         -- README
      -- ...other…
   -- environments/
      -- dev/
         -- backend.tf
         -- main.tf
      -- qa/
         -- backend.tf
         -- main.tf
      -- prod/
         -- backend.tf
         -- main.tf
```

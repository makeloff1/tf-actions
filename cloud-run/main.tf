terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.34.0"
    }
  }
}

resource "random_id" "default" {
  byte_length = 8
}

resource "google_storage_bucket" "default" {
  # Every bucket name must be globally unique
  name                        = "${random_id.default.hex}-gcf-source" 
  location                    = "US"
  uniform_bucket_level_access = true
}

data "archive_file" "function_archive" {
  # 圧縮方式
  type = "zip"
  # main.pyの存在するディレクトリ
  source_dir = "randomgen"
  # 関数ソースコードのルートディレクトリ(main.pyと同じ階層)でなければならない
  output_path = "randomgen/function-source.zip"
}

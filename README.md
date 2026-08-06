# マイリワードポータル プロトタイプ

ロイヤリティアプリのUIプロトタイプ(フレームワーク不使用)。モジュール単位でクライアントに合わせて機能を選べる、というビジネス展開を想定し、3つの構成を用意している。

## 3種類のビルド

- **`index.html`(フル版)** — https://ayumunomoto.github.io/myreward-portal-demo/
  通常/スポーツ観光/わかおしっ！の3モード切替、ガチャ、キャラクター演出・ストーリーゲージ、QR決済・チェックイン、リワード交換(カテゴリ別・共通ポイント交換)、アンケートチャレンジ、プッシュ通知デモ、利用履歴。下部ナビで各画面を行き来する。
- **`lite.html`(コア版)** — https://ayumunomoto.github.io/myreward-portal-demo/lite.html
  モードを1本化し、以下6モジュールのみに絞った構成:
  ポイント基盤(残高カード+履歴) / リワード交換(カテゴリ別・共通ポイント交換) / QR決済・チェックイン / チャレンジ(アンケート含む) / プッシュ通知。下部ナビで各画面を行き来する。
- **`hub.html`(ハブ版)** — https://ayumunomoto.github.io/myreward-portal-demo/hub.html
  コア版と同じ6モジュール構成だが、下部ナビを置かず、ホーム画面(残高カード)から必要な画面へ遷移する構成。残高カード内に「QRを読む」ボタンと「履歴を見る」ボタン、チャレンジ/リワードは各プロモカードの「すべて見る」から遷移する。各画面には戻るボタンを設置。

## コード構成(共通更新の仕組み)

3系統に共通するロジック・スタイル・データ(状態管理、QR決済フロー、リワード交換フロー、チャレンジ、履歴、プッシュ通知、共通ポイント交換ロゴ、写真素材など)は `assets/core.css` と `assets/core.js` に集約している。フル版だけが使うモード切替・ガチャ・キャラクター演出・ストーリーゲージ・桜演出は `assets/theme-switch.css` / `assets/theme-switch.js` に分離し、`index.html` だけが読み込む。

```text
assets/
  core.css           全ビルド共通のスタイル
  core.js            全ビルド共通のロジック・データ・initApp()
  theme-switch.css    フル版のみ: モード切替/ガチャ/キャラクター演出のスタイル
  theme-switch.js     フル版のみ: 同上のロジック・データ(THEMES.sports/wakaoshi 等を core の
                       オブジェクトに Object.assign で追加し、renderThemeChrome 等の一部関数は
                       テーマ対応版で再定義して core の簡易版を上書きする)
index.html    core + theme-switch を読み込む薄いページ(モード切替+下部ナビの構成)
lite.html     core のみを読み込む薄いページ(下部ナビの構成)
hub.html      core のみを読み込む薄いページ + ページ内だけの追加CSS/JS(ハブナビの構成)
build.py      thin wrapperを単一HTMLファイルに束ねるビルドスクリプト(下記参照)
```

**共通ロジックを直したいとき**は `assets/core.css` / `assets/core.js` を1回編集すれば、3ビルドすべてに反映される(ブラウザは `<link>` / `<script src>` で毎回最新のファイルを読み込むため、GitHub Pages 上では commit → push するだけでよい)。フル版だけの見た目・挙動(モード切替やガチャなど)を直したいときは `assets/theme-switch.*` を編集する。各ページ固有のHTML構成(下部ナビ vs ハブナビなど)は各 `.html` ファイル自体を編集する。

### Claude Artifact 用に単一ファイルへ束ねる

Claude Artifact は1ファイルしか受け付けないため、上記の分割ファイルをその場で1ファイルに結合するスクリプトを用意している。

```bash
python3 build.py index.html          # index.standalone.html を生成
python3 build.py lite.html
python3 build.py hub.html
python3 build.py --all /path/to/dir  # 3つまとめて生成
```

`assets/core.*` や `assets/theme-switch.*` を更新したら、Artifactとして配布している版を最新化するために `build.py` を実行し、生成された `*.standalone.html` をArtifactとして再公開する。

## デモ公開(GitHub Pages)

このリポジトリを GitHub にプッシュし、Pages を有効化すると `https://<ユーザー名>.github.io/<リポジトリ名>/` で複数人にURLを配布してデモできる(サブパスの `/lite.html` `/hub.html` も同様)。

```bash
# 1. GitHub上にリポジトリを作成(Web UIまたは gh CLI)
gh repo create <リポジトリ名> --public --source=. --remote=origin --push
# もしくは、Web UIで空のリポジトリを作成した後:
# git remote add origin https://github.com/<ユーザー名>/<リポジトリ名>.git
# git push -u origin main

# 2. GitHub Pages を有効化
# リポジトリの Settings > Pages > Source を「Deploy from a branch」、
# Branch を「main」/「/(root)」に設定して保存。
# 数分後に https://<ユーザー名>.github.io/<リポジトリ名>/ で公開される。
```

## 注意事項

- 「わかおしっ！」モードのキャラクターイラストは和歌山市の公式PRキャラクターの画像を使用している(`assets/theme-switch.js` のみに含まれ、`lite.html`/`hub.html` には一切含まれない)。社外・商用利用には和歌山市への事前相談と利用許諾申請(無償・2年以内)が必要。本プロトタイプはあくまで内部検討用。
- リワードの「共通ポイント交換」(Vポイント/dポイント/PayPayポイント/楽天ポイント)のロゴは、実物ロゴを模した独自デザイン(色・形状のみ参考)であり、各社の公式ロゴデータそのものではない。
- GitHub Pages は無料プランの場合、公開リポジトリでのみ利用可能(=サイトは非公開URLではあるがインターネット上に公開される)。社外に見せたくない情報が含まれていないか確認のうえ公開すること。

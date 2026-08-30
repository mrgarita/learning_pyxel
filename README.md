# learning_pyxel

Python のゲームライブラリ **[Pyxel](https://github.com/kitao/pyxel)** を使って、
ゲーム制作プログラミングを一から学ぶための個人学習プロジェクトです。

完成版のコードをそのまま写すのではなく、各 step のゲームをフェーズに分割し、
「考え方 → 必要な API → コード → 解説」の順に手を動かしながら理解を積み上げます。

## 解説サイト

学習の解説・備忘録は `docs/site/` に静的 HTML として置き、GitHub Pages で公開します。

- **公開 URL：https://mrgarita.github.io/learning_pyxel/**
- **step0 の作品「Star Voyager」（ブラウザでそのまま動きます）：https://mrgarita.github.io/learning_pyxel/site/step0/star_voyager.html**

## 学習ステップ

| step | 内容 |
|---|---|
| step0 | 環境構築と簡単なアニメーション作品。Pyxel の機能を広く浅く体験する |
| step1 | 「お化けに捕まらずにどれだけお菓子を集められるか」ゲーム |
| step2 | 倉庫番（10 ステージ制・タイトル画面つき） |
| step3 | 縦スクロールシューティング（3 ステージ制・中ボス／ボスあり） |
| step4 | 未定（step3 完了後に検討） |

## 開発環境

| 項目 | バージョン |
|---|---|
| Python | 3.12.10 |
| Pyxel | 2.9.9 |

## セットアップ

```bash
pip install pyxel
```

## ディレクトリ構成

```
learning_pyxel/
├── docs/site/          解説 HTML（GitHub Pages で公開）
├── step0/              step0 の作品コード
├── step0-learning/     step0 で学んだことの復習作品
├── CLAUDE.md           Claude Code 向けの作業指針
└── project.txt         学習計画の原本
```

## ライセンス / 素材について

グラフィック・サウンド素材は Pyxel 付属のリソースエディタで自作します。
参考記事や既存ゲームの素材は転載していません。

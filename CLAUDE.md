# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Claude Desktop 導入ハンズオン（Hands-On Tutorial）サイト。メインコンテンツは `index-content.html` に記述され、Home ページの iframe 内で表示される。

## Commands

- `pnpm install` — 依存関係インストール（pnpm 10.4.1 必須、packageManager フィールドで指定）
- `pnpm dev` — 開発サーバー起動（port 3000、HMR 有効）
- `pnpm build` — プロダクションビルド（Vite でクライアント → `dist/public/`、esbuild でサーバー → `dist/index.js`）
- `pnpm start` — プロダクションサーバー起動（`dist/index.js`）
- `pnpm check` — TypeScript 型チェック（`tsc --noEmit`）
- `pnpm format` — Prettier でコードフォーマット

テストフレームワーク（Vitest）は導入済みだがテストファイルは未作成。

## Architecture

フルスタック TypeScript（React + Express）SPA。

```
client/src/       — React 19 フロントエンド（Vite 7）
  pages/          — ページコンポーネント（Home: iframe でチュートリアル表示）
  components/ui/  — shadcn/ui コンポーネント（new-york スタイル）
  contexts/       — ThemeContext（ライト/ダーク）
  hooks/          — useMobile, useComposition など
  lib/utils.ts    — cn() ヘルパー（clsx + tailwind-merge）
server/           — Express サーバー（SPA フォールバック + 静的ファイル配信）
shared/           — クライアント・サーバー共有の定数
```

## Path Aliases

- `@/*` → `client/src/*`
- `@shared/*` → `shared/*`
- `@assets/*` → `assets/*`

## Build & Deploy

- GitHub Pages へ自動デプロイ（main ブランチ push 時）
- `GITHUB_PAGES=true` でビルドすると base URL が `/claude-study/` になる
- デプロイ時に Manus ランタイムと analytics スクリプトは自動除去される
- `index.html` → `404.html` コピーで SPA ルーティング対応

## Styling

- Tailwind CSS 4（`@tailwindcss/vite` プラグイン）
- OKLCh カラースペースによるテーマ変数（`client/src/index.css`）
- Prettier: セミコロンあり、ダブルクォート、末尾カンマ(es5)、2スペースインデント

## Key Notes

- `wouter@3.7.1` にカスタムパッチ適用済み（`patches/` ディレクトリ）
- `__manus__/` は開発用デバッグ収集ツール（プロダクションビルドから除外）
- 環境変数: `VITE_OAUTH_PORTAL_URL`, `VITE_APP_ID`, `PORT`（デフォルト 3000）

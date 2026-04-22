# Plot Figure Experiment

这个仓库是 `D:\Code\autoReaserch\web` 的 GitHub Pages 发布仓库。

- 仓库地址：`https://github.com/hamster111111/plot-figure-experiment`
- 站点地址：`https://hamster111111.github.io/plot-figure-experiment/`
- 本地源目录：`D:\Code\autoReaserch\web`
- 发布目录：`work/`

## 目录结构

```text
plot-figure-experiment/
├── .github/workflows/deploy.yml
├── scripts/
│   ├── gen_index.py
│   ├── publish.ps1
│   ├── sync_from_workspace.py
│   └── update_site.ps1
└── work/
```

## 最省事的发布方式

在仓库根目录执行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/publish.ps1 -Message "update pages"
```

这条命令会自动做 4 件事：

1. 把 `D:\Code\autoReaserch\web` 同步到 `work/`
2. 重新生成 `work/index.html`
3. 提交 git 变更
4. 推送到 `origin/main`

推送后 GitHub Actions 会自动部署 Pages。

## 只更新本地站点，不推送

```powershell
powershell -ExecutionPolicy Bypass -File scripts/update_site.ps1
```

## 只提交，不推送

```powershell
powershell -ExecutionPolicy Bypass -File scripts/publish.ps1 -Message "update pages" -NoPush
```

## 说明

- `work/` 是最终发布目录，站点内容会从这里部署。
- GitHub Actions 会在远端再生成一次 `work/index.html`。
- 如果 `web/` 没有变化，`publish.ps1` 会直接提示 `No changes to publish.` 并退出。

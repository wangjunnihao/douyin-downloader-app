# 抖音视频下载器 Android App

基于 Kivy 框架开发的抖音视频下载应用。

## 功能

- ✅ 输入抖音链接下载视频
- ✅ 去水印支持
- ✅ 进度显示
- ✅ 简单易用的界面

## 本地运行（调试）

```bash
# 安装依赖
pip install -r requirements.txt

# 运行
python main.py
```

## 构建 APK

### 方式 1：GitHub Actions（推荐）

1. 点击本仓库的 **Actions** 页面
2. 选择 **Build Android APK**
3. 点击 **Run workflow**
4. 构建完成后在 Artifacts 中下载 APK

### 方式 2：本地打包

```bash
# 安装 buildozer
pip install buildozer

# 打包
buildozer android debug
```

APK 文件位于 `bin/` 目录下。

## 配置说明

- 下载保存路径：`/storage/emulated/0/Download/`
- 支持 Android 5.0+

## 注意事项

本工具仅供学习和个人使用，请遵守抖音服务条款，不要批量抓取或商业使用。

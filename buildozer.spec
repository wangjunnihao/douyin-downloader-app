[app]

title = 抖音下载器
package.name = douyin_downloader
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy,requests

orientation = portrait

osx.python_version = 3
osx.kivy_version = 2.1.0

fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.acceptsdklicense = yes

android.archs = arm64-v8a,armeabi-v7a

"""
抖音视频下载器 - Android App
基于 Kivy 框架 + 飞蛙 API
"""

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.switch import Switch
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.clock import Clock
import threading
import os
import re
import requests
import json
from urllib.parse import urlparse

kivy.require('2.1.0')


class DouyinDownloaderApp(App):
    """抖音下载器主应用"""
    
    def build(self):
        """构建 UI"""
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 标题
        title = Label(
            text='[b]抖音视频下载器[/b]',
            markup=True,
            font_size='24sp',
            size_hint_y=None,
            height=50
        )
        layout.add_widget(title)
        
        # 链接输入
        self.url_input = TextInput(
            hint_text='粘贴抖音链接，如：https://v.douyin.com/xxxx',
            multiline=False,
            font_size='16sp',
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.url_input)
        
        # 选项布局
        options_layout = GridLayout(cols=2, size_hint_y=None, height=50)
        
        watermark_label = Label(text='去水印', font_size='16sp')
        self.watermark_switch = Switch(active=True)
        options_layout.add_widget(watermark_label)
        options_layout.add_widget(self.watermark_switch)
        
        layout.add_widget(options_layout)
        
        # 下载按钮
        self.download_btn = Button(
            text='下载视频',
            font_size='18sp',
            size_hint_y=None,
            height=60,
            background_color=(0.2, 0.6, 1, 1)
        )
        self.download_btn.bind(on_press=self.start_download)
        layout.add_widget(self.download_btn)
        
        # 进度条
        self.progress = ProgressBar(max=100, value=0, size_hint_y=None, height=30)
        layout.add_widget(self.progress)
        
        # 状态显示
        self.status_label = Label(
            text='就绪 - 请输入抖音链接',
            font_size='14sp',
            color=(0.5, 0.5, 0.5, 1)
        )
        layout.add_widget(self.status_label)
        
        # 日志滚动区域
        scroll = ScrollView(size_hint_y=1)
        self.log_label = Label(
            text='欢迎使用抖音视频下载器\n',
            font_size='12sp',
            text_size=(Window.width - 40, None),
            halign='left'
        )
        scroll.add_widget(self.log_label)
        layout.add_widget(scroll)
        
        return layout
    
    def log(self, message):
        """添加日志"""
        Clock.schedule_once(lambda dt: self._add_log(message))
    
    def _add_log(self, message):
        self.log_label.text += message + '\n'
    
    def update_status(self, text):
        """更新状态"""
        Clock.schedule_once(lambda dt: self.status_label.__setattr__('text', text))
    
    def update_progress(self, value):
        """更新进度"""
        Clock.schedule_once(lambda dt: self.progress.__setattr__('value', value))
    
    def start_download(self, instance):
        """开始下载"""
        url = self.url_input.text.strip()
        
        if not url:
            self.update_status('请输入抖音链接！')
            return
        
        if 'douyin.com' not in url:
            self.update_status('请输入有效的抖音链接！')
            return
        
        # 禁用下载按钮
        self.download_btn.disabled = True
        self.update_status('开始下载...')
        self.log(f'🔗 链接: {url}')
        
        # 在新线程中下载
        thread = threading.Thread(target=self.download_video, args=(url,))
        thread.start()
    
    def download_video(self, url):
        """下载视频"""
        try:
            self.update_progress(10)
            self.log('📡 正在解析链接...')
            
            # 1. 解析短链接
            real_url = self.resolve_short_url(url)
            self.log(f'✅ 解析成功: {real_url}')
            
            self.update_progress(20)
            self.log('🔍 正在获取视频信息...')
            
            # 2. 获取视频信息
            video_info = self.get_video_info(real_url)
            
            if not video_info or not video_info.get('url'):
                raise Exception('无法获取视频信息')
            
            self.log(f'📹 标题: {video_info.get("title", "未知")}')
            self.update_progress(40)
            
            # 3. 下载视频
            self.log('⬇️ 正在下载视频...')
            file_path = self.download_file(video_info['url'], video_info['title'])
            
            self.update_progress(100)
            self.update_status('✅ 下载完成！')
            self.log(f'💾 已保存到: {file_path}')
            
        except Exception as e:
            self.update_status(f'❌ 下载失败: {str(e)}')
            self.log(f'错误: {str(e)}')
        
        finally:
            Clock.schedule_once(lambda dt: self.download_btn.__setattr__('disabled', False))
    
    def resolve_short_url(self, url):
        """解析短链接"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'
            }
            response = requests.head(url, headers=headers, allow_redirects=True, timeout=10)
            return response.url
        except Exception as e:
            self.log(f'解析短链接失败: {e}')
            return url
    
    def get_video_info(self, url):
        """获取视频信息 - 使用第三方解析接口"""
        
        # 方法1: 使用免费解析接口
        try:
            # 飞蛙解析接口（示例）
            api_url = 'https://api.xingyue520.cn/api/douyin/video'
            params = {'url': url}
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36'
            }
            
            response = requests.get(api_url, params=params, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 200:
                    return {
                        'title': data.get('data', {}).get('title', '抖音视频'),
                        'url': data.get('data', {}).get('url', '')
                    }
        except Exception as e:
            self.log(f'解析接口1失败: {e}')
        
        # 方法2: 尝试直接解析（备用）
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36',
                'Referer': 'https://www.douyin.com/'
            }
            
            # 从 URL 提取视频 ID
            video_id = ''
            if '/video/' in url:
                video_id = re.search(r'/video/(\d+)', url).group(1)
            else:
                # 尝试从页面获取
                response = requests.get(url, headers=headers, timeout=10)
                video_id = re.search(r'"aweme_id":"(\d+)"', response.text)
                if video_id:
                    video_id = video_id.group(1)
            
            if video_id:
                # 调用抖音 API
                api_url = f'https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id={video_id}'
                response = requests.get(api_url, headers=headers, timeout=10)
                data = response.json()
                
                if data.get('aweme_detail'):
                    detail = data['aweme_detail']
                    # 尝试获取无水印地址
                    play_url = detail.get('video', {}).get('play_addr', {}).get('url_list', [''])[0]
                    
                    return {
                        'title': detail.get('desc', '抖音视频')[:50],
                        'url': play_url
                    }
        except Exception as e:
            self.log(f'解析接口2失败: {e}')
        
        # 返回 None 表示解析失败
        return None
    
    def download_file(self, url, filename):
        """下载文件"""
        if not url:
            raise Exception('无效的下载链接')
        
        # 清理文件名
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)[:50]
        if not filename:
            filename = 'douyin_video'
        
        # 保存路径
        save_path = '/storage/emulated/0/Download/Douyin/'
        os.makedirs(save_path, exist_ok=True)
        
        file_path = os.path.join(save_path, f'{filename}.mp4')
        
        self.log(f'📁 保存路径: {file_path}')
        
        # 下载
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, stream=True, timeout=60)
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    if total_size:
                        progress = 40 + int((downloaded / total_size) * 60)
                        self.update_progress(progress)
        
        return file_path


if __name__ == '__main__':
    DouyinDownloaderApp().run()

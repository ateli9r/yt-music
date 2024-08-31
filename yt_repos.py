from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

import os
import yaml
import shutil
import yt_dlp


@dataclass
class VideoInfo:
    '비디오 정보'
    url: str = ''
    videoId: str = ''
    title: str = ''
    author: str = ''
    publishDate: str = ''
    views: int = 0
    length: int = 0
    rating: int = 0
    description: str = ''
    likes: int = 0
    dislikes: int = 0
    categories: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


class YoutubeMusicRepository(ABC):
    @abstractmethod
    def videoInfo(self, videoUrl): '비디오 정보 가져오기'
    
    @abstractmethod
    def videoDownload(self, videoUrl, outputFilePath): '비디오 다운로드'


class YoutubeMusicLocalRepository(YoutubeMusicRepository):
    def videoInfo(self, videoUrl):
        # 비디오 아이디 추출
        sptUrl = videoUrl.split('?v=')[1].split('&')
        videoId = sptUrl[0]

        # 로컬 비디오 정보 경로
        infoFilePath = 'data/local/{}.yml'.format(videoId)
        if not os.path.exists(infoFilePath): return None

        with open(infoFilePath, 'r') as f:
            data = yaml.safe_load(f)
            info = data['videoInfo']

            return VideoInfo(
                url=videoUrl,
                videoId=videoId,
                title=info['title'] if 'title' in info else '',
                author=info['author'] if 'author' in info else '',
                publishDate=info['publishDate'] if 'publishDate' in info else '',
                views=info['views'] if 'views' in info else 0,
                length=info['length'] if 'length' in info else 0,
                rating=info['rating'] if 'rating' in info else 0,
                description=info['description'] if 'description' in info else '',
                likes=info['likes'] if 'likes' in info else 0,
                dislikes=info['dislikes'] if 'dislikes' in info else 0,
                categories=info['categories'] if 'categories' in info else [],
                tags=info['tags'] if 'tags' in info else [],
            )


    def videoDownload(self, videoUrl, outputFilePath):
        # 비디오 아이디 추출
        sptUrl = videoUrl.split('?v=')[1].split('&')
        videoId = sptUrl[0]

        # 비디오 파일 경로
        videoFilePath = 'data/local/{}.mp4'.format(videoId)
        if not os.path.exists(videoFilePath): return None

        # 파일 복사
        shutil.copy(videoFilePath, outputFilePath)


class YoutubeMusicProdRepository(YoutubeMusicRepository):
    def videoInfo(self, videoUrl):
        try:
            with yt_dlp.YoutubeDL() as ydl:
                # 비디오 정보 가져오기
                info = ydl.extract_info(videoUrl, download=False)

                # 비디오 아이디 추출
                sptUrl = videoUrl.split('?v=')[1].split('&')
                videoId = sptUrl[0]

                return VideoInfo(
                    url=videoUrl,
                    videoId=videoId,
                    title=info.get('title'),
                    author=info.get('uploader'),
                    publishDate=info.get('upload_date'),
                    views=info.get('view_count'),
                    length=info.get('duration'),
                    rating=info.get('average_rating'),
                    description=info.get('description'),
                    likes=info.get('like_count'),
                    dislikes=info.get('dislike_count'),
                    categories=info.get('categories'),
                    tags=info.get('tags'),
                )
        except Exception as e:
            print(e)


    def videoDownload(self, videoUrl, outputFilePath):
        try:
            # 다운로드 옵션
            options = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': outputFilePath,
            }

            # 비디오 다운로드
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([videoUrl])

            # 파일경로 보정
            if os.path.exists(outputFilePath + '.webm'):
                os.rename(outputFilePath + '.webm', outputFilePath)
        
        except Exception as e:
            print(e)

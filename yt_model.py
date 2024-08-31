import os
import shutil
from moviepy.editor import VideoFileClip

from yt_repos import YoutubeMusicRepository, VideoInfo


class YoutubeMusic:
    repository: YoutubeMusicRepository


    def __init__(self, repository: YoutubeMusicRepository):
        self.repository = repository


    def videoUrl(self, videoId):
        '비디오 URL'
        return f'https://www.youtube.com/watch?v={videoId}'


    def videoDownloadPath(self, videoInfo: VideoInfo):
        '비디오 다운로드 경로'
        videoPath = 'data/temp/{}.mp4'.format(videoInfo.videoId)
        return videoPath


    def audioExtractPath(self, videoInfo: VideoInfo):
        '음원 추출 경로'
        audioPath = 'data/temp/{}.mp3'.format(videoInfo.videoId)
        return audioPath
    
    
    def audioDeployPath(self, videoInfo: VideoInfo):
        '음원 배포 경로'
        outputPath = 'data/music/{}.mp3'.format(videoInfo.title)
        return outputPath
    

    def extractAudio(self, videoFilePath, outputFilePath):
        '음원 추출'
        with VideoFileClip(videoFilePath) as clip:
            clip.audio.write_audiofile(outputFilePath)
            clip.audio.close()
            clip.close()


    # 음원 파일 배포
    def deployAudio(self, videoInfo: VideoInfo):
        # 파일 경로
        outputFilePath = self.audioDeployPath(videoInfo)
        audioFilePath = self.audioExtractPath(videoInfo)

        # 파일 검사
        if not os.path.exists(audioFilePath): return

        # 파일 복사
        shutil.copy(audioFilePath, outputFilePath)


    # 임시 파일 정리
    def clearTempFiles(self, videoInfo: VideoInfo):
        os.unlink(self.videoDownloadPath(videoInfo))
        os.unlink(self.audioExtractPath(videoInfo))


    def videoInfo(self, videoUrl):
        '비디오 정보 가져오기'
        return self.repository.videoInfo(videoUrl)


    def videoDownload(self, videoInfo: VideoInfo, outputFilePath):
        '비디오 다운로드'
        self.repository.videoDownload(videoInfo.url, outputFilePath)


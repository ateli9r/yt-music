import os
import unittest

from yt_repos import YoutubeMusicLocalRepository, YoutubeMusicProdRepository
from yt_model import YoutubeMusic


class YoutubeMusicTestCase(unittest.TestCase):
    # 테스트 클래스 초기화
    @classmethod
    def setUpClass(cls) -> None:
        cls.isProd = os.getenv('PROD_TEST') == 'true'
        if cls.isProd:
            repository = YoutubeMusicProdRepository()
        else:
            repository = YoutubeMusicLocalRepository()
        cls.ytm = YoutubeMusic(repository)

        # 테스트 비디오 ID
        cls.testVideoId = 'yBLdQ1a4-JI'

        return super().setUpClass()
    

    # 비디오 정보
    def test_01_video_info(self):
        # 비디오 URL
        videoUrl = self.ytm.videoUrl(self.testVideoId)
        self.assertIsNotNone(videoUrl)

        # 비디오 정보
        videoInfo = self.ytm.videoInfo(videoUrl)
        self.assertIsNotNone(videoInfo)
        self.assertEqual(videoInfo.videoId, self.testVideoId)


    # 비디오 다운로드
    def test_02_download_video(self):
        # 비디오 URL
        videoUrl = self.ytm.videoUrl(self.testVideoId)
        self.assertIsNotNone(videoUrl)

        # 비디오 정보
        videoInfo = self.ytm.videoInfo(videoUrl)
        self.assertIsNotNone(videoInfo)

        # 비디오 다운로드 경로
        outputFilePath = self.ytm.videoDownloadPath(videoInfo)
        self.assertIsNotNone(outputFilePath)

        # 파일 삭제
        if os.path.exists(outputFilePath):
            os.unlink(outputFilePath)

        # 비디오 다운로드
        self.ytm.videoDownload(videoInfo, outputFilePath)
        self.assertTrue(os.path.exists(outputFilePath))


    # 음원 추출
    def test_03_extract_audio(self):
        # 비디오 URL
        videoUrl = self.ytm.videoUrl(self.testVideoId)
        self.assertIsNotNone(videoUrl)

        # 비디오 정보
        videoInfo = self.ytm.videoInfo(videoUrl)
        self.assertIsNotNone(videoInfo)

        # 비디오 다운로드 경로
        videoFilePath = self.ytm.videoDownloadPath(videoInfo)
        self.assertTrue(os.path.exists(videoFilePath))

        # 음원 추출 경로
        outputFilePath = self.ytm.audioExtractPath(videoInfo)

        # 파일 삭제
        if os.path.exists(outputFilePath):
            os.unlink(outputFilePath)
        
        # 음원 추출
        self.ytm.extractAudio(videoFilePath, outputFilePath)
        self.assertTrue(os.path.exists(outputFilePath))
    

    # 음원 파일 배포
    def test_04_deploy_audio(self):
        # 비디오 URL
        videoUrl = self.ytm.videoUrl(self.testVideoId)
        self.assertIsNotNone(videoUrl)

        # 비디오 정보
        videoInfo = self.ytm.videoInfo(videoUrl)
        self.assertIsNotNone(videoInfo)

        # 파일 경로
        outputFilePath = self.ytm.audioDeployPath(videoInfo)
        audioFilePath = self.ytm.audioExtractPath(videoInfo)
        self.assertTrue(os.path.exists(audioFilePath))

        # 파일 삭제 (목적지)
        if os.path.exists(outputFilePath):
            os.unlink(outputFilePath)

        # 음원 파일 배포
        self.ytm.deployAudio(videoInfo)
        self.assertTrue(os.path.exists(outputFilePath))
    

    # 임시 파일 정리
    def test_05_clear_temp_files(self):
        # 비디오 URL
        videoUrl = self.ytm.videoUrl(self.testVideoId)
        self.assertIsNotNone(videoUrl)

        # 비디오 정보
        videoInfo = self.ytm.videoInfo(videoUrl)
        self.assertIsNotNone(videoInfo)

        # 파일 경로
        videoFilePath = self.ytm.videoDownloadPath(videoInfo)
        audioFilePath = self.ytm.audioExtractPath(videoInfo)
        self.assertTrue(os.path.exists(videoFilePath))
        self.assertTrue(os.path.exists(audioFilePath))

        # 임시 파일 정리
        self.ytm.clearTempFiles(videoInfo)
        self.assertFalse(os.path.exists(videoFilePath))
        self.assertFalse(os.path.exists(audioFilePath))

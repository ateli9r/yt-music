import yaml

from yt_repos import YoutubeMusicProdRepository
from yt_model import YoutubeMusic


def main():
    # 모델 생성
    repository = YoutubeMusicProdRepository()
    ytm = YoutubeMusic(repository)

    # 설정파일 읽기
    config_file_path = 'data/config.yml'
    with open(config_file_path, 'r') as f:
        config = yaml.safe_load(f)
        videoIds = config['videoIds']
    
    # 비디오 아이디 목록 없으면 리턴
    if not videoIds: return
    
    # 유튜브 음원 다운로드
    for videoId in videoIds:
        videoUrl = ytm.videoUrl(videoId)
        videoInfo = ytm.videoInfo(videoUrl)

        videoFilePath = ytm.videoDownloadPath(videoInfo)
        audioFilePath = ytm.audioExtractPath(videoInfo)

        ytm.videoDownload(videoInfo, videoFilePath)
        ytm.extractAudio(videoFilePath, audioFilePath)
        ytm.deployAudio(videoInfo)
        ytm.clearTempFiles(videoInfo)


# 스크립트 메인
if __name__ == "__main__":
    main()

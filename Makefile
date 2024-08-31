clean:
	@mkdir -p data/music
	@mkdir -p data/temp
	@rm -f data/music/*
	@rm -f data/temp/*

test:
	@python -m unittest yt_test

test-cur:
	# python -m unittest yt_test.YoutubeMusicTestCase.test_01_video_info
	# python -m unittest yt_test.YoutubeMusicTestCase.test_02_download_video
	# python -m unittest yt_test.YoutubeMusicTestCase.test_03_extract_audio
	python -m unittest yt_test.YoutubeMusicTestCase.test_04_deploy_audio

run:
	@python app.py

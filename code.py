import os
from pytube import YouTube
import moviepy.editor as mp

def download_youtube_video(url, output_file):
    yt = YouTube(url)
    # 最高品質の動画をダウンロード
    yt.streams.get_highest_resolution().download(output_path=os.path.dirname(output_file), filename=os.path.basename(output_file))
    # ダウンロードした動画のパスを返す
    return output_file

def concatenate_videos(input_files, output_file):
    # 動画を連結
    video_clips = [mp.VideoFileClip(file) for file in input_files]
    final_clip = mp.concatenate_videoclips(video_clips)
    final_clip.write_videofile(output_file)

def main():
    # ユーザーによるYouTube動画のURLの入力を受け取る
    youtube_url = input("YouTube動画のURLを入力してください: ")

    # 出力ファイルの保存先を指定
    output_file = input("出力ファイルの名前を入力してください（例: output.mp4）: ")

    # YouTube動画をダウンロード
    download_file = download_youtube_video(youtube_url, output_file)

    # ユーザーによる動画の秒数指定を受け取る
    segments = []
    while True:
        segment_start = input("開始時間（HH:MM:SS）を入力してください（終了する場合はEnter）: ")
        if not segment_start:
            break
        segment_end = input("終了時間（HH:MM:SS）を入力してください: ")
        segments.append((segment_start, segment_end))

    # 各セグメントの動画を指定された秒数内で切り取って連結
    output_files = []
    for i, (start, end) in enumerate(segments):
        output_file = f"segment_{i}.mp4"
        with mp.VideoFileClip(download_file) as clip:
            segment = clip.subclip(start, end)
            segment.write_videofile(output_file)
        output_files.append(output_file)

    # 動画を連結して出力
    concatenate_videos(output_files, output_file)
    print(f"連結した動画を {output_file} として出力しました。")

if __name__ == "__main__":
    main()

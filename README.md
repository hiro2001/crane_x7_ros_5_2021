[English](README.en.md) | [日本語](README.md)

# crane_x7_examples
このパッケージは、https://github.com/rt-net/crane_x7_ros/tree/master/crane_x7_examples を千葉工業大学未来ロボティクス学科2020年度７班が改変したものを松田が改変したものです。
このパッケージは、リアルセンスを用いて上田先生の画像に黒目線を引くことを目標に作成されています。

## realsenceの環境構築

以下のURLを参考にしました。  
https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md  
https://github.com/IntelRealSense/realsense-ros  

## OpenCVの環境構築

以下のURLを参考にしました。  
https://qiita.com/tnoce/items/c819c85a85c16d246be8  
https://github.com/opencv/opencv/tree/master  


## 実機を使う場合

実機で動作を確認する場合、
制御信号ケーブルを接続した状態で次のコマンドを実行します。

```sh
sudo chmod 666 /dev/ttyUSB0
roslaunch crane_x7_bringup demo.launch fake_execution:=false
```

## realsence を起動

realsenceを接続した状態で、以下のコマンドを実行します。

```sh
roslaunch realsense2_camera rs_camera.launch
```

## 実行方法
以下の2つのコマンドを実行します。
```sh
rosrun crane_x7_examples vision.py
rosrun crane_x7_examples rats.py
```

## デモ動画リンク

 https://youtu.be/0TrebpTqbK8

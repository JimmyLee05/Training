//
//  BgMusicViewController.swift
//  Pomodoro Flow
//
//  Created by 李南君 on 2018/3/21.
//  Copyright © 2018年 Dan K. All rights reserved.
//

import AVFoundation

// 设置背景音乐
class BgMusicViewController {

    //单例
    static let shared = BgMusicViewController()

    var audioPlayer: AVAudioPlayer?

    let myMusic = ["raining", "thunder"]

    func randomMusic() -> String {
        let choose = Int(arc4random_uniform(UInt32(myMusic.count)))
        return myMusic[choose]
    }

    func playBgMusic() {
        let url = Bundle.main.url(forResource: String(describing: randomMusic()), withExtension: "mp3")
        var err: NSError?

        do {
            try audioPlayer = AVAudioPlayer(contentsOf: url!)
            audioPlayer?.numberOfLoops = -1
            audioPlayer?.prepareToPlay()
        } catch let err1 as NSError {
            err = err1
        }

        if err != nil {
            print(err)
        }

        let audioSession = AVAudioSession.sharedInstance()
        do {
            try audioSession.setCategory(AVAudioSessionCategoryPlayback)
        } catch {

        }
    }

    func startBGMusic() {
        audioPlayer?.play()
    }

    func stopBGMusic() {
        if (audioPlayer?.isPlaying) != nil {
            audioPlayer?.stop()
        }
    }
}

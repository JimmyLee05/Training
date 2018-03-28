//
//  Audio.swift
//  myForm
//
//  Created by bb on 2017/6/6.
//  Copyright © 2017年 bb. All rights reserved.
//

import UIKit
import AVFoundation

class Audio: NSObject {

    static let shared = Audio()
    
    // 这个数组中保存音频的名称
    var arrayOfTracks: [String] = [""] {
        didSet{
            print(arrayOfTracks)
            start()
        }
    }
    
    //记录待播放音频的数量
    var currentTrackNumber: Int = 0
    var audio: AVAudioPlayer!

    private override init() {
        super.init()
        initPlayer()
    }

    func initPlayer() {
        let path = Bundle.main.path(forResource: arrayOfTracks[currentTrackNumber], ofType: "mp3")
        print(arrayOfTracks)
        
        let url = URL(fileURLWithPath: path!)
        do {
            try audio = AVAudioPlayer(contentsOf: url)
        } catch {
            print(11)
        }
        audio.delegate = self
        audio.play()
    }
    //开始播放
    func start() {
        currentTrackNumber = 0
        initPlayer()
    }
}

// MARK: - AVAudioPlayerDelegate
extension Audio: AVAudioPlayerDelegate {

    func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        if flag {
            if currentTrackNumber < arrayOfTracks.count - 1 {
                currentTrackNumber += 1
                print("正在播放\(currentTrackNumber)个音频")
                if audio != nil {
                    audio.stop()
                    audio = nil
                }
                initPlayer()
            } else {
                print("全部播放完成")
                currentTrackNumber = 0
                audio.stop()
                audio = nil
            }
        }
    }
}

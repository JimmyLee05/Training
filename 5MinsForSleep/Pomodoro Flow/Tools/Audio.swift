//
//  Audio.swift
//  myForm
//
//  Created by bb on 2017/6/6.
//  Copyright © 2017年 bb. All rights reserved.
//

import UIKit
import AVFoundation

class Audio: NSObject, AVAudioPlayerDelegate {
    
    // 这个数组中保存音频的名称
    static var arrayOfTracks:[String] = [""]{
        didSet{
            print(arrayOfTracks)
            start()
        }
    }
    //记录待播放音频的数量
    static var currentTrackNumber:Int = 0
    static var audio:AVAudioPlayer!

    class func initPlayer(){
        let path = Bundle.main.path(forResource: arrayOfTracks[currentTrackNumber], ofType: "mp3")
        print(arrayOfTracks)
        
        let url = URL(fileURLWithPath: path!)
        do {
            try audio = AVAudioPlayer(contentsOf: url)
        } catch {
            print(11)
        }
        audio.delegate = self as? AVAudioPlayerDelegate
        audio.play()
    }
    
    //开始播放
    class func start(){
        currentTrackNumber = 0
        initPlayer()
    }
    
    //audioPlayer代理方法
    private class func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        if flag {
            if currentTrackNumber < arrayOfTracks.count - 1 {
                currentTrackNumber += 1
                print("正在播放\(currentTrackNumber)个音频")
                if audio != nil {
                    audio.stop()
                    audio = nil
                }
                initPlayer()
            }else{
                print("全部播放完成")
                currentTrackNumber = 0
                audio.stop()
                audio = nil
            }
        }
    }


}

//
//  AppSetting.swift
//  Pomodoro Flow
//
//  Created by 李南君 on 2018/3/27.
//  Copyright © 2018年 Dan K. All rights reserved.
//

import UIKit
import AVFoundation

class AppSetting: NSObject {
    
    //后台播放
    class func audioSession(){

        let audioSession = AVAudioSession.sharedInstance()

        do {
            try audioSession.setActive(true)
        } catch {

        }
        
        do {
            try audioSession.setCategory(AVAudioSessionCategoryPlayback)
        } catch {

        }
    }
}

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
        //创建会话，后台播放必须
        let audioSession = AVAudioSession.sharedInstance()
        //激活会话
        do {
            try audioSession.setActive(true)
        } catch {

        }
        //设置后台播放
        do {
            try audioSession.setCategory(AVAudioSessionCategoryPlayback)
        } catch {

        }
    }
}

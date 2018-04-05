//
//  PickerType.swift
//  Pomodoro Flow
//
//  Created by 李南君 on 2018/3/15.
//  Copyright © 2018年 JimmyLee. All rights reserved.
//

import Foundation

//  Setting里的General选项，在这里设置：1.一个番茄的时间长度 2.中间短休息的时间 3.一次长休息的时间 4.目标奖章数
enum PickerType {
    case pomodoroLength
    case shortBreakLength
    case longBreakLength
    case targetPomodoros
}


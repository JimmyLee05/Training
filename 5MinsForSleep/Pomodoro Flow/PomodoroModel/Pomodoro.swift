//
//  Pomodoro.swift
//  Pomodoro Flow
//
//  Created by 李南君 on 2018/3/15.
//  Copyright © 2018年 JimmyLee. All rights reserved.
//

import Foundation

// 这个类用来处理番茄时钟和完成后的一些逻辑，例如完成后加一个奖章。
class Pomodoro {
    
    static let shared = Pomodoro()

    let userDefaults    = UserDefaults.standard
    let settings        = SettingsManager.shared
    
    var state: State = .default

    fileprivate init() {}

    var pomodorosCompleted: Int {
        get {
            return userDefaults.integer(forKey: currentDateKey)
        }
        set {
            userDefaults.set(newValue, forKey: currentDateKey)
        }
    }

    func completePomodoro() {
        pomodorosCompleted += 1
        state = (pomodorosCompleted % 7 == 0 ? .longBreak : .shortBreak)
    }

    func completeBreak() {
        state = .default
    }

    func pomodoroCancel() {
        pomodorosCompleted = 0
    }

    fileprivate var currentDateKey: String {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy-MM-dd"
        return dateFormatter.string(from: Date())
    }
}

//
//  SettingsManager.swift
//  Pomodoro Flow
//
//  Created by 李南君 on 2018/3/15.
//  Copyright © 2018年 JimmyLee. All rights reserved.
//

import Foundation

// 设置一个对象来检索和保存对App的设置
class SettingsManager {

    static let shared = SettingsManager()

    fileprivate init() {}

    fileprivate let userDefaults = UserDefaults.standard
    fileprivate let notificationCenter = NotificationCenter.default

    // MARK: 设置中 General里的4个选项
    fileprivate struct Settings {
        static let pomodoroLength = "Settings.PomodoroLength"
        static let shortBreakLength = "Settings.ShortBreakLength"
        static let longBreakLength = "Settings.LongBreakLength"
        static let targetPomodoros = "Settings.TargetPomodoros"
    }
    // MARK: - General settings
    var pomodoroLength: Int {
        get { return userDefaults.object(forKey: Settings.pomodoroLength) as? Int ?? 5 * 60 }
        set { userDefaults.set(newValue, forKey: Settings.pomodoroLength) }
    }

    var shortBreakLength: Int {
        get { return userDefaults.object(forKey: Settings.shortBreakLength) as? Int ?? 2 * 60 }
        set { userDefaults.set(newValue, forKey: Settings.shortBreakLength) }
    }

    var longBreakLength: Int {
        get { return userDefaults.object(forKey: Settings.longBreakLength) as? Int ?? 1 * 60 }
        set { userDefaults.set(newValue, forKey: Settings.longBreakLength) }
    }

    var targetPomodoros: Int {
        get { return userDefaults.object(forKey: Settings.targetPomodoros) as? Int ?? 7 }
        set {
            userDefaults.set(newValue, forKey: Settings.targetPomodoros)
            notificationCenter.post(name: Notification.Name(rawValue: "targetPomodorosUpdated"), object: self)
        }
    }
}

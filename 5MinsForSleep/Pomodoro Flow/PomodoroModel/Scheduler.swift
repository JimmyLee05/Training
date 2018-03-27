//
//  Scheduler.swift
//  Pomodoro Flow
//
//  Created by 李南君 on 2018/3/15.
//  Copyright © 2018年 JimmyLee. All rights reserved.
//

import UIKit

// 计时过程中的四种调度：暂停，继续，开始，停止
protocol SchedulerDelegate: class {
    func schedulerDidPause()
    func schedulerDidUnpause()
    func schedulerDidStart()
    func schedulerDidStop()
}

class Scheduler {

    weak var delegate: SchedulerDelegate?

    static let sharedScheduler = Scheduler()

    fileprivate let userDefaults = UserDefaults.standard
    fileprivate let settings = SettingsManager.sharedManager
    fileprivate let pomodoro = Pomodoro.sharedPomodoro
    
    // 暂停时间的设置
    var pausedTime: Double? {
        get {
            return userDefaults.object(forKey: "PausedTime") as? Double
        }
        set {
            if let value = newValue, value != 0 {
                userDefaults.set(value, forKey: "PausedTime")
            } else {
                userDefaults.removeObject(forKey: "PausedTime")
            }
        }
    }

    // Date representing fire date of scheduled notification
    var fireDate: Date? {
        get {
            return userDefaults.object(forKey: "FireDate") as? Date
        }
        set {
            if let value = newValue {
                userDefaults.set(value, forKey: "FireDate")
            } else {
                userDefaults.removeObject(forKey: "FireDate")
            }
        }
    }

    // 如果pausedTime 不为空的话返回paused
    var paused: Bool {
        return pausedTime != nil
    }

    func timeStart() {
        switch pomodoro.state {
        case .default: schedulePomodoro()
        case .shortBreak: scheduleShortBreak()
        case .longBreak: scheduleLongBreak()
        }
        delegate?.schedulerDidStart()
        print("Scheduler started")
    }

    func timePause(_ interval: TimeInterval) {
        pausedTime = interval
        cancelNotification()
        delegate?.schedulerDidPause()
        print("Scheduler paused")
    }

    func timeUnpause() {
        guard let interval = pausedTime else { return }

        switch pomodoro.state {
        case .default: schedulePomodoro(interval)
        case .shortBreak: scheduleShortBreak(interval)
        case .longBreak: scheduleLongBreak(interval)
        }
        pausedTime = nil
        delegate?.schedulerDidUnpause()
        print("Scheduler unpaused")
    }

    func timeStop() {
        pausedTime = nil
        cancelNotification()

        delegate?.schedulerDidStop()
        print("Scheduler stopped")
    }

    // MARK: - 番茄计时结束后的通知
    fileprivate var firstScheduledNotification: UILocalNotification? {
        return UIApplication.shared.scheduledLocalNotifications?.first
    }

    fileprivate func cancelNotification() {
        UIApplication.shared.cancelAllLocalNotifications()
        fireDate = nil
        print("Notification canceled")
    }

    fileprivate func schedulePomodoro(_ interval: TimeInterval? = nil) {
        let interval = interval ?? TimeInterval(settings.pomodoroLength)
        scheduleNotification(interval,
                             title: NSLocalizedString("变强了一点！", comment: ""), body: "加油，自律让我们自由!")
        print("Pomodoro scheduled")
    }

    fileprivate func scheduleShortBreak(_ interval: TimeInterval? = nil) {
        let interval = interval ?? TimeInterval(settings.shortBreakLength)
        scheduleNotification(interval,
                             title: "是时候再来一组俯卧撑了！", body: "开始吧!")
        print("Short break scheduled")
    }

    fileprivate func scheduleLongBreak(_ interval: TimeInterval? = nil) {
        let interval = interval ?? TimeInterval(settings.longBreakLength)
        scheduleNotification(interval,
                             title: "今天的俯卧撑做完啦！", body: "100天后变成新的自己！")
        print("Long break scheduled")
    }

    fileprivate func scheduleNotification(_ interval: TimeInterval, title: String, body: String) {
        let notification = UILocalNotification()
        notification.fireDate = Date(timeIntervalSinceNow: interval)
        notification.alertTitle = title
        notification.alertBody = body
        notification.applicationIconBadgeNumber = 1
        notification.soundName = UILocalNotificationDefaultSoundName
        UIApplication.shared.scheduleLocalNotification(notification)
        fireDate = notification.fireDate

        print("Pomodoro notification scheduled for \(notification.fireDate!)")
    }
}

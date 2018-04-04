//
//  Scheduler.swift
//  Pomodoro Flow
//
//  Created by 李南君 on 2018/3/15.
//  Copyright © 2018年 JimmyLee. All rights reserved.
//

import UIKit
import SCLAlertView

// 计时过程中的四种调度：暂停，继续，开始，停止
protocol SchedulerDelegate: class {
    
    func schedulerDidPause()
    func schedulerDidUnpause()
    func schedulerDidStart()
    func schedulerDidStop()
}

@available(iOS 10.0, *)
class Scheduler {

    let CoreData = CoreDataManager.shared

    weak var delegate: SchedulerDelegate?

    static let shared = Scheduler()

    fileprivate let userDefaults = UserDefaults.standard
    fileprivate let settings = SettingsManager.shared
    fileprivate let pomodoro = Pomodoro.shared

    var Times: Double? {
        didSet {
        }
    }
    
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
                             title: NSLocalizedString("休息两分钟继续锻炼", comment: ""), body: "")

        print("做完一组俯卧撑通知")
    }

    fileprivate func scheduleShortBreak(_ interval: TimeInterval? = nil) {
        let interval = interval ?? TimeInterval(settings.shortBreakLength)
        scheduleNotification(interval,
                             title: "休息结束，开始锻炼，", body: "")
        print("调用短休息通知")
    }

    fileprivate func scheduleLongBreak(_ interval: TimeInterval? = nil) {

        var totalTimes: Double = 0

        let interval = interval ?? TimeInterval(settings.longBreakLength)
        pomodoro.pomodoroCancel()
        totalTimes += 1
        let pushupTimes = totalTimes
        self.Times = pushupTimes
        saveRun()
        scheduleNotification(interval,
                             title: "完成了一组俯卧撑，好样的 👍", body: "")
        print("调用长休息通知")
    }

    private func saveRun() {

        if Times == nil {
            print("no data")
        } else {
            CoreDataManager.shared.saveTimes(times: Times!)
        }

        print("查看存储次数数据 \(String(describing: Times))")
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

        print("----------------> 通知已发出 \(notification.fireDate!)")
    }
}

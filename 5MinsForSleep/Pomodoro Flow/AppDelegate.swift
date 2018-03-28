//
//  AppDelegate.swift
//  Pomodoro Flow
//
//  Created by 李南君 on 2018/3/15.
//  Copyright © 2018年 JimmyLee. All rights reserved.
//

import UIKit

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?

    let pomodoroState       = Pomodoro.sharedPomodoro
    let scheduler           = Scheduler.sharedScheduler

    func application(_ application: UIApplication,
                     didFinishLaunchingWithOptions launchOptions: [UIApplicationLaunchOptionsKey: Any]?) -> Bool {

        //增加标识，用于判断是否是第一次启动应用
        if (!(UserDefaults.standard.bool(forKey: "everLaunched"))) {
            UserDefaults.standard.set(true, forKey:"everLaunched")
            let guideViewController = GuideViewController()
            self.window?.rootViewController = guideViewController
            print("guideview launched!")
        }

        registerNotifications()
        configureTabBarColor()

        return true
    }

    func application(_ application: UIApplication,
                     didReceive notification: UILocalNotification) {

        print("didReceiveLocalNotification")
        timerViewController.presentAlertFromNotification(notification)
    }

    func applicationWillResignActive(_ application: UIApplication) {
    }

    func applicationDidEnterBackground(_ application: UIApplication) {
//        timerViewController.timerPause()
//        print("applicationDidEnterBackground")
//        switch pomodoroState.state {
//        case .default:
//        scheduleNotification(2,
//                             title: NSLocalizedString("回来做俯卧撑啦", comment: ""),
//                             body: NSLocalizedString("每天28分钟的锻炼，我们可以完成!", comment: ""))
//        case .shortBreak:
//            print("...")
//        case .longBreak:
//            print("...")
//        }
    }

    func applicationWillEnterForeground(_ application: UIApplication) {
    }

    func applicationDidBecomeActive(_ application: UIApplication) {
        resetBadgeNumber()
    }

    func applicationWillTerminate(_ application: UIApplication) {
        print("applicationWillTerminate")
    }

    fileprivate var timerViewController: TimerViewController {
        let tabBarController = window!.rootViewController as! UITabBarController
        return tabBarController.viewControllers!.first as! TimerViewController
    }

    fileprivate func registerNotifications() {
        let notificationSettings = UIUserNotificationSettings(types: [.alert, .badge, .sound],
                                                              categories: nil)
        UIApplication.shared.registerUserNotificationSettings(notificationSettings)
    }

    fileprivate func resetBadgeNumber() {
        print("reset badge number")
        UIApplication.shared.applicationIconBadgeNumber = 0
    }

    fileprivate func configureTabBarColor() {
        UITabBar.appearance().tintColor = UIColor(red: 240/255.0, green: 65/255.0, blue: 90/255.0, alpha: 1)
    }

    fileprivate func scheduleNotification(_ interval: TimeInterval, title: String, body: String) {
        let notification = UILocalNotification()
        notification.fireDate = Date(timeIntervalSinceNow: interval)
        notification.alertTitle = title
        notification.alertBody = body
        notification.applicationIconBadgeNumber = 1
        notification.soundName = UILocalNotificationDefaultSoundName
        UIApplication.shared.scheduleLocalNotification(notification)

        print("Pomodoro notification scheduled for \(notification.fireDate!)")
    }

    public func DispatchAfter(after: Double, handler:@escaping ()->())
    {
        DispatchQueue.main.asyncAfter(deadline: .now() + after) {
            handler()
        }
    }

}


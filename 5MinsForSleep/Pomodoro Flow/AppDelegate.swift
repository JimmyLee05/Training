//
//  AppDelegate.swift
//  Pomodoro Flow
//
//  Created by 李南君 on 2018/3/15.
//  Copyright © 2018年 JimmyLee. All rights reserved.
//

import UIKit
import CoreData

@available(iOS 10.0, *)
@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?
    
    let pomodoroState           = Pomodoro.shared
    let scheduler               = Scheduler.shared

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
        NotificationCenter.default.post(name: NSNotification.Name("XMNotification"), object: notification)
    }

    func applicationWillResignActive(_ application: UIApplication) {

    }

    func applicationDidEnterBackground(_ application: UIApplication) {

        print("applicationDidEnterBackground")
        switch pomodoroState.state {
        case .default:
        scheduleNotification(   2,
                                title: NSLocalizedString("回来做俯卧撑啦", comment: ""),
                                body: NSLocalizedString("每天28分钟的锻炼，我们可以完成!", comment: ""))
        case .shortBreak:
            print("...")
        case .longBreak:
            print("...")
        }
    }

    func applicationWillEnterForeground(_ application: UIApplication) {
    }

    func applicationDidBecomeActive(_ application: UIApplication) {
        resetBadgeNumber()
    }

    func applicationWillTerminate(_ application: UIApplication) {
        print("applicationWillTerminate")
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

    // MARK: - CoreData
    lazy var managedObjectModel: NSManagedObjectModel = {
        let modelURL = Bundle.main.url(forResource: "Pomodoro Flow", withExtension: "momd")
        let managedObjectModel = NSManagedObjectModel.init(contentsOf: modelURL!)
        return managedObjectModel!
    }()

    lazy var persistentStoreCoordinator: NSPersistentStoreCoordinator = {
        let persistentStoreCoordinator = NSPersistentStoreCoordinator.init(managedObjectModel: managedObjectModel)

        let sqliteURL = documentDir.appendingPathComponent("Pomodoro Flow.sqlite")

        let options = [NSMigratePersistentStoresAutomaticallyOption : true, NSInferMappingModelAutomaticallyOption : true]

        var failureReason = "创建NSPersistentStoreCoordinator时出现错误"

        do {
            try persistentStoreCoordinator.addPersistentStore(ofType: NSSQLiteStoreType, configurationName: nil, at: sqliteURL, options: options)
        } catch {
            // Report any error we got.
            var dict = [String: Any]()
            dict[NSLocalizedDescriptionKey] = "初始化NSPersistentStoreCoordinator失败" as Any?
            dict[NSLocalizedFailureReasonErrorKey] = failureReason as Any?
            dict[NSUnderlyingErrorKey] = error as NSError
            let wrappedError = NSError(domain: "YOUR_ERROR_DOMAIN", code: 6666, userInfo: dict)
            print("未解决的错误： \(wrappedError), \(wrappedError.userInfo)")
            abort()
        }
        return persistentStoreCoordinator
    }()

    lazy var context: NSManagedObjectContext = {
        let context = NSManagedObjectContext.init(concurrencyType: NSManagedObjectContextConcurrencyType.mainQueueConcurrencyType)

        context.persistentStoreCoordinator = persistentStoreCoordinator

        return context
    }()

    lazy var documentDir: URL = {
        let documentDir = FileManager.default.urls(for: FileManager.SearchPathDirectory.documentDirectory, in: FileManager.SearchPathDomainMask.userDomainMask).first
        return documentDir!
    }()
}

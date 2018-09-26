//
//  AppDelegate.swift
//  HanCam
//
//  Created by 李南君 on 2018/9/25.
//  Copyright © 2018 NanJun Li. All rights reserved.
//

import UIKit

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?


    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {

        self.window                     = UIWindow(frame: UIScreen.main.bounds)
        self.window?.backgroundColor    = .white

        self.window?.rootViewController = TabBarViewController.shared
        
        return true
    }

    func applicationWillResignActive(_ application: UIApplication) {

    }

    func applicationDidEnterBackground(_ application: UIApplication) {

    }

    func applicationWillEnterForeground(_ application: UIApplication) {

    }

    func applicationDidBecomeActive(_ application: UIApplication) {

    }

    func applicationWillTerminate(_ application: UIApplication) {

    }

}


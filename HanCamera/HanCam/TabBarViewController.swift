//
//  ViewController.swift
//  HanCam
//
//  Created by 李南君 on 2018/9/25.
//  Copyright © 2018 NanJun Li. All rights reserved.
//

import UIKit

struct TabBarData {

    var itemsTitle: String!
    var itemsImage: UIImage!
    var viewController: UIViewController!

    init(itemsTitle: String,
         itemsImage: UIImage,
         viewController: UIViewController) {

        self.itemsTitle     = itemsTitle
        self.itemsImage     = itemsImage
        self.viewController = viewController
    }
}

class TabBarViewController: UITabBarController {

    static let shared = TabBarViewController()

    let tabBarDatas = [TabBarData(itemsTitle: NSLocalizedString("BTN_BAR_PHOTO",
                                                                comment: ""),
                                  itemsImage: UIImage(named: "app_tabbar_photo")!,
                                  viewController: CameraViewController()),
                       TabBarData(itemsTitle: NSLocalizedString("BTN_BAR_CAMERA",
                                                                comment: ""),
                                  itemsImage: UIImage(named: "app_tabbar_camera")!,
                                  viewController: CameraViewController()),
                       TabBarData(itemsTitle: NSLocalizedString("BTN_BAR_SETTING",
                                                                comment: ""),
                                  itemsImage: UIImage(named: "app_tabbar_setting")!,
                                  viewController: CameraViewController())]

    var navigationControllers = [BaseNavigationController]()

    override func viewDidLoad() {
        super.viewDidLoad()

        self.tabBar.clipsToBounds = true

        self.tabBarDatas.forEach { (tabBarData) in

            let navigationController = BaseNavigationController(rootViewController: tabBarData.viewController)
            navigationController.tabBarItem.title = tabBarData.itemsTitle
            navigationController.tabBarItem.image = tabBarData.itemsImage
            navigationControllers.append(navigationController)
        }

        tabBar.tintColor =  UIColor(red: 20 / 255,
                                    green: 20 / 255,
                                    blue: 20 / 255,
                                    alpha: 1)

        self.viewControllers = navigationControllers

        UITabBarItem.appearance().titlePositionAdjustment = UIOffset(horizontal: 0,
                                                                     vertical: (UIDevice.isNotchScreen ? -8 : -5))
    }

    override func viewWillLayoutSubviews() {
        var tabFrame: CGRect = self.tabBar.frame
        tabFrame.size.height = UIDevice.isNotchScreen ? 95 : 55
        tabFrame.origin.y    = self.view.frame.size.height - (UIDevice.isNotchScreen ? 95 : 55)
        self.tabBar.frame    = tabFrame
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
    }

    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }

}



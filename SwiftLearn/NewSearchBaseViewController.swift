//
//  NewSearchBaseViewController.swift
//  MYNT
//
//  Created by 李南君 on 2017/11/2.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit
import MYNTKit

private let kCloseNotification = NSNotification.Name("kClosedNotification")

class SearchBaseViewController: BaseViewController {
    
    weak var connectingMynt: Mynt?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        NotificationCenter.default.addObserver(self, selector: #selector(closedViewControllerNotification(notification:)), name: kClosedNotification, object: nil)
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    override func leftBarButtonClickedHandler() {
        _ = navigationController?.popToRootViewController(animated: true)
        didDismissViewController()
    }
    
    override func didDismissViewController() {
        super.didDismissViewController()
        if connectingMynt == nil || connectingMynt.state != .connected {
            NotificationCenter.default.post(name: kCloseNotification, object: self is MyntEducationViewController ? "" : nil)
        }
    }
    
    @objc func closedViewControllerNotification(notification: Notification) {
        if notification.object == nil {
            connectingMynt?.disconnect()
        }
        connectingMynt = nil
        NotificationCenter.default.removeObserver(self)
    }
}

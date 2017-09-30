//
//  NewMyntChargeViewController.swift
//  MYNT
//
//  Created by 李南君 on 2017/9/29.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit
import MYNTKit
import SlightechKit
import RealmSwift

public enum PayType: Int {
    
    case wechatPay
    case aliPay
    case none
    
    var image: UIImage? {
        switch self {
        case .wechatPay:
            return UIImage(named: "app_settings_payment_wechat")
        case .aliPay:
            return UIImage(named: "app_setting_payment_alipay")
        case .none:
            return UIImage(named: "")
        }
    }
    
    var payName: String {
        switch self {
        case .wechatPay:
            return MTLocalizedString("GPS_CHARGE_WECHAT", comment: "微信支付")
        case .aliPay:
            return MTLocalizedString("GPS_CHARGE_ALI", comment: "阿里支付")
        case .none:
            return ""
        }
    }
}

class MyntChargeViewController: MYNTKitBaseViewController,UIScrollViewDelegate {
    
    public class func show(parentViewController: UIViewController?, mynt: Mynt?) {
        let viewController      = MyntChargeViewController()
        viewCobtroller.mynt     = mynt
        parentViewController?.present(BaseNavigationController(rootViewController: viewController),
                                      animated: true,
                                      completion: nil)
    }
}







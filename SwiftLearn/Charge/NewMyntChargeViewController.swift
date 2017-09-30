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

class NewMyntChargeViewController: MYNTKitBaseViewController,UIScrollViewDelegate {
    
    public class func show(parentViewController: UIViewController?, mynt: Mynt?) {
        let viewController      = MyntChargeViewController()
        viewCobtroller.mynt     = mynt
        parentViewController?.present(BaseNavigationController(rootViewController：viewController),
                                      animated: true,
                                      completion: nil)
    }
    
    @IBOutlet weak var scrollView: UIScrollView!
    @IBOutlet weak var infoView: UIView!
    @IBOutlet weak var avatarImageView: UIImageView!
    @IBOutlet weak var nameLabel: UILabel!
    @IBOutlet weak var remainderHintLabel: UILabel!
    @IBOutlet weak var remainderNumLabel: UILabel!
    @IBOutlet weak var remainderUnitLabel: UILabel!
    @IBOutlet weak var remainderTimeLabel: UILabel!
    

    @IBOutlet weak var package1View: UIView!
    @IBOutlet weak var package2View: UIView!
    @IBOutlet weak var package3View: UIView!
    
    @IBOutlet weak var alipayView: UIView!
    @IBOutlet weak var wechatView: UIView!
    
    @IBOutlet weak var chargeButton: UIButton!
    
    lazy var infoBackgroundLayer: CALayer = {
        let layer = CALayer()
        layer.backgroundColor = navigationBarColor.cgColor
        layer.anchorPoint     = .zero
        self.infoView.layer.insertSublayer(layer, at: 0)
        return layer
    }()
    
    var payType: PayType = .aliPay {
        didSet {
            alipayView.viewWithTag(102)?.layer.borderWidth = payType == .aliPay ? 0 : 1
            wechatView.viewWithTag(102)?.layer.borderWidth = payType == .wechatPay ? 0 : 1
            (alipayView.viewWithTag(102) as? UIImageView)?.image = payType == .aliPay ? UIImage(named: "tick") : nil
            (wechatView.viewWithTag(102) as? UIImageView)?.image = payType == .wechatPay ? UIImage(named: "tick") : nil
        }
    }
    
    var packagesView: [UIView] {
        return [package1View, packgae2View, package3View]
    }
    var paysView: [UIView] {
        return [alipayView, wechatView]
    }
    
    var selectedPackage: SCPay.SCPackage? {
        didSet {
            packagesView.forEach { view in
                let textColor = view.tag == selectedPackage?.month ?
                UIColor(red:0.65, green:0.93, blue:0.15, alpha:1.00) :
                UIColor(red:0.24, green:0.24, blue:0.24, alpha:1.0)
                
                let borderColor = view.tag == selectedPackage?.month ?
                UIColor(red:0.65, green:0.93, blue:0.15, alpha:1.00) :
                UIColor(red:0.82, green:0.82, blue:0.82, alpha:1.00)
                
                (view.viewWithTag(101) as? UILabel)?.textColor = textColor
                (view.viewWithTag(102) as? UILabel)?.textColor = textColor
                (view.viewWithTag(103) as? UILabel)?.textColor = textColor
                view.layer.borderColor = borderColor.cgColor
            }
        }
    }
    
    var packages: [SCPay.SCPackage] = [] {
        didSet {
            if packages.count == packagesView.count {
                for i in 0..<packagesView.count {
                    let package = packages[i]
                    let packageView = packagesView[i]
                    
                    packageView.tag = package.month
                    packageView.isHidden = false
                    (packageView.viewWithTag(101) as? UILabel)?.text = String(format: "%.2f", package.money)
                    (packageView.viewWithTag(103) as? UILabel)?.text = "\(package.month)" + MTLocalizedString("GPS_CHARGE_MONTH", comment: "月")
                }
                selectedPackage = packages.first
            }
        }
    }
    
    override var isShowBackgroundLayer: Bool {
        return false
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        title = MTLocalizedString("GPS_CHARGE_TITLE", comment: "支付")
        setLeftBarButtonItem(image: Resource.Image.Nacigation.close)
        
    }
}
















































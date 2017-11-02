//
//  NewSearchTipsViewController.swift
//  MYNT
//
//  Created by 李南君 on 2017/11/2.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit
import MYNTKit
import Lottie

class NewSearchTipsViewController: UIViewController {
    
    var animation: String {
        switch self {
        case .none:
            return ""
        case .mynt:
            return Resource.Lottie.StartingUp.mynt
        case .myntGPS:
            return Resource.Lottie.StartingUp.myntGPS
        case .myntES:
            return Resource.Lottie.StartingUp.myntES
        }
    }
    
    var message: String {
        switch self {
        case .none:
            return ""
        case .mynt:
            return MTLocalizedString("PAIR_PROMPT_MESSAGE", comment: "提示语")
        case .myntGPS:
            return MTLocalizedString("PAIR_PROMPT_GPS_MESSAGE", comment: "提示语")
        case .myntES:
            return MTLocalizedString("PAIR_PROMPT_ES_MESSAGE", comment: "提示语")
        }
    }
}

// 指示界面
class SearchTipsViewController: SearchBaseViewController {
    
    var productType = SCDeviceType.mynt
    
    var animationView: LOTAnimationView?
    
    var isPairFailed = false
    
    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = UIColor.white
        backgroundLayer?.removeFromSuperlayer()
        title = MTLocalizedString("PAIR_PAIRING_ADD_TITLE", comment: "添加小觅")
        setLeftBarButtonItem(image: Resource.Image.Navigation.back)
        
        okButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)
        
        if isPairFailed {
            messageLabel.text = MTLocalizedString("PAIR_FAIL", comment: "配对失败")
            okButton.setTitle(MTLocalizedString("PAIR_RETRY", comment: "重试"), for: .normal))
        } else {
            messageLabel.text = productType.message
            okButton.setTitle(MTLocalizedString("PAIR_DONE", comment: "完成"), for: .normal)
        }
        
        guard let bundlePath = Bundle.main.path(forResource: productType.animation, ofType: "bundle") else { return }
        guard let bundle = Bundle(path: bundlePath) else { return }
        animationView                       = LOTAnimationView(name: "data", bundle: bundle)
        animationView?.cacheEnable        = false
        animationView?.contentMode        = .scaleAspectFit
        animationView?.loopAnimation      = true
        animationView?.layer.anchorPoint  = CGPoint(x: 0.5, y: 0.5)
        animationView?.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(animationView!)
        animationView?.fillInSuperView()
        animationView?.play()
    }
    
    override func viewDidLayoutSubviews() {
        super.viewDidLayoutSubviews()
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
    }
    
    @IBAction func didClickOkButton(_ sender: AnyObject) {
        let viewController = SearchViewController()
        viewController.productType = productType
        removeBackBarButtonTitle()
        navigationController?.pushViewController(viewController, animated: true)
    }
}


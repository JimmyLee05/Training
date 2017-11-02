//
//  NewSearchPairBLEViewController.swift
//  MYNT
//
//  Created by 李南君 on 2017/11/2.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit

class NewSearchPairBLEViewController: UIViewController {
    
    
    var isNew = true
    
    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = UIColor.white
        backgroundLayer?.removeFromSuperlayer()
        backgroundLayer = nil
        
        if isNew {
            setLeftBarButtonItem(image: Resource.Image.Navigation.back)
        } else {
            setLeftBarButtonItem(image: Resource.Image.Navigation.close)
        }
        okButton.setTitle(MTLocalizedString("ADD_OK", comment: "ok"), for: UIControlState.normal)
        messageLabel.text = MTLocalizedString("PAIR_PAIRING_SUBTITLE", comment: "")
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    override func leftBarButtonClickedHandler() {
        if isNew {
            _ = navigationController?.popToRootViewController(animated: true)
            connectingMynt?.disconnect()
        } else {
            connectingMynt?.disconnect()
            dismissNavigationController(animated: true, completion: nil)
        }
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        
        let animation = CABasicAnimation(keyPath: "position")
        animation.byValue = NSValue(cgPoint: CGPoint(x: 15, y: -8))
        animation.repeatCount = Float.infinity
        animation.autoreverses = true
        animation.duration = 1
        arrowImageView.layer.add(animation, forKey: "arrow-move")
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        arrowImageView.layer.removeAllAnimations()
    }
}

//
//  Animation.swift
//  myForm
//
//  Created by bb on 2017/6/7.
//  Copyright © 2017年 bb. All rights reserved.
//

import UIKit

struct Animation {
    
    //缩放动画
    static func scale(view: UIView){

        let animation: CABasicAnimation = CABasicAnimation.init(keyPath: "transform.scale")

        animation.duration = 0.2
        animation.repeatCount = 0
        animation.autoreverses = true
        //animation.fromValue = NSNumber(floatLiteral: 1.0)
        animation.toValue = NSNumber(floatLiteral: 0.9)

        view.layer.add(animation, forKey: "scale-layer")
    }
}

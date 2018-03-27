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
        // 设定为缩放
        let animation: CABasicAnimation = CABasicAnimation.init(keyPath: "transform.scale")
        // 动画选项设定
        animation.duration = 0.2 // 动画持续时间
        animation.repeatCount = 0 // 重复次数
        animation.autoreverses = true
        // 缩放倍数
        //animation.fromValue = NSNumber(floatLiteral: 1.0) // 开始时的倍率
        animation.toValue = NSNumber(floatLiteral: 0.9) // 结束时的倍率
        // 添加动画
        view.layer.add(animation, forKey: "scale-layer")
    }

}

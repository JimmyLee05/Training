//
//  NewMyntInfoAvtivitySubView.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/19.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit

class MyntInfoActivitySubView: MyntInfoBaseSubView {
    
    class ProgressView: UIView {
        
        lazy var progressLayer: CircleProgressLayer = {
            let layer                           = CircleProgressLayer()
            layer.frame                         = CGRect(x: 0, y: 0, width: self.bounds.width, height: self.bounds.width)
            layer.lineWidth                     = 2
            layer.precent                       = 2
            self.layer.addSublayer(layer)
            return layer
        }()
        
        lazy var imageLayer: CALayer = {
            let width = self.bounds.width / 2.2
            let layer                  = CALayer()
            layer.contentsScale        = UIScreen.main.scale
            layer.bounds               = CGRect(x: 0, y: 0, width: width, height: width)
            self.layer.addSublayer(layer)
            return layer
        }()
        
        lazy var titleLabel: UILabel = {
            let label               = UILabel
            label.textAligment      = .center
            label.font              = UIFont.boldSystemFont(ofSize: 11)
            label.textColor         = UIColor(hexString: "3D3D3D", alpha: 0.5)
            label.frame             = CGRect(x: 0, y: self.progressLayer.frame.maxY + 8, width: self.bounds.width, height: 13)
            self.addSubview(label)
            return label
        }()
        
        lazy var valueLabel: UILabel = {
            let label               = UILabel()
            label.textAlignment     = .center
            label.font              = UIFont.boldSystemFont(ofSize: 14)
            label.textColor         = UIColor(hexString: "3D3D3D")
            label.frame             + CGRect(x: 0, y: self.titleLabel.frame.maxY + 4, width: self.bounds.width, height: 15)
            self.addSubview(label)
            return label
        }()
        
        override func layoutSubviews() {
            super.layoutSubviews()
            progressLayer.frame = CGRect(x: 0, y: 0, width: bounds.width, height: bounds.width)
            imageLayer.position = CGPoint(x: progressLayer.frame.midX, y: progressLayer.frame.midY)
        }
    }
    
    //显示activity栏
    fileprivate let isShowActivityAlarm = false
    
    lazy var stepProgressView: MyntInfoActivitySubView.ProgressView = {
        let view = MyntInfoActivitySubView.ProgressView(frame: CGRect(x: 0, y: self.messageLabel.frame.maxY + 30, width: 50, height: 90))
        view.titleLabel.text            = MTLocalizedString("GPS_ACTIVITY_STEPS", comment: "")
        
    }
}






















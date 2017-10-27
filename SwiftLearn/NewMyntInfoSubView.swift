//
//  NewMyntInfoSubView.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/26.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit
import SlightechKit

// MARK: - 设备信息界面
class MyntInfoSubView: MyntInfoBaseSubView {
    
    override var isShowLine: Bool { return false }
    
    // 电量文字
    lazy var batteryLabel: UILabel = {
        let label               = UILabel()
        label.textAlignment     = .left
        label.font              = UIFont.systemFont(ofSize: 11)
        label.frame             = CGRect(x: self.bounds.midX + 2, y: self.avatarImageView.frame.minY - 20, width: 30, height: 12)
        self.addSubview(label)
        return label
    }()
    
    // 电量
    lazy var batteryView: BatteryView = {
        let view = BatteryView()
        view.frame = CGRect(x: self.bounds.midX - 22, y: self.avatarImageView.frame.minY - 20, width: 20, height: 12)
        self.addSubview(view)
        return view
    }()
    
    // 头像
    lazy var avatarImageView: UIImageView = {
        let width: CGFloat = 120
        let view = UIImageView(frame: CGRect(x: self.bounds.midX - width / 2, y: 70, width: width, height: width))
        self.addSubview(view)
        return view
    }()
    
    // 分享tag
    lazy var sharedImageView: UIImageView = {
        let width: CGFloat = 36
        let view           = UIImageView(image: UIImage(named: "gps_share"))
        view.backgroundColor = UIColor.white
        view.frame           = CGRect(x: self.avatarImageView.frame.minX,
                                      y: self.avatarImageView.frame.maxY - width,
                                      width: width,
                                      height: width)
        view.layer.cornerRadius = view.bounds.height / 2
        self.insertSubview(view, aboveSubview: self.avatarImageView)
        return view
    }()
    
    // 箭头
    lazy var arrowImageView: UIImageView = {
        let view = UIImageView(image: UIImage(named: "homepage_arrow_down"))
        self.addSubview(view)
        return view
    }()
    
    // 名字
    lazy var nameLabel: UILabel = {
        let label               = UILabel()
        label.textAlignment     = .center
        label.font              = UIFont.systemFont(ofSize: 25)
        label.textColor         = UIColor.white
        label.frame             = CGRect(x: 20, y: self.avatarImageView.frame.maxY + 14, width: self.bounds.width - 40, height: 27)
        self.addSubview(label)
        return label
    }()
    
    // 距离
    lazy var distanceLabel: UILabel = {
        let label               = UILabel()
        label.textAlignment     = .center
        label.font              = UIFont.systemFont(ofSize: 13)
        label.textColor         = UIColor.white
        label.frame             = CGRect(x: 20, y: self.nameLabel.frame.maxY + 6, width: self.bounds.width - 40, height: 15)
        self.addSubview(label)
        return label
    }()
    
    // 断线时间
    lazy var distanceTimeLabel: UILabel = {
        let label               = UILabel()
        label.textAlignment     = .center
        label.font              = UIFont.systemFont(ofSize: 11)
        label.textColor         = UIColor(white: 1, alpha: 0.5)
        label.frame             = CGRect(x: 20, y: self.distanceLabel.frame.maxY + 4, width: self.bounds.width - 40, height: 20)
        self.addSubview(label)
        return label
    }()
    
    // 连接中的动画
    lazy var connectingLayer: ConnectingLayer = {
        let batteryRadius: CGFloat = self.avatarImageView.bounds.width + 12
        
        let layer = ConnectingLayer(bounds: CGRect(origin: CGPoint.zero, size: CGSize(width: batteryRadius, height: batteryRadius)),
                                    fromColor: UIColor.white,
                                    toColor: UIColor.clear,
                                    linewidth: 4)
        layer.anchorPoint          = CGPoint(x: 0.5, y: 0.5)
        layer.position             = CGPoint(x: self.avatarImageView.bounds.midX, y: self.avatarImageView.bounds.midY)
        layer.opacity              = 0
        self.avatarImageView.layer.insertSublayer(layer, at: 0)
        return layer
    }()
    
    // 离线遮罩
    lazy var avatarOfflineLayer: CGShapeLayer = {
        let layer                       = CAShapeLayer()
        layer.connectsScale             = UIScreen.main.scale
        layer.position                  = CGPoint.zero
        layer.anchorPoint               = CGPoint.zero
        layer.fileColor                 = UIColor(white: 1, alpha: 0.8).cgColor
        layer.bounds                    = self.avatarImageView.bounds
        layer.path                      = UIBezierPath(ovaIn: layer.bounds).cgPath
        self.avatarImageView.layer.addSublayer(layer)
        return layer
    }()
    
    fileprivate var onlineAnimation: MyntStateAnimationProtocol?
    fileprivate var isRunningAnimation = false
    
    override var uiState: MYNTUIState {
        
        didSet {
            if uiState == oldValue { return }
            
            mynt?.updateStatusLabel(addressLabel: distanceLabel, simStatusLabel: distanceTimeLabel)
            
            avatarOfflineLayer.isHidden = uiState == .online
            if oldValue == .connecting {
                // 从连接中切换到在线
                connectingLayer.stopAnimation()
            }
            
            
        }
    }
}































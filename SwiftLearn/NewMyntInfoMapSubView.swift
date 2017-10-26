//
//  NewMyntInfoMapSubView.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/23.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit
import SlightechKit

class MyntInfoMapSubView: MyntInfoBaseSubView {
    
    class MyntMapAddressView: UIView {
        
        lazy var locationImageView: UIImageView = {
            let imageView = UIImageView(image: UIImage(named: "map_icon"))
            imageView.frame             = CGRect(origin: CGRect(x: 0, y: self.bounds.height / 2 - imageView.frame.height / 2), size: imageView.frame.size)
            self.addSubview(imageView)
            return imageView
        }()
        
        lazy var arrowImageView: UIImageView = {
            let imageView = UIImageView(image: UIImage(named: "setting_app_arrow_right"))
            imageView.frame = CGRect(origin: CGPoint(x: self.bounds.width - imageView.frame.width,
                                                     y: self.bounds.height / 2 - imageView.frame.height / 2),
                                     size: imageView.frame.size)
            self.addSubview(imageView)
            return imageView
        }()
        
        lazy var addressLabel: UILabel = {
            let label = UILabel()
            label.textColor     = UIColor.black
            label.textAlignment = .left
            label.font          = UIFont.systemFont(ofSize: 14)
            label.frame         = CGRect(x: self.locationImageView.frame.maxX + 15, y: 0,
                                         width: self.bounds.width - self.locationImageView.frame.width - self.arrowImageView.frame.width - 25, height: 18)
            self.addSubview(label)
            return label
        }()
        
        lazy var nodataLabel: UILabel = {
        let label = UILabel()
        label.textColor     = UIColor.black
        label.textAligment  = .left
        label.font          = UIFont.systemFont(ofSize: 14)
        label.frame         = CGRect(x: self.locationImageView.frame.maxX + 15,
                                     y: 0,
                                     width: self.bounds.width - self.locationImageView.frame.width - self.arrowImageView.frame.width - 25,
                                     height:self.bounds.height)
        self.addSubview(label)
        return label
    }()
    
        lazy var timeLabel: UILabel = {
            let label = UILabel()
            label.textColor         = UIColor(white: 0, alpha: 0.5)
            label.textAlignment     = .left
            label.font              = UIFont.systemFont(ofSize: 14)
            label.frame             = CGRect(x: self.addressLabel.frame.minX, y: self.addressLabel.frame.maxY,
                                             width: self.addressLabel.frame.width, height: 18)
            self.addSubview(label)
            return label
        }()
        
        override init(frame: CGRect) {
            super.init(frame: frame)
        }
        
        required init(coder aDecoder: NSCoder) {
            fatalError("init(coder:) has not been implemented")
        }
    }
    
    lazy var mapImageView: UIImageView = {
        let width = self.bounds.width - 40
        let imageView = UIImageView()
        imageView.frame = CGRect(x: 20, y: self.messageLabel.frame.maxY + 30, width: width, height: width / 2)
        self.addSubview(imageView)
        return imageView
    }()
    
    lazy var mapEmptyView: UIView = {
        let view = UIView()
        view.frame = self.mapImageView.bounds
        self.mapImageView.addSubview(view)
        return view
    }()
    
    lazy var addressView: MyntMapAddressView = {
        let width = self.bounds.width - 40
        let view = MyntMapAddressView()
        view.frame = CGRect(x: 20, y: self.mapImageView.frame.maxY + 20, width: width, height: 40)
        self.addSubview(view)
        return view
    }()
    
    //按钮
    lazy var realtimeButton: BorderButton = {
        let button = BorderButton()
        button.titleLabel?.font = UIFont.systemFont(ofSize: 14)
        button.loadMyntStyle()
        button.setTitle(MTLocalizedString("MYNTSETTING_MAP_REALTIME_TITLE", comment: ""),
                        for: .normal)
        button.addTarget(self, action: #selector(MyntInfoMapSubView.didClickButton(button:)), for: .touchUpInside)
        button.contentEdgeInsets = UIEdgeInsets(top: 0, left: 20, bottom: 0, right: 20)
        button.sizeToFit()
        let width = button.frame.size.width
        button.frame = CGRect(x: self.bounds.midX - width / 2, y: self.addressView.frame.maxY + 50, width: width, height: 40)
        button.layer.cornerRadius = button.bounds.height / 2
        self.addSubview(button)
        return button
    }()
    
    //信息
    
}


















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
    
    
}












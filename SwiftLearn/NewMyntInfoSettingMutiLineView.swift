//
//  NewMyntInfoSettingMutiLineView.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/19.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit

class MyntInfoSettingMultiLineView: BaseMyntInfoSettingLineView {
    
    lazy var titleLabel: UILabel = {
        let label               = UILabel(frame: self.descLabel.frame)
        label.textAligment      = .left
        label.font              = UIFont.systemFont(ofSize: 15)
        label.textColor         = UIColor(hexString: "3D3D3D")
        label.frame.origin.y    = self.descLabel.frame.minY - label.frame.height - 6
        self.addSubview(label)
        return label
    }()
    
    lazy var descLabel: UILabel = {
        let label               = UILabel(frame: CGRect(origin: CGPoint(x: 25, y: 0), size:
            CGSize(width: self.valueLabel.frame.maxX - 50, height: 18)))
        label.textAligment      = .left
        label.font              = UIFont.systemFont(ofSize: 15)
        label.frame.origin.y    = self.bounds.height - 20 - label.frame.height
        self.addSubview(label)
        return label
    }()
    
    lazy var valueLabel: UILabel = {
        let label               = UILabel()
        label.textAlignment     = .right
        label.font              = UIFont.boldSystemFont(ofSize: 14)
        label.textColor         = UIColor(hexString: "4397FF")
        label.frame             = CGRect(x: self.arrowImageView.frame.minX - 70, y: 0, width: 60, height: self.bounds.height)
        self.addSubview(label)
        return label
    }()
    
    lazy var arrowImageView: UIImageView = {
        let imageView           = UIImageView(image: UIImage(named: "setting_app_arrow_right"))
        imageView.frame         = CGRect(x: self.bounds.width - 35, y: (self.bounds.height - 20) / 2, width: 20, height: 20)
        self.addSubview(imageView)
        return imageView
    }()
    
    init() {
        super.init(frame: CGRect(x: 0, y: 0, width: 0, height: 75))
    }
    
    private override init(frame: CGRect) {
        super.init(frame: frame)
    }
    
    required init?(coder aDecoder: NSCoder) {
        super.init(coder: aDecoder)
    }
    
    func addLine() {
        let line = UIView()
        line.frame = CGRect(x: 25, y: 0, width: bounds.width - 25, height: 1)
        line.backgroundColor = UIColor(red:0.85, green:0.85, blue:0.85, alpha:1.00)
        self.addSubview(line)
    }
}


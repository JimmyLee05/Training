//
//  DistanceView.swift
//  myForm
//
//  Created by bb on 2017/6/3.
//  Copyright © 2017年 bb. All rights reserved.
//

import UIKit
import SnapKit

class DistanceView: UIView {

    var distanceLabel:UILabel!
    var unitLabel:UILabel!

    override init(frame: CGRect) {
        super.init(frame: frame)
        
        //self.backgroundColor = UIColor.gray
        
        distanceLabel = UILabel()
        distanceLabel.text = "0.00"
        distanceLabel.textColor = UIColor.white
        distanceLabel.textAlignment = .center
        //distanceLabel.backgroundColor = UIColor.green
        distanceLabel.font = UIFont.init(name: "DINEngschriftStd", size: 120)
        self.addSubview(distanceLabel)
        distanceLabel.snp.makeConstraints({ (make) in
            make.center.equalTo(self)
            make.width.lessThanOrEqualToSuperview()
            make.height.equalToSuperview()
        })
        
        unitLabel = UILabel()
        unitLabel.text = "公里"
        unitLabel.textColor = UIColor.lightText
        unitLabel.textAlignment = .center
        //unitLabel.backgroundColor = UIColor.red
        unitLabel.font = UIFont.systemFont(ofSize: 12)
        self.addSubview(unitLabel)
        unitLabel.snp.makeConstraints({ (make) in
            make.left.equalTo(distanceLabel.snp.right)
            make.centerY.equalTo(distanceLabel).offset(20)
            make.width.greaterThanOrEqualTo(46)
            make.height.equalTo(20)
        })
    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

}

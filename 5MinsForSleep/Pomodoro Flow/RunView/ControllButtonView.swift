//
//  ControllButtonView.swift
//  myForm
//
//  Created by bb on 2017/6/2.
//  Copyright © 2017年 bb. All rights reserved.
//

import UIKit
import SnapKit

class ControllButtonView: UIView {
    
    var button:UIButton!
    var circleView:CircleView!

    override init(frame: CGRect) {
        super.init(frame: frame)
        
        circleView = CircleView()
        self.addSubview(circleView)
        circleView.snp.makeConstraints({ (make) in
            make.left.equalTo(self)
            make.top.equalTo(self)
            make.right.equalTo(self)
            make.bottom.equalTo(self)
        })
        
        button = UIButton()
        button.setTitle("开始", for: .normal)
        button.layer.cornerRadius = (frame.width - 10)/2
        button.layer.masksToBounds = true
        button.addTarget(self, action: #selector(ControllButtonView.touchDown), for: .touchDown)
        self.addSubview(button)
        button.snp.makeConstraints({ (make) in
            make.left.equalTo(self).offset(5)
            make.top.equalTo(self).offset(5)
            make.right.equalTo(self).offset(-5)
            make.bottom.equalTo(self).offset(-5)
        })

    }
    
    //按下
    func touchDown(){
        Animation.scale(view: self)
    }

    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

}

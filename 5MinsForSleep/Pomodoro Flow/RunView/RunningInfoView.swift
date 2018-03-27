//
//  RunningInfoView.swift
//  myForm
//
//  Created by bb on 2017/6/2.
//  Copyright © 2017年 bb. All rights reserved.
//

import UIKit
import SnapKit

class RunningInfoView: UIView {

    var image:UIImageView!
    var number:UILabel!
    var title:UILabel!

    override init(frame: CGRect) {
        super.init(frame: frame)

        image = UIImageView()
        //image.backgroundColor = UIColor.blue
        image.contentMode = .scaleAspectFit
        self.addSubview(image)
        image.snp.makeConstraints({ (make) in
            make.left.equalTo(self)
            make.top.equalTo(self)
            make.right.equalTo(self)
            make.height.equalTo(22)
        })

        title = UILabel()
        //title.backgroundColor = UIColor.green
        title.textAlignment = .center
        title.textColor = UIColor.lightText
        title.font = UIFont.systemFont(ofSize: 12)
        self.addSubview(title)
        title.snp.makeConstraints({ (make) in
            make.left.equalTo(self)
            make.bottom.equalTo(self)
            make.right.equalTo(self)
            make.height.equalTo(20)
        })

        number = UILabel()
        //number.backgroundColor = UIColor.brown
        number.textAlignment = .center
        number.textColor = UIColor.white
        number.contentMode = .center
        number.font = UIFont.init(name: "DINEngschriftStd", size: 38)
        self.addSubview(number)
        number.snp.makeConstraints({ (make) in
            make.left.equalTo(self)
            make.top.equalTo(image.snp.bottom).offset(10)
            make.bottom.equalTo(title.snp.top)
            make.right.equalTo(self)
        })


    }

    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
}


//
//  RoundedButton.swift
//  Pomodoro Flow
//
//  Created by 李南君 on 2018/3/15.
//  Copyright © 2018年 JimmyLee. All rights reserved.
//

import UIKit

class RoundedButton: UIButton {

    let defaultColor = UIColor(red: 240/255, green: 65/255, blue: 90/255, alpha: 1)
    let highlightedColor = UIColor(red: 220/255, green: 70/255, blue: 70/255, alpha: 1)

    required init?(coder aDecoder: NSCoder) {
        super.init(coder: aDecoder)

        layer.cornerRadius = 8
        layer.backgroundColor = defaultColor.cgColor
    }

    override var isHighlighted: Bool {
        didSet {
            if isHighlighted {
                layer.backgroundColor = highlightedColor.cgColor
            } else {
                layer.backgroundColor = defaultColor.cgColor
            }
        }
    }
}


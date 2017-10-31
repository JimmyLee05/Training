//
//  NewBaseMyntMapViewController.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/31.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit

public extension Date {
    
    var dateString: String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        return formatter.string(from: self)
    }
}



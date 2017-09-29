//
//  NewOrderListTableViewCell.swift
//  MYNT
//
//  Created by 李南君 on 2017/9/29.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit

class NewOrderListTableViewCell: UITableViewCell {
    
    //充值日期
    @IBOutlet weak var dateLabel: UILabel!
    //充值时间
    @IBOutlet weak var hourLabel: UILabel!
    //充值金额
    @IBOutlet weak var moneyLabel: UILabel!
    //充值月份
    @IBOutlet weak var monthLabel: UILabel!
    //充值状态
    @IBOutlet weak var stateLabel: UILabel!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }
    
}

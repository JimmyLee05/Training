//
//  NewMyntSimCheckTableViewCell.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/17.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit

class NewMyntSimCheckTableViewCell: UITableViewCell {
    
    @IBOutlet
    @IBOutlet
    
    fileprivate var
    fileprivate var
    fileprivate var
    
    var progress: Mynt.CheckSimProgress = .none {
        
    }
    
    override func awakeFromNib() {
        super.awakeFromNib()
        selectionStyle = .none
        
        if stateLayer == nil {
            stateLayer = CALayer()
        }
    }
    
    override func setSelected() {
        
    }
    
    func setState(isSuccess: Bool) {
        
    }
    
    func stopRotate() {
        
    }
    
    func startRotate() {
        
    }
}

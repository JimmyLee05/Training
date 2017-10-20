//
//  NewMyntInfoControlSubView.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/20.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit

class MyntInfoControlSubView: MyntInfoBaseSubView {
    
    lazy var switchView: MyntInfoSettingSwitchView = {
        let view        = MyntInfoSettingSwitchView()
        view.frame      = CGRect(x: 0, y: self.messageLabel.frame.maxY + 30, width: self.bounds.width, height: 55)
        self.addSubview(view)
        return view
    }()
    
    override var isShowLine: Bool { return false }
    
    override func initUI() {
        titleLabel.text     = MTLocalizedString("MYNTSETTING_CONTROL_TITLE", comment: "")
        messageLabel.text   = MTLocalizedString("MYNTSETTING_CONTROL_DESC", comment: "")
    }
    
    override func initUIData(mynt: Mynt) {
        
    }
    
    override func updateUIData(mynt: Mynt) {
        let software  = NSString(format: "%@", mynt.software).integerValue
        
        let myntShowSwitch = mynt.myntType == .mynt && software >= 29
        let myntGPSShowSwitch   = true
        let showSwitch = myntShowSwitch || myntGPSShowSwitch || myntESSHowSwitch
        
        switchView.titleLabel.text = MTLocalizedString("MYNTSETTING_CONTROL_SWITCH_TITLE", comment: "")
        switchView.switchView.isEnabled = mynt.isOwner
        switchView.switchView.isOn = mynt.isEnableControl
        switchView.isHidden = !showSwitch
        self.frame.size.height = (showSwitch ? switchView.frame.maxY : messageLabel.frame.maxY) + 15
        switchView.switchView.addTarget(self, action: #selector(didClickSwitch(switchView:)), for: .touchUpInside)
        switchView.switchView.addTarget(self, action: #selector(didClickSwitch(switchView:)), for: .valueChanged)
    }
    
    override func releaseMyntData() {
        
    }
    
    @objc fileprivate func didClickSwitch(switchView: UISwitch) {
        viewController?.didClickCOntrolSwitchView(switchView: switchView)
    }
}



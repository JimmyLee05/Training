//
//  NewMyntInfoButtonsSubView.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/20.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit

class MyntInfoButtonsSubview: MyntInfoBaseSubView {
    
    override var isShowLine: Bool { return false }
    
    var frameChangedHandler: ((CGRect) -> Void)?
    
    override var frame: CGRect {
        didSet {
            if frame == oldValue { return }
            frameChangedHandler?(frame)
        }
    }
    
    lazy var buttonsView: MyntButtons = {
        let view = MyntButtonsView(frame: CGRect(x: 0, y: 10, width: self.bounds.width, height: 45))
        self.addSubview(view)
        return view
    }()
    
    lazy var reportHintLabel: UILabel = {
        let label               = UILabel()
        label.textAlignment     = .center
        label.text              = MTLocalizedString("SHARE_PLACEHOLDER", comment: "")
        label.font              = UIFont.systemFont(ofSize: 11)
        label.textColor         = UIColor(white: 1, alpha: 0.5)
        label.numberOfLines     = 2
        label.frame             = CGRect(x: 40, y: self.buttonsView.frame.maxY + 4, width: self.bounds.width - 80, height: 25)
        self.addSubview(label)
        return label
    }()
    
    override var uiState: MYNTUIState {
        didSet {
            buttonsView.uiState = uiState
            reportHintLabel.isHidden = mynt?.lostState == .normal
        }
    }
    
    override func initUI() {
        
    }
    
    override func initUIData(mynt: Mynt) {
        
    }
    
    override func updateUIData(mynt: Mynt) {
        buttonsView.mynt            = mynt
        buttonsView.viewController  = viewController
        buttonsView.uiState         = mynt.uiState
        
        self.frame.size.height      = mynt.isOwner ? 90 : 0
    }
    
    override func releaseMyntData() {
        
    }
}



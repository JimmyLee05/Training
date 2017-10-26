//
//  NewMyntInfoRemoveSubView.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/26.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit

class NewMyntInfoRemoveSubView: MyntInfoBaseSubView {
    
    override var linePosition: MyntInfoBaseSubView.LinePosition { return .top }
    
    //按钮
    lazy var button: BorderButton = {
        let button = BorderButton()
        button.titleLabel?.font = UIFont.systemFont(ofSize: 14)
        button.loadMyntStyle()
        button.setTitle(MTLocalizedString("MYNTSETTING_REMOVE", comment: ""), for: .normal)
        button.addTarget(self, action: #selector(NewMyntInfoRemoveSubView.didClickButton(button:)), for: .touchUpInside)
        button.contentEdgeInsets = UIEdgeInsets(top: 0, left: 20, bottom: 0, right: 20)
        button.sizeToFit()
        let width = max(200, button.frame.size.width)
        button.frame = CGRect(x: self.bounds.midX - width / 2, y: 40, width: width, height: 40)
        button.layer.cornerRadius = button.bounds.height / 2
        self.addSubview(button)
        return button
    }()
    
    //信息
    lazy var infoLabel: UILabel = {
        let label               = UILabel()
        label.textColor         = UIColor(red:0.70, green:0.70, blue:0.70, alpha:1.00)
        label.textAlignment     = .center
        label.numberOfLines     = 0
        label.font              = UIFont.systemFont(ofSize: 10)
        label.frame             = CGRect(x: 20, y: self.button.frame.maxY + 5, width: self.bounds.width - 40, height: 20)
        label.isUserInteractionEnabled = true
        label.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(didClickLabel)))
        self.addSubview(label)
        self.frame.size.height = label.frame.maxY + 60
        return label
    }()
    
    override func initUI() {
        
    }
    
    override func initUIData(mynt: Mynt) {
        loadDebugFirmewareLabel()
    }
    
    override func updateUIData(mynt: Mynt) {
        self.infoLabel.text = "\(mynt.sn) (v\(mynt.software))"
    }
    
    override func releaseMyntData() {
        
    }
    
    @objc fileprivate func didClickLabel() {
        guard let mynt = mynt else { return }
        let pasteboard          = UIPasteboard.general
        posteboard.string       = "sn:\(mynt.sn)\nsoftware:\(mynt.software)\nhardware:\(mynt.hardware)\nfirmware:\(mynt.firmware)"
        MTToast.show("复制成功")
    }
    
    @objc fileprivate func didClickButton(button: UIbutton) {
        viewController?.didClickRemoveButton()
    }
}

// MRAK: - 线下环境加载
extension MyntInfoRemoveSubView {
    
    fileprivate func loadDebugFirmwareLabel() {
        if mynt?.hardware.contains("Bata") == false { return }
        
        let label           = UILabel()
        label.text          = "DEBUG FIRMWARE"
        label.textColor     = .gray
        label.font          = UIFont.boldSystemFont(ofSize: 12)
        label.textAlignment = .left
        label.translatesAutoresizingMaskIntoConstraints = false
        self.addSubview(label)
        self.addConstraints(NSLayoutConstraint.constraints(withVisualFormat: "H:|-5-[label]", options: .directionLeadingToTrailing, metrics: nil, views: ["label": label]))
        self.addConstraints(NSLayoutConstraint.constraints(withVisualFormat:
            "V:[label]-5-",
                                                           options: .directionLeadingToTailing,
                                                           metrics: nil,
                                                           views: ["label": label]))
    }
}

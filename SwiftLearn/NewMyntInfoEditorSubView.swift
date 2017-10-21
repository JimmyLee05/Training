//
//  NewMyntInfoEditorSubView.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/21.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit

class MyntInfoEditorSubView: MyntInfoBaseSubView, UITextFieldDelegate {
    
    override var isShowLine: Bool { return false }
    
    class ButtonView: UIButton {
        
        lazy var iconImageView: UIImageView = {
            let view        = UIImageView()
            self.addSubview(view)
            return view
        }()
        
        lazy var nameLabel: UILabel = {
            let label               = UILabel()
            label.textColor         = UIColor(red:0.29, green:0.29, blue:0.29, alpha:1.00)
            label.textAlignment     = .center
            label.font              = UIFont.systemFont(ofSize: 11)
            self.addSubview(label)
            return label
        }()
        
        override func layoutSubviews() {
            super.layoutSubviews()
            let width: CGFloat = 35
            iconImageView.frame = CGRect(x: bounds.width / 2 - width / 2, y: 0, width: width, height: width)
            nameLabel.frame     = CGRect(x: 0, y: iconImageView.frame.maxY + 5, width: bounds.width, height: 15)
        }
    }
    
    lazy var renameLabel: UILabel = {
        let label               = UILabel()
        label.text              = MTLocalizedString("RENAME", comment: "重命名")
        label.textColor         = UIColor(red:0.29, green:0.29, blue:0.29, alpha:1.00)
        label.textAlignment     = .center
        label.font              = UIFont.systemFont(ofSize: 16)
        label.frame             = CGRect(x: 0, y: 18, width: self.bounds.width, height: 20)
        self.addSubview(label)
        return label
    }()
    
    lazy var avatarLabel: UILabel = {
        let label               = UILabel()
        label.text              = MTLocalizedString("CUSTOMIZE_THUMBNAIL", comment: "设置缩略图")
        label.textColor         = UIColor(red:0.29, green:0.29, blue:0.29, alpha:1.00)
        label.textAlignment     = .center
        label.font              = UIFont.systemFont(ofSize: 16)
        label.frame             = CGRect(x: 0, y: self.renameTextField.frame.maxY + 20, width: self.bounds.width, height: 20)
        self.addSubview(label)
        return label
    }()
    
    lazy var renameTextField: UITextField = {
        let width: CGFloat = 200
        let textField                   = UITextField()
        textField.delegate              = self
        textField.backgroundColor       = UIColor(red:0.96, green:0.96, blue:0.98, alpha:1.00)
        textField.frame                 = CGRect(x: self.bounds.width / 2 - width / 2,self.renameLabel.frame.maxY + 11, width: width, height: 30)
        textField.layer.cornerRadius    = textField.bounds.height / 2
        textField.textAlignment         = .center
        textField.font                  = UIFont.systemFont(osSize: 14)
        textField.returnKeyType         = .done
        self.addSubview(textField)
        return textField
    }()
    
    lazy var pictureButton: ButtonView = {
        let button = ButtonView()
        button.iconImageView.image = UIImage(named: "setting_account_customize_album")
        button.nameLabel.text = MTLocalizedString("GALLERY", comment: "相册")
        self.addSubview(button)
        return button
    }()
    
    lazy var cameraButton: ButtonView = {
        let button = ButtonView()
        button.iconImageView.image = UIImage(named: "setting_account_customize_camera")
        button.nameLabel.text = MTLocalizedString("CAMERA", comment: "相机")
        self.addSubview(button)
        return button
    }()
    
    lazy var defaultButton: ButtonView = {
        let button = ButtonView()
        if let mynt = self.mynt {
            switch mynt.myntType {
            case .mynt:
                button.iconImageView.image = UIImage(named: "homepage_customize_thumbnail_mynt")
            case .myntGPS:
                button.iconImageView.image = UIImage(named: "homepage_customize_thumbnail_gps")
            case .myntES:
                button.iconImageView.image = UIImage(named: "homepage_customize_thumbnail_es")
            case .none:
                button.iconImageView.image = UIImage(named: "homepage_customize_thumbnail_mynt")
            }
        } else {
            button.iconImageView.image = UIImage(named: "homepage_customize_thumbnail_mynt")
        }
        button.nameLabel.text = MTLocalizedString("DEFAULT", comment: "默认")
        self.addSubview(button)
        return button
    }()
    
    override func initUI() {
        self.backgroundColor = .white
        
        let count: CGFloat  = 3
        let width: CGFloat  = 100
        let height: CGFloat = 55
        let minY: CGFloat   = avatarLabel.frame.maxY + 15
        let space: CGFloat  = (self.bounds.width - width * count) / (count + 1)
        
        let buttons: [ButtonView] = [pictureButton, cameraButton, defaultButton]
        for i in 0..<buttons.count {
            buttons[i].frame = CGRect(x: space * CGFloat(i + 1) + width * CGFloat(i), y: minY, width: width, height: height)
            buttons[i].addTarget(self, action: #selector(didClickEditThumb(button:)),
                                 for: .touchUpInside)
        }
        self.frame.size.height = 210
    }
    
    override func initUIData(mynt: Mynt) {
        
    }
    
    override func updateUIData(mynt: Mynt) {
        renameTextField.text = mynt.name
    }
    
    override func releaseMyntData() {
        
    }
    
    @objc fileprivate func didClickEditThumb(button: ButtonView) {
        switch button {
        case pictureButton:
            guard let viewController = ViewController else { return }
            
        }
    }
}





















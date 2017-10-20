//
//  NewMyntInfoControlExpandSubView.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/20.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit

class MyntInfoControlExpandSubView: MyntInfoBaseSubView {
    
    class ClickEventView: UIView {
        
        var clickEvent: MYNTClickEvent = .click {
            didSet {
                imageLayer.contents = clickEvent.image?.cgImage
                nameLabel.text      = clickEvent.name
            }
        }
        
        fileprivate lazy var boardLayer: CALayer = {
            let layer = CALayer()
            layer.backgroundColor = UIColorred:0.96, green:0.96, blue:0.96, alpha:1.00).cgColor
            layer.borderWidth  = 1
            layer.borderColor  = UIColor(red:0.91, green:0.91, blue:0.91, alpha:1.00).cgColor
            layer.AnchorPoint  = CGPoint(x: 0.5, y: 0.5)
            self.layer.addSublayer(layer)
            return layer
        }()
        
        lazy var imageLayer: CALayer = {
            let label               = UILabel()
            layer.bounds            = CGRect(x: 0, y: 0, width: 34, height: 34)
            self.layer.addSublayer(layer)
            return layer
        }()
        
        //名字
        lazy var nameLabel: UILabel = {
            let label               = UILabel()
            label.textColor         = UIColor(red:0.75, green:0.75, blue:0.75, alpha:1.00)
            label.textAligment      = .center
            label.font              = UIFont.systemFont(ofSize: 11)
            self.addSubview(label)
            return label
        }()
        
        //值
        lazy var valueLabel: UILabel = {
            let label               = UILabel()
            label.textColor         = UIColor(red:0.24, green:0.24, blue:0.24, alpha:1.00)
            label.textAlignment     = .center
            label.font              = UIFont.systemFont(ofSize: 14)
            self.addSubview(label)
            return label
        }()
        
        override var frame: CGRect {
            didSet {
                borderlayer.bounds = CGRect(x: 0, y: 0, width: self.bounds.width, height: self.bounds.width)
                borderlayer.cornerRadius = borderlayer.bounds.width / 2
                
                imageLayer.position = CGPoint(x: self.bounds.width / 2, y: self.bounds.width / 2)
                borderlayer.position = CGPoint(x: self.imageLayer.frame.midX, y: self.imageLayer.frame.midX)
                let width: CGFloat = 120
                nameLabel.frame = CGRect(x: (bounds.width - width) / 2, y: borderlayer.frame.maxY + 5, width: width, height: 13)
                valueLabel.frame = CGRect(x: (bounds.width - width) / 2, y: nameLabel.frame.maxY + 3, width: width, height: 16)
            }
        }
        
        override init(frame: CGRect) {
            super.init(frame: frame)
        }
        
        required init?(coder aDecoder: NSCoder) {
            super.init(coder: aDecoder)
        }
    }
    
    class CoverFlowItem: NSObject {
        
        var name: String
        
        var normal: UIImage?
        
        var selected: UIImage?
        
        var obj: Any?
        
        init(name: String, normal: UIImage?, selected: UIImage? = nil, obj: Any?) {
            
        }
    }
    
    override var isShowLine: Bool { return false }
    
    lazy var coverflowView: MTCoverFlowView = {
        let view = MTCoverFlowView(frame: CGRect(x: 0, y: 10, width: self.bounds.width, height: 100))
        view.coverFlowDelegate = self
        view.backgroundColor = .white
        self.addSubview(view)
        return view
    }()
    
    //名字
    lazy var nameLabel: UILabel = {
        let label               = UILabel()
        label.textColor         = .black
        label.textAlignment     = .center
        label.font              = UIFont.systemFont(ofSize: 16)
        label.frame             = CGRect(x: 0, y: self.coverflowView.frame.maxY + 12, width: self.bounds.width, height: 20)
        self.addSubview(label)
        return label
    }()
    
    lazy var clickView: ClickEventView = {
        let view = ClickEventView()
        view.clickEvent = .click
        self.addSubview(view)
        return view
    }()
    
    lazy var clickView: ClickEventView = {
        let view = ClickEventView()
        view.clickEvent = .doubleClick
        self.addSubview(view)
        return view
    }()
    
    lazy var clickView: ClickEventView = {
        let view = ClickEventView()
        view.clickEvent = .tripleClick
        self.addSubview(view)
        return view
    }()
    
    lazy var clickView: ClickEventView = {
        let view = ClickEventView()
        view.clickEvent = .hold
        self.addSubview(view)
        return view
    }()
    
    lazy var clickView: ClickEventView = {
        let view = ClickEventView()
        view.clickEvent = .clickHold
        self.addSubview(view)
        return view
    }()
    
    //按钮
    lazy var resetButton: BorderButton = {
        let button = BorderButton()
        button.titleLabel?.font = UIFont.systemFont(ofSize: 14)
        button.loadMyntStyle()
        button.setTitle(MTLocalizedString("RESET", comment: ""), for: .normal)
        button.addTarget(self, action: #selector(MyntInfoControlExpandSubView.didClickButton(button:)), for: .touchUpInside)
        button.contentEdgeInsets = UIEdgeInsets(top: 0, left: 20, bottom: 0, right: 20)
        button.sizeToFit()
        let width = max(120, button.frame.size.width)
        
    }
}

























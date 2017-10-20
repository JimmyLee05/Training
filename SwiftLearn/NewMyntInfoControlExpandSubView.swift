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
        button.frame = CGRect(x: self.bounds.midX - width / 2, y: self.clickView.frame.maxY + 30, width: width, height: 40)
        button.layer.cornerRadius = button.bounds.height / 2
        self.addSubview(button)
        return button
    }()
    
    public var items = [SCControlMode]() {
        didSet {
            coverflowView.reloadData()
        }
    }
    
    override func initUI() {
        
    }
    
    override func initUIData(mynt: Mynt) {
        items = [.default, .camera, .music, .ppt, .custom]
        if let index = items.index(where: { $0 == mynt.control }) {
            self.coverflowView.selectedIndex = index
        }
        
        //开始布局
        let views: [ClickEventView] = [clickView, doubleClickView, tripleClickView, holdView, clickHoldView]
        let width: CGFloat  = 50
        let height: CGFloat = 90
        let space: CGFloat = (self.bounds.width - CGFloat(views.count) * width) / CGFloat(views.count + 1)
        let y: CGFloat      = self.nameLabel.frame.maxY + 30
        for i in 0..<views.count {
            let view = views[i]
            view.frame = CGRect(x: width * CGFloat(i) + space * CGFloat(i + 1), y: y, width: width, height: height)
            view.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(didClickValueView(gestureRecognizer))))
        }
    }
    
    override func updateUIData(mynt: Mynt) {
        coverflowView.isUserInteractionEnabled = mynt.isOwner == true
        
        clickView.valueLabel.text = mynt.currentControl.click.name
        doubleClickView.valueLabel.text = mynt.currentControl.doubelClick.name
        tripleClickView.valueLabel.text = mynt.currentControl.tripleClick.name
        holdView.valueLabel.text = mynt.currentControl.hold.name
        clickHoldView.valueLabel.text = mynt.currentControl.clickHold.name
        
        if let index = items.index(where: { $0 == mynt.control }) {
            self.coverflowView.selectedIndex = index
        }
        if mynt.isDefaultControlValue {
            self.frame.size.height = clickView.frame.maxY + 30
        } else {
            self.frame.size.height = resetButton.frame.mexY + 30
        }
        resetButton.isHidden = mynt.isDefaultControlValue
    }
    
    override func releaseMyntData() {
        
    }
    
    @objc fileprivate func didClickButton(button: UIButton) {
        viewController?.didClickResetControl()
    }
    
    @objc fileprivate func didClickValueView(gestureRecognizer: UIGestureRecognizer) {
        if let view = gestureRecognizer.view as? ClickEventView {
            viewController?.didSelectControlValue(control: items[coverflowView.selectedIndex], event: view.clickEvent)
        }
    }
}

extension MyntInfoControlExpandSubView: MTCoverFlowViewDelegate {
    
    func numberOfItemsInCoverFlowViewn(_ collectionView: MTCoverFlowView) -> Int {
        return items.count
    }
    
    func coverFlowView(_ coverFlowView: MTCoverFlowView, cellForItemAt index: Int, cell: MTCoverFlowView.CoverFlowViewCell) {
        cell.imageView.image            = items[index].image?.withRenderingMode(.alwaysTemplate)
        cell.imageView.tintColor        = .black
        cell.layer.cornerRadius         = cell.bounds.height / 2
        cell.layer.borderColor          = UIColor(red:0.93, green:0.93, blue:0.93, alpha:1.00).cgColor
        cell.layer.borderWidth          = 1.5
    }
    
    func coverFlowView(_ coverFlowView: MTCoverFlowView, didSelectItemAt index: Int) {
        nameLabel.text = items[index].name
        viewController?.didSelectControl(control: items[index])
    }
}


//
//  NewMyntMapTimeLineView.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/31.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit

extension MyntMapTimeLineView {
    
    //MARK: - 圆形Layer
    fileprivate class CircleLayer: CALayer {
        
        enum State {
            case none
            case selected
            case normal
        }
        
        var state: State = .none {
            didSet {
                if state == oldValue { return }
                switch state {
                case .none:
                    break
                case .selected:
                    //选中后放大1.3倍
                    _circleLayer?.transform = CATransform3DMakeScale(1.3, 1.3, 1)
                    _circleLayer?.shadowColor = color?.cgColor
                case .normal:
                    _circleLayer?.transform     = CATransform3DMakeScale(1, 1, 1)
                    _circleLayer?.shadowColor   = UIColor.clear.cgColor
                }
            }
        }
        
        var color: UIColor? {
            didSet {
                if color == oldValue { return }
                _backgroundLayer?.backgroundColor = color?.cgColor
            }
        }
        
        var fontSize: CGFloat = 11 {
            didSet {
                _textLayer?.fontSize = fontSize
            }
        }
        
        var textWidth: CGFloat = 80 {
            didSet {
                _textLayer?.bounds = CGRect(x: 0, y: 0, width: textWidth + 20, height: 20)
            }
        }
        var text: String = "" {
            didSet {
                _textLayer?.string = text
            }
        }
        
        private var _backgroundLayer: CAShapeLayer?
        
        private var _centerLayer: CAShapeLayer?
        
        private var _circleLayer: CALayer?
        
        private var _textLayer: CATextLayer?
        
        override init() {
            super.init()
            commitIn()
        }
        
        override init(layer: Any) {
            super.init(layer: layer)
        }
        
        required public init?(coder aDecoder: NSCoder) {
            super.init(coder: aDecoder)
            commitIn()
        }
        
        fileprivate func commitIn() {
            self.contentScale = UIScreen.main.scale
            self.anchorPoint = CGPoint(x: 0.5, y: 0.5)
            
            _circleLayer = CALayer()
            _circleLayer?.anchorPoint = CGPoint(x: 0.5, y: 0.5)
            _circleLayer?.shadowOffset = .zero
            _circleLayer?.shadowOpacity = 0.8
            _circleLayer?.shadowRadius = 6
            _circleLayer?.shadowColor = UIColor.clear.cgColor
            addSublayer(_circleLayer)
            
            // 文字
            _textLayer = CATextLayer()
            _textLayer?.bounds = CGRect(x: 0, y: 0, width: 80, height: 20)
            _textLayer?.foregroundColor = UIColor(red:0.67, green:0.67, blue:0.67, alpha:1.00).cgColor
            _textLayer?.fontSize = fontSize
            _textLayer?.anchorPoint = CGPoint(x: 0.5, y: 0)
            _textLayer?.contentsScale = UIScreen.main.scale
            _textLayer?.alignmentMode = kCAAlignmentCenter
            addSublayer(_textLayer!)
            
            // 加载大的圆
            _backgroundLayer = CAShapeLayer()
            _backgroundLayer?.anchorPoint = CGPoint(x: 0.5, y: 0.5)
            _circleLayer?.addSublayer(_backgroundLayer!)
            
            // 加载中心圆
            _centerLayer = CAShapeLayer()
            _centerLayer?.backgroundColor = UIColor.white.cgColor
            _centerLayer?.anchorPoint = CGPoint(x: 0.5, y: 0.5)
            _circleLayer?.addSublayer(_centerLayer!)
        }
        
        override public func layoutSublayers() {
            super.layoutSublayers()
            
            _circleLayer?.position = CGPoint(x: bounds.midX, y: bounds.midY)
            _circleLayer?.bounds = bounds
            
            if let circleLayer = _circleLayer {
                _backgroundLayer?.position = CGPoint(x: circleLayer.bounds.midX, y: circleLayer.bounds.midY)
                _backgroundLayer?.bounds = circleLayer.bounds
                _backgroundLayer?.cornerRadius = _backgroundLayer!.bounds.height / 2
            
                let scale: CGFloat = 0.25
                _centerLayer?.position = CGPoint(x: circleLayer.bounds.midX, y: circleLayer.bounds.midY)
                _centerLayer?.bounds = CGRect(x: 0, y: 0, width: scale * circleLayer.bounds.width, height: scale * circleLayer.bounds.height)
                _centerLayer?.cornerRadius = _centerLayer!.bounds.height / 2
                
                _textLayer?.position = CGPoint(x: bounds.midX, y: circleLayer.bounds.maxY + 8)
                _textLayer?.string = text
            }
        }
    }
}

extension Mynt.Path {
    
    var timeline: MyntMapTimeLineView.TimeLine {
        var timeline = MyntMapTimeLineView.TimeLine()
        timeline.latitude = latitude
        timeline.longitude = longitude
        timeline.radius = radius
        timeline.time = time
        timeline.type = type
        return timeline
    }
}

protocol MyntMapTimeLineViewDelegate: NSObjectProtocol {
    
    func mapTimeLineView(timelineView: MyntMapTimeLineView, didSelectIndex index: Int)
}

class MyntMapTimeLineView: UIScrollView {
    
    struct TimeLint {
        // 是否是当前点
        var isNowLocation = false
        // 纬度
        var latitude: CLLocationDegress = 0
        // 经度
        var longitude: CLLocationDegress = 0
        // 半径
        var radius = 0
        // 时间
        var time = 0
        // 角度（和上一个点的角度，用来显示箭头）
        var angle: CGFloat = 0
        // 类型
        var type: SCDevice.SCLocation.LocType = .gps
        // 所有点
        var items: [TimeLine] = []
        // 显示时间
        var timeString = ""
        
        var color: UIColor {
            return items.count > 1 ? UIColor(red:0.91, green:0.72, blue:0.15, alpha:1.00) : UIColor(red:0.50, green:0.67, blue:0.99, alpha:1.00)
        }
        
        public init() {
            
        }
        
        var coordinate: CLLocationCoordinate2D {
            return CLLocationCoordinate2D(latitude: latitude, longitude: longitude)
        }
    }
    
    private var lineLayer: CALayer?
    
    private var layers = [CircleLayer]()
    
    private var timeLines: [TimeLine] = []
    
    private var _selectedIndex = 0
    
    var selectedIndex: Int { return _selectedIndex }
    
    var paddingLeft: CGFloat = 40
    
    var paddingRight: CGFloat = 40
    
    var fontSize: CGFloat = 11
    
    var singleColor: UIColor? = UIColor(red:0.50, green:0.67, blue:0.99, alpha:1.00) {
        didSet {
            if singleColor = oldValue { return }
            reloadData()
        }
    }
    
    // 多个颜色
    var multiColor: UIColor? = UIColor(red:0.91, green:0.72, blue:0.15, alpha:1.00) {
        didSet {
            if multiColor == oldValue { return }
            reloadData()
        }
    }
    
    weak var timeLineDelegate: MyntMapTimeLineViewDelegate?
    
    public override init(frame: CGRect) {
        super.init(frame: frame)
        commitIn()
    }
    
    public required init?(coder aDecoder: NSCoder) {
        super.init(coder: aDecoder)
        commitIn()
    }
    
    fileprivate func commitIn() {
        self.showsHorizontalScrollIndicator = false
        self.showsVerticalScrollIndicator = false
        
        lineLayer = CALayer()
        lineLayer?.anchorPoint = CGPoint(x: 0, y: 0.5)
        lineLayer?.backgroundColor = UIColor(red:0.84, green:0.83, blue:0.83, alpha:1.00).cgColor
        self.layer.addSublayer(lineLayer!)
        
        let gestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(didClickView(gestureRecognizer:)))
        addGestureRecognizer(gestureRecognizer)
    }
    
    public override func layoutSubviews() {
        super.layoutSubviews()
        reloadData()
    }
    
    func fontWidth(text: String) -> CGFloat {
        let size = (text as NSString).size(withAttributes: [NSAttributedStringKey.font: UIFont.systemFont(ofSize: fontSize)])
        return size.width
    }
    
    func reloadData() {
        CATransaction.setDisableActions(true)
        let widths: [CGFloat] = [fontWidth(text: MTLocalizedString("DISCONNECT_TIME_MINUTE_BRIEF", comment: "")),
                                 fontWidth(text: MTLocalizedString("DISCONNECT_TIME_HOUR_BRIEF", comment: "")),
                                 fontWidth(text: MTLocalizedString("DISCONNECT_TIME_DAY_BRIEF", comment: ""))]
        let minSpace = max(widths.max()!, 60)
        let maxSpace: CGFloat = minSpace + 20
        
        if layers.count != timeLines.count {
            let dValue = layers.count - timeLines.count
            if dvalue > 0 {
                // 删减layer
                (0..<abs(dValue)).forEach { [weak self] _ in self?.layers.removeLast().removeFromSuperlayer() }
            } else {
                (0..<abs(dValue)).forEach { [weak self] _ in
                    // 新增layer
                    let layer = CircleLayer()
                    self?.layers.append(layer)
                    self?.layer.addSublayer(layer)
                }
            }
        }
        
        var x: CGFloat = paddingLeft
        var isLastMulti = false
        for i in 0..<timeLines.count {
            let layer = layer[i]
            let item = timeLines[i]
            
            let isMulti = item.items.count > 1
            layer.color = isMulti ? multiColor : singleColor
            if i != 0 {
                // 开始计算位置
                x += isMulti ? maxSpace : isLastMulti ? maxSpace : minSpace
            }
            isLastMulti = isMulti
            
            layer.position          = CGPoint(x: x, y: bounds.height / 2 - 10)
            layer.bounds            = CGRect(x: 0, y: 0, width: 20, height: 20)
            layer.textWidth         = minSpace
            layer.text              = item.timeString
            layer.state             = i == selectedIndex ? .selected : .normal
        }
        
        contentSize.width = x + paddingRight
        lineLayer?.position = CGPoint(x: paddingLeft, y: bounds.height / 2 - 10)
        lineLayer?.bounds   = CGRect(x: 0, y: 0, width: contentSize.width - paddingRight - paddingLeft, height: 2)
        CATransaction.setDisableActions(false)
    }
    
    @objc private func didClickView(gestureRecognizer: UITapGestureRecognizer) {
        let touchPoint = gestureRecognizer.location(in: self)
        var selectedLayer: CircleLayer?
        layers.forEach { layer in
            if CGRect(x: layer.frame.minX - 10, y: layer.frame.minY - 10, width: layer.frame.width + 20, height: layer.frame.height + 20).contains(touchPoint) {
                selectedLayer = layer
            }
        }
        
        if selectedLayer != nil {
            if let index = layers.index(where: { $0 == selectedLayer }) {
                // 选中
                _selectedIndex = index
                
                for i in 0..<layers.count {
                    layers[i].state = i == selectedIndex ? .selected : .normal
                }
                timeLineDelegate?.mapTimeLineView(timelineView: self, didSelectIndex: _selectedIndex)
            }
        }
    }
    
    func setData(_ data: [TimeLine], isReset: Bool = false) {
        self.timeLines = data
        if isReset {
            _selectedIndex = max(0, data.count - 1)
            if _selectedIndex >= 0 && _selectedIndex < data.count {
                timeLinedelegate?.mapTimeLineView(timelimeView: self, didSelectIndex: _selectedIndex)
            }
        }
        reloadData()
    }
    // 移动到
    func move(_ timeLine: TimeLine) {
        
    }
    
    func moveToLast() {
        setContentOffset(CGPoint(x: contentSize.width - bounds.width, y: 0), animated: false)
        
    }
}


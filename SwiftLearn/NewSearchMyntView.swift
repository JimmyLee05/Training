//
//  NewSearchMyntView.swift
//  MYNT
//
//  Created by 李南君 on 2017/11/2.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit
import MyntCoreBluetooth
import MYNTKit
import SlightechKit
import SCloudKit

infix operator ==
func == (left: GradientColor, right: GradientColor) -> Bool {
    return (left.start == right.start) && (left.end == right.end)
}

fileprivate extension SCDeviceType {
    
    var image: UIImage? {
        switch self {
        case .mynt:
            return UIImage(named: "homepage_mynt")
        case .myntGPS:
            return UIImage(named: "homepage_gps")
        case .myntES:
            return UIImage(named: "homepage_es")
        default:
            return UIImage(named: "")
        }
    }
}

class SearchMyntLayer: CALayer {
    
    var index: Int = 0
    // 角度
    var indexAngle: CGFloat = 0
    // 最大坐标
    var maxPoint: CGPoint = CGPoint.zero
    // 最小坐标
    var minPoint: CGPoint = CGPoint.zero
    // 运动范围
    var range: CGRect = CGRect.zero
    
    var centerPoint = CGPoint.zero
    
    var gradientColor = CGPoint.zero
    
    var textLayer: CATextLayer?
    
    var mynt: Mynt? {
        didSet {
            guard let mynt = mynt else {
                return
            }
            textLayer?.string = mynt.sn
        }
    }
    
    override var bounds: CGRect {
        didSet {
            textLayer?.bounds   = CGRect(x: 0, y: 0, width: bounds.width, height: 20)
            textLayer?.position = CGPoint(x: bounds.width / 2, y: bounds.height / 2)
        }
    }
    
    override init() {
        super.init()
        anchorPoint     = CGPoint(x: 0.5, y: 0.)
        contentsScale   = UIScreen.main.scale
        
        if AppConfig.isDebugMode {
            textLayer                       = CATextLayer()
            textLayer?.fontSize             = 8
            textLayer?.foregroundColor      = UIColor.black.cgColor
            textLayer?.anchorPoint          = CGPoint(x: 0.5, y: 0.5)
            textLayer?.contentsScale        = UIScreen.main.scale
            textLayer?.alignmentMode        = kCAAlignmentCenter
            addSublayer(textLayer!)
        }
    }
    
    override init(layer: Any) {
        super.init(layer: layer)
    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    func position(_ percent: CGFloat) -> CGPoint {
        let xLength = maxPoint.x - minPoint.x
        let yLength = maxPoint.y - minPoint.y
        var centerPoint = CGPoint(x: minPoint.x + xLength * (1 - percent), y: minPoint.y + yLength * (1 - percent))
        centerPoint = _checkCross(centerPoint)
        return centerPoint
    }
    
    /**
    检测越界
 
     - parameter angle: 角度
     */
    fileprivate func _checkCross(_ point: CGPoint) -> CGPoint {
        
        if indexAngle != 90 && indexAngle != 270 {
            
            let pointX = { (point: CGPoint, angle: CGFloat) -> CGFloat in return atan(angle * (π / 180)) * point.y }
            let pointY = { (point: CGPoint, angle: CGFloat) -> CGFloat in return tan(angle * (π / 180)) * point.x }
            
            var newPoint = CGPoint(x: point.x - centerPoint.x, y: point.y - centerPoint.y)
            if !range.contains(self.maxPoint) {
                repeat {
                    if point.x < range.origin.x {
                        newPoint.x = range.origin.x
                        newPoint.y = pointY(newPoint, indexAngle)
                        break
                    }
                    if point.y < range.origin.y {
                        newPoint.y = range.origin.y - centerPoint.y
                        newPoint.x = pointX(newPoint, indexAngle)
                        break
                    }
                    if point.x > range.origin.x + range.size.width {
                        newPoint.x = range.origin.x + range.size.width - centerPoint.x
                        newPoint.y = pointY(newPoint, indexAngle)
                        break
                    }
                    if point.y > range.origin.y + range.size.height {
                        newPoint.y = range.origin.y + range.size.height - centerPoint.y
                        newPoint.x = pointX(newPoint, indexAngle)
                        break
                    }
                } while (false)
            }
            newPoint = CGPoint(x: centerPoint.x + newPoint.x, y: centerPoint.y + newPoint.y)
            return newPoint
        }
        return point
    }
}

protocol SearchMyntViewDelegate: NSObjectProtocol {
    
    func searchView(_ searchView: SearchMyntView, didClickMyntLayer layer: SearchMyntLayer)
    
    func didClickResearchMynt(_ searchView: SearchMyntView)
}

class SearchMyntView: UIView {
    
    private let kRadius: CGFloat = 30
    // 顺序
    // private let kIndexList = [7, 5, 1, 6, 2, 0, 4, 3]
    // 日本顺序版
    private let kIndexList = [6, 7, 0, 1, 2, 3, 4, 5]
    private let kColors = [ColorStyle.kGoldTips, ColorStyle.kOrange,
                           ColorStyle.kPortlandOrange, ColorStyle.kCarminePink,
                           ColorStyle.kOliveHaze, ColorStyle.kMantis,
                           ColorStyle.kShamrock, ColorStyle.kSpiroDiscoBall]
    private var _mynts = [Mynt]()
    private var _layers = [Mynt: SearchMyntLayer]()
    private var _colors = [Mynt: GradientColor]()
    private var _maxRadius: CGFloat = 0
    private var _minRadius: CGFloat = 0
    private var _centerPoint = CGPoint.zero
    
    weak var delegate: SearchMyntViewDelegate?
    
    var count: Int {
        return _mynts.count
    }
    var mynts: [Mynt] {
        return _mynts
    }
    
    override init(frame: CGRect) {
        super.init(frame: frame)
        _commitIn()
    }
    
    required init?(coder aDecoder: NSCoder) {
        super.init(coder: aDecoder)
        _commitIn()
    }
    
    override func layoutSubviews() {
        super.layoutSubviews()
        
        // 计算最大宽度，最小宽度
        let widthRadius = bounds.width / 2
        let heightRadius = bounds.height / 2
        _maxRadius = max(widthRadius, heightRadius) - kRadius
        _mixRadius = kRadius * 3.6
        _centerPoint = CGPoint(x: bounds.midX, y: bounds.midY)
    }
    
    fileprivate func _commitIn() {
        backgroundColor = UIColor.clear
        isUserInteractionEnabled = true
        addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(SearchMyntView.didClickSearchView(_:))))
    }
    
    @objc func didClickSearchView(_ tapGestureRecognizer: UITapGestureRecognizer) {
        let touchPoint = tapGestureRecognizer.location(in: self)
        let centerRect = CGRect(x: bounds.midX - 30, y: bounds.midY - 30, width: 60, height: 60)
        if centerRect.contains(touchPoint) {
            delegate?.didClickResearchMynt(self)
            return
        }
        for (_, layer) in _layers {
            if layer.hitTest(touchPoint) != nil {
                // 点击
                delegate?.searchView(self, didClickMyntLayer: layer)
                return
            }
        }
    }
    
    func released() {
        _mynts = []
        _layers = [:]
        _colors = [:]
    }
    
    func addMynt(with mynt: Mynt, productType: SCDeviceType = .mynt) {
        var isNew = false
        if !_mynts.contains(mynt) {
            if _mynts.count >= 8 {
                return
            }
            
            // 添加小觅
            let color = _getGradientColor()
            let layer = SearchMyntLayer()
            let image = UIImage.create(with: kRadius * 2, icon: productType.image, color: color)
            layer.contents  = image?.cgImage
            layer.bounds    = CGRect(origin: CGPoint.zero, size: CGSize(width: kRadius * 2, height: kRadius * 2))
            self.layer.addSublayer(layer)
            
            layer.index                 = index
            layer.indexAngle            = angle
            layer.gradientColor         = color
            layer.mynt                  = mynt
            layer.minPoint              = _calcPoint(_centerPoint, radius: _minRadius, angle: angle)
            layer.maxPoint              = _calcPoint(_centerPoint, radius: _maxRadius, angle: angle)
            layer.range                 = CGRect(x: kRadius + 5, y: kRadius + 5, width: bounds.width - kRadius * 2 - 10, height: bounds.height - kRadius * 2 - 10)
            layer.centerPoint           = _centerPoint
            
            _mynts.append(mynt)
            _layers[mynt] = layer
            _colors[mynt] = color
            
            isNew = true
        }
        
        guard let layer = _layers[mynt] else {
            return
        }
        
        let max: CGFloat = 127
        let min: CGFloat = 20
        let percent = (max - abs(CGFloat(mynt.rssi))) / (max - mi)
        let position = layer.position(percent)
        if isNew {
            CATransaction.setDisableActions(false)
            layer.position = position
            CATransaction.setDisableActions(true)
            
            let opacityAnimation = CABasicAnimation(keyPath: "opacity")
            opacityAnimation.fromValue = 0
            opacityAnimation.toValue   = 1
            opacityAnimation.isRemovedOnCompletion = false
            opacityAnimation.fillMode = kCAFillModeForwards
            opacityAnimation.duration = 0.3
            opacityAnimation.timingFunction = CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseOut)
            layer.add(opacityAnimation, forKey: "opacity-layer")
            return
        }
        
        // 更新坐标
        let moveAnimation = CABasicAnimation(keyPath: "position")
        moveAnimation.fromValue = NSValue(cgPoint: layer.position)
        moveAnimation.toValue   = NSValue(cgPoint: position)
        moveAnimation.autoreverses = false
        moveAnimation.isRemovedOnCompletion = false
        moveAnimation.fillMode = kCAFillModeForwards
        moveAnimation.repeatCount = 1
        moveAnimation.duration = 0.15
        moveAnimation.timingFunction = CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseOut)
        layer.add(moveAnimation, forKey: "percent-layer")
        layer.position = position
    }
    
    func removeAll(_ mynt: Mynt? = nil, isSequence: Bool = false, completion: (() -> Void)? = nil) {
        let time: CFTimeInterval = 0.06
        let count = mynts.count
        for i in (0..<_mynts.count).reversed() {
            let _mynt = _mynts[i]
            if _mynt != mynt {
                deleteMynt(_mynt, beginTime: isSequence ? time * CFTimeInterval(i) : 0)
            }
        }
        if let completion = completion {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now() + .milliseconds(count * Int(time * 1000) + 300), execute: completion)
        }
        released()
    }
    
    func deleteMynt(_ mynt: Mynt, beginTime: CFTimeInterval = 0) {
        if _mynts.contains(mynt) {
            
        }
    }
}





















































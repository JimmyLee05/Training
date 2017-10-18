//
//  NewAskPreviewController.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/18.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit
import Social

private class AnnotationLayer: CALayer {
    
    var image: UIImage? {
        didSet {
            
        }
    }
    
    private var _backgroundLayer: CALayer!
    private var _triangleLayer: CAShapeLayer!
    private var _imageLayer: CALayer!
    
    fileprivate override var bounds: CGRect {
        didSet {
            
        }
    }
    
    override init() {
        super.init()
        _commitIn()
    }
    
    override init(layer: Any) {
        super.init(layer: layer)
        _commitIn()
    }
    
    required init?(coder aDecoder: NSCoder) {
        super.init(coder: aDecoder)
        _commitIn()
    }
    
    private func _commitIn() {
        
    }
}

class AskPreviewViewController: MYNTKitBaseViewController {
    
    fileprivate var mapView: MKMapView?
    
    @IBOutlet
    
    var shareType: SCShareType = .link
    
    private var _annotationLayer: AnnotationLayer!
    fileprivate var centerPoint = CGPoint.zero
    
    //火星坐标
    fileprivate var lostCoorCenter = CLLocationCoordinate2DZero {
        didSet {
            lostCoorCenter.china2World.reverseGeocodeLocation { [weak self] address, _ in
                self?.locationLabel.text = address
            }
        }
    }
    
    fileprivate var isRenderMapDone = false
    
    private var isInitSuccess = false
    
    override var isShowBackgroundLayer: Bool { return false }
    
    override func viewDidLoad() {
        
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    override func didDismissViewController() {
        super.didDismissViewController()
        DialogManager.shared.checkQueue()
        releaseMapView()
    }
    
    override func leftBarButtonClickedHandler() {
        dismissNavigationController(animated: true)
        MTNTKit.shared.removeMyntKitDelegate(key: selfKey)
        isFinishController = true
    }
    
    override func viewDidLayoutSubviews() {
        super.viewDidLayoutSubviews()
        
        let maskPath = UIBezierPath(roundedRect: dialogView.bounds, byRoundingCorners:
            [.topLeft, .topRight], cornerRadii: CGSize(width: 5, height: 5))
        
        if _annotationLayer != nil {
            
        }
        _annotationLayer?.position = centerPoint
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        initMapView()
    }
    
    override func viewDidDisappear(_ animated: Bool) {
        super.viewDidDisappear(animated)
        isDidAppear = false
        releaseMapView()
    }
    
    func moveToMyntCoordinate(coordinate: CLLocationCoordinate2D, radius: Double = 1000) {
        if coordinate.isNull { return }
        mapView.gotoCoordinate(coordinate, range: radius)
    }
    
    //加载地图
    func initMapView() {
        
    }
    
    //释放地图
    func releaseMapView() {
        
    }
    
    func initCoordinate() {
        
    }
    
    @IBAction func didClickLinkButton(_ sender: AnyObject) {
        
    }
    
    @IBAction func didClickFriendButton(_ sender: AnyObject) {
        
    }
    
    @IBAction func didClickMomentButton(_ sender: AnyObject) {
        
    }
    
    private func _initAnnotation() {
        
    }
}

extension AskPreviewViewController: MKMapViewDelegate {
    
    func mapViewDidFinishRenderingMap() {
        
    }
    
    func mapView() {
        
    }
}

extension AskPreviewViewController {
    
    //创建分享链接
    func createShareLink(isWechat: Bool = true, handle: @escaping () ) {
        
    }
    
    //是否已安装微信客户端
    @discardableResult
    func isInstalledWechat() -> Bool {
        if WXApi.isWXAppInstalled() && WXApi.isWXAppSupport() {
            return true
        } else {
            return false
        }
    }
    
    //跳转到微信
    func shareToWechat(_ url: String, isScene: WXScene) {
        
    }
}

extension Mynt {
    
    public func getShareIconImage(block: @escaping (UIImage?) -> Void) {
        
}


































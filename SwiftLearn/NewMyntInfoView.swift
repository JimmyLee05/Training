//
//  NewMyntInfoView.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/19.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit

extension MyntInfoViewController {
    
    func initNavigationBar() {
        view.backgroundColor = .white
        automaticallyAdjustsScrollViewInsets = false
        view.supportHideKeyBoard()
        
        setRightBarButtonItem(image: Resource.Image.Navigation.more)
        setBackBarButton()
        removeBackBarButtonTitle()
    }
    
    func initView() {
        let view = MyntInfoView(frame: winRect, viewController: self)
        self.contentView = view
        self.view.addSubview(view)
    }
}

fileprivate extension MYNTUIState {
    
    var navigationColor: UIColor {
        return self == .online ? navigationBarColor : ColorStyle.kOfflineGradientColor.start
    }
}

class MyntInfoView: UIView, UIScrollViewDelegate {
    
    //MARK: - 标题栏
    class NavigationBarView: UIView {
        
        static var statusHeight: CGFloat = 32
        
        //标题栏名字Label
        lazy var titleLabel: UILabel = {
            var y: CGFloat          = NavigationBarView.statusHeight
            let label               = UILabel(frame: CGRect(x: 0, y: y, width: self.bounds.width, height: 18))
            label.textAlignment     = .center
            label.textColor         = .white
            label.font              = UIFont.systemFont(ofSize: 13)
            self.addSubview(label)
            return label
        }()
        
        //标题栏地址Label
        lazy var addressLabel: UILabel = {
            let label               = UILabel(frame: CGRect(x: 0,
                                                            y: self.titleLabel.frame.maxY + 2,
                                                            width: self.bounds.width,
                                                            hieht: 15))
            label.textAligment      = .center
            label.textColor         = .white
            label.font              = UIFont.systemFont(ofSize: 17)
            self.addSubview(label)
            return label
        }()
        
        override init(frame: CGRect) {
            super.init(frame: frame)
        }
        
        required init?(coder aDecoder: NSCoder) {
            super.init(coder: aDecoder)
        }
    }
    
    weak var viewController: MyntInfoViewController!
    
    var uiState: MYNTUIState = .none {
        didSet {
            if uiState == oldValue { return }
            
            scrollView.subviews.forEach { ($0 as? MyntInfoBaseSubView)?.uiState = uiState }
            infoBackgroundLayer.backgroundColor = uiState.navigationColor.cgColor
            topView.backgroundColor             = uiState.navigationColor.cgColor
            navigationBarView.backgroundColor   = uiState.navigationColor
            
            updateNavigationBar()
            
            runAnimation()
        }
    }
    
    //滚动组件
    lazy var scrollView: ExpandScrollView = {
        let scrollView = ExpandScrollView(frame: self.bounds)
        if #available(iOS 11, *) {
            scrollView.contentInsetAdjustmentBehavior = .never
        }
        scrollView.showsVerticalScrollIndicator = false
        scrollView.showsHorizontalScrollIndicator = false
        scrollView.delegate = self
        self.addSubview(scrollView)
        return scrollView
    }()
    
    //顶部组件，用于拖动显示黑色部分
    lazy var topView: CALayer = {
        let layer = CALayer()
        layer.backgroundColor = self.uiState.navigationColor.cgColor
        layer.anchorPoint = .zero
        self.layer.insertSublayer(layer, at: 0)
        return layer
    }()
    
    //信息背景音乐
    lazy var infoBackgroundLayer: CALayer = {
        let layer = CALayer()
        layer.backgroundColor = self.uiState.navigationColor.cgColor
        layer.anchorPoint = .zero
        self.layer.insertSublayer(layer, at: 0)
        return layer
    }()
    
    //模拟的NavigationBar的背景
    lazy var navigationBarView: NavigationBarView = {
        NavigationBarView.statusHeight = self.viewController.statusHeight
        let view = NavigationBarView(frame: CGRect(x: 0, y: 0, width: winSize.width, height: self.viewController.navigationBarHeight))
        view.backgroundColor = self.uiState.navigationColor
        view.isHidden = true
        self.insertSubview(view, aboveSubview: self.scrollView)
        return view
    }()
    
    //信息view
    lazy var infoView: MyntInfoSubview = {
        let view = MyntInfoSubView(viewController: self.viewController)
        return view
    }()
    
    //编辑view
    lazy var editView: MyntInfoEditorSubView = {
        let view = MyntInfoEditorSubView(viewController: self.viewController)
        return view
    }()
    
    //按钮view
    lazy var buttonsView: MyntInfoButtonsSubView = {
        let view = MyntInfoButtonsSubView(viewController: self.viewController)
        return view
    }()
    
    //tipsview
    lazy var tipsView: MyntInfoTipsSubView = {
        let view = MyntInfoTipsSubView(viewController: self.viewController)
        return view
    }()
    
    //地图view
    lazy var mapsView: MyntInfoMapSubView = {
        let view = MyntInfoMapSubView(viewController: self.viewController)
        return view
    }()
    
    //丢失view
    lazy var lossView: MyntInfoLossSubView = {
        let view = MyntInfoLossSubView(viewController: self.viewController)
        return view
    }()
    
    //活动view
    lazy var activityView: MyntInfoActivitySubView = {
        let view = MyntInfoActivitySubView(viewController: self.viewController)
        return view
    }()
    
    //控制view
    lazy var controlView: MyntInfoControlSubView = {
        let view = MyntInfoControlSubView(viewController: self.viewController)
        return view
    }()
    
    //控制展开view
    lazy var controlExpandView: MyntInfoControlSubView = {
        let view = MyntInfoRemoveSubView(viewController: self.viewController)
        return view
    }()
    
    //移除view
    lazy var removeView: MyntInfoRemoveSubView = {
        let view = MyntInfoRemoveSubView(viewController: self.viewController)
        return view
    }()
    
    //丢失动画layer
    lazy var reportAnimationLayer: ReportRippleLayer = {
        let layer = ReportRippleLayer.create(superLayer: self.infoBackgroundLayer)
        return layer
    }()
    
    fileprivate init(frame: CGRect, viewController: MyntInfoViewController) {
        super.init(frame: frame)
        self.viewController = viewController
    }
    
    override func didMoveToSuperview() {
        initScrollView()
        
        //添加点击事件
        infoView.isUserInteractionEnabled = true
        infoView.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(expandEditorView)))
        
        buttonView.frameChangedHandler = { [weak self] frame in
            if let scrollView = self?.scrollView {
                self?.infoBackgroundLayer.frame = CGRect(x: 0. y: scrollView.contentOffset.y * -1, width: frame.width,height: frame.maxY)
                self?.runAnimation()
            }
        }
        updateNavigationBar()
    }
    
    required init?(coder aDecoder: NSCoder) {
        super.init(coder: aDecoder)
    }
    
    //初始化滚动组件
    fileprivate func initScrollView() {
        guard let mynt = viewController?.mynt else { return }
        
        scrollView.insertSubView(infoView)
        scrollView.insertSubView(buttonView)
        scrollView.insertSubView(tipsView)
        scrollView.insertSubView(mapsView)
        scrollView.insertSubView(lossView)
        
        if mynt.myntType == .myntGPS {
            scrollView.insertSubView(activityView)
        }
        
        let software = NSString(format: "@", mynt.software).integerValue
        let isShowControl = (mynt.myntType == .mynt && software > 10) ||
            (mynt.myntType == .myntGPS) ||
            (mynt.myntType == .myntES)
        let isShowSubControl = (mynt.myntType == .mynt && ((mynt.isEnableControl && software >= 29) || software < 29)) ||
            (mynt.myntType == .myntGPS && mynt.isEnableControl) ||
            (mynt.myntType == .myntES && mynt.isEnableControl)
        
        if isShowControl {
            scrollView.insertSubView(controlView)
        }
        if isShowControl && isShowSubControl {
            scrollView.expand(controlExpandView, below: contentView)
        }
        scrollView.insertSubView(removeView)
        
        scrollView.subviews.forEach { ($0 as? MyntInfoBaseSubView)?.uiState = mynt.uiState }
    }
    
    fileprivate func runAnimation() {
        if infoBackgroundLayer.bounds == .zero { return }
        switch uiState {
        case .report:
            reportAnimationLayer.startAnimation()
        default:
            reportAnimationLayer.stopAnimation()
        }
    }
    
    @objc fileprivate func expandEditorView(gestureRecognizer: UIGestureRecognizer) {
        viewController.didClickInfoView()
    }
    
    func updateNavigationBar() {
        navigationBarView.titleLabel.text   = infoView.nameLabel.text
        navigationBarView.addressLabel.text = infoView.distanceLabel.text
    }
    
    func scrollViewDidScroll(_ scrollView: UIScrollView) {
        CATransction.setDisableActions(true)
        let height: CGFloat = abs(min(0, scrollView.contentOffset.y))
        if height != 0 {
            topView.bounds = CGRect(x: 0, y: 0, width: winSize.width, height: height)
        }
        infoBackgroundLayer.frame = CGRect(x: 0, y: scrollView.contentOffset.y * -1, width: frame.width, height: buttonsView.frame.maxY)
        CATransition.setDisableActions(false)
        //转换
        let maxY = navigationBarView.titleLabel.convert(navigationBarView.titleLabel.frame, to: scrollView).maxY
        navigationBarView.isHidden = maxY < infoView.nameLabel.frame.maxY
    }
}


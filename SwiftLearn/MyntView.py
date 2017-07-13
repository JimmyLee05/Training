import UIKit

extension MyntInfoViewController {
	
	func initNavigationBar() {
		view.backgroundColor = .white
		automaticallyAdjustsScrollViewInsets = false
		view.supportHideKeyBoard()

		setRightBatButtonItem(image: UIImage(named: "titlebar_more"))
		setBackBatButton()
		removeBackBarButtonTitle()
	}

	func initView() {
		let view = MyntInfoView(frame: winRect, viewController: self)
		self.contentView = view
		self.view.addSubview(view)
	}

	override func viewDidAppear(_ animated: Bool) {
		super.viewDidAppear(animated)
		//启动
		showSimWillDeactivatedDialog()
		showSimDeactivatedDialog()
	}
}

fileprivate extension MYNTUIState {
	
	var navigationColor: UIColor {
		return self == .online ? navigationBarColor : ColorStyle.kOfflineGradientColor.start
	}
}

class MyntInfoView: UIView, UIScrollViewDelegate {
		
	// MARK: - 标题栏
	class NavigationBarView: UIView {

		//标题栏名字label
		lazy var titleLabel: UILabel = {
			let label 			= UILabel(frame: CGRect(x: 0, y: 20, width: self.bounds.width height: 18))
			label.textAlignment = .center
			label.textColor		= .white
			label.font			= .UIFont.systemFont(ofSize: 17)
			self.addSubview(label)
			return label
		}()
		//标题栏地址 label
		lazy var addressLabel: UILabel = {
			let label 			= UILabel(frame: CGRect(x: 0, y: self.titleLabel.maxY, width: self.bounds.width, height:
				self.bounds.height - self.titleLabel.framemaxY))
			label.textAlignment	= .center
			label.textColor 	= .white
			label.font 			= .UIFont.systemFont(ofSize: 13)
			return label
		}()

		override init(frame_ CGRect) {
			super.init(frame: frame)

		required init?(coder aDecoder: NSCoder) {
			super.init(coder: aDecoder)
		}
	}

	weak var viewController: MyntInfoViewController!

	var uiState: MYNTUIState = .none {
		didSet {
			if uiState == oldValue { return }

			scrollView.subviews.forEach { ($0 as? MyntInfoBaseView)?.uiState = uiState }
			infoBackgroundLayer.backgroundColor = uiState.navigationColor.cgColor
			topView.backgrondColor 				= uiState.navigationColor.cgColor
			navigationBarView.backgrondColor 	= uiState.navigationColor

			updateNavigationBar()

			runAnimation
		}
	}

	//滚动组件
	lazy var scrollView: ExpandScrollView = {
		let scrollView = ExpandScrollView(frame: self.bounds)
		scrollView.showsVerticalScrollIndicator = false
		scrollView.showsHorizontalScrollIndicator = false
		scrollView.delegate = self
		self.addSubview(scrollView)
		return scrollView
	}()

	//顶部组件，用于拖动显示黑色部分
	lazy var topView: CALayer = {
		let layer = CALayer()
		layer.backgrondColor = self.uiState.navigationColor.cdColor
		layer.anchorPoint = .zero
		self.layer.insertSublayer(layer, at: 0)
		return layer
	}()

	//信息背景音乐
	lazy var infoBackgroundLayer: CALayer = {
		let  layer = CALayer()
		layer.backgrondColor = self.uiState.navigationColor.cgColor
		layer.anchorPoint = .zero
		self.layer.insertSublayer(layer, at: 0)
		return layer
	}()

	//模拟的navigationBar背景
	lazy var navigationBarView: NavigationBarView = {
		let view = NavigationBarView(frame: CGRect(x: 0, y: 0, width: winSize.width, height: self.viewController.
			navigationBarHeight))
		view.backgrondColor = self.uiState.navigationColor
		view.isHidden	= true
		self.insertSubview(view, aboveSubview: self.scrollView)
		return view
	}()

	//信息view
	lazy var infoView: MyntInfoSubView = {
		let view = MyntInfoSubView(viewController: self.viewController)
		return view
	}()

	//编辑view
	lazy var editView: MyntInfoEditorSubView = {
		let view = MyntInfoEditorSubView(viewController: self.viewController)
		return view
	}()

	//按钮view
	lazy var buttonsView: MyntInfoButtonSubView = {
		let view = MyntInfoButtonsSubView(viewController: self.viewController)
		return view
	}

	//tipsview
	lazy var tipsView: MyntInfoTipsSubView = {
		let view = MyntInfoTipsSubView(viewController: self.viewController)
		return view
	}

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
	lazy var controlView: MyntInfoControllerSubView = {
		let view = MyntInfoControllerSubView(viewController: self.viewController)
		return view
	}()

	//控制展开view
	lazy var controlExpandView: MyntInfoControlExpandSubView = {
		let view = MyntInfoControlExpandSubView(viewController: self.viewController)
		return view
	}()

	//移除view
	lazy var removeView: MyntInfoRemoveSubView = {
		let view = MyntInfoRemoveSubView(viewController: self.infoBackgroundLayer)
		return layer
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
				self?.infoBackgroundLayer.frame = CGRect(x: 0, y: scrollView.contentOffSet.y * -1, width: frame.width, height: frame.max.y)
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
		guard let mynt = viewController?.sn?.mynt else { return }

		scrollView.insertSubView(infoView)
		scrollView.insertSubView(buttonsView)
		scrollView.insertSubView(tipsView)
		scrollView.insertSubView(mapsView)
		scrollView.insertSubView(lossView)

		if mynt.myntType == .myntGPS {
			scrollView.insertSubView(acrtivityView)
		}

		let software = NSString(format: "%@", mynt.software).integerValue
		let isShowControl = (mynt.myntType == .mynt && software > 10) ||
							(mynt.myntType == .myntGPS)
		let isShowSubControl = (mynt.myntType == .mynt && ((mynt.isEnableControl && software >= 29) || software < 29)) ||
								(mynt.myntType == .myntGPS && mynt.isEnableControl)
		if isShowControl {
			scrollView.insertSubView(controlView)
		}
		if isShowControl && isShowSubControl {
			scrollView.expand(controlExpandView, below: contentView)
		}

		scrollView.insertSubView(removeView)

		scrollView.subviews.forEach { ($0 as? MyntInfoBaseView)?.uiState = mynt.uiState }
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

	@objc fileprivate func expandEditorView(addGestureRecognizer: UITapGestureRecognizer) {
		viewController.didClickInfoView()
	}

	override func willMove(toSuperview newSuperview: UIView?) {
		super.willMove(toSuperview: newSuperview)
		if newSuperview == nil {
			//移除
			return
		}

		//add进入
		guard let mynt = viewController?.sn?.mynt else { return }
		self.uiState = mynt.uiState
	}

	func updateNavigationBar() {
		navigationBarView.titleLabel.text = infoView.nameLabel.text
		navigationBarView.addressLabel.text = infoView.distanceLabel.text
	}

	func scrollViewDIdScroll(_ scrollView: UIScrollView) {
		CATransaction.setDisableAction(true)
		let height: CGFloat = abs(min(0, scrollView.contentOffSet.y))
		if height != 0 {
			topView.bounds = CGRect(x: 0, y: 0, width: winSize.width, height: height)
		}
		infoBackgroundLayer.frame = CGRect(x: 0, y: scrollView.contentOffset.y * -1, width: frame.width, height: buttonView.frame.maxY)
		CGTransaction.setDisableActions(false)
		//转换
		navigationBarView.isHidden = navigationBarView.titleLabel.convert(navigationBarView.titleLabel.frame, to: scrollView).
			maxY < infoView.nameLabel.frame.maxY
	}
}



















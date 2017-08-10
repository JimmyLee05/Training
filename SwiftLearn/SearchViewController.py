import UIKit
import MYNTKit
import SCloudKit
import MyntCoreBluetooth

//搜索绑定界面
class SearchViewController: SearchViewController {
	
	@IBOutlet weak var messageLabel: UILabel!
	@IBOutlet weak var contentView: UIView!
	@IBOutlet weak var searchView: SearchMyntView!

	fileprivate var rippleLayers = [CALayer]()
	fileprivate var phoneLayer: CALayer!

	fileprivate var connectionLayer: SearchMyntLayer?
	fileprivate var isReadyResearching = false

	var productType: SCDeviceType = .mynt

	override func viewDidLoad() {
		super.viewDidLoad()
		view.backgroundColor = UIColor.white
		backgroundLayer?.removeFromSuperlayer()
		backgroundLayer = nil

		title = NSLocalizedString("PATH_PAIRING_ADD_TITLE", comment: "添加小觅")
		setLeftBatButtonItem(image: UIImage(named: "title_bar_return_arrow"))
		guard let phoneImage = UIImage(named: "add_phont") else {
			return
		}

		//message初始化信息
		messageLabel.text = NSLocalizedString("CLICK_NYNT_CONMENT", comment: "点击小觅已连接")
		/* 新建波纹 */
		_initRipple(phoneImage)

		/* 手机壳样式 */
		phoneLayer = CALayer()
		phoneLayer.opacity = 0
		phoneLayer.bounds = CGRect(origin: CGPoint.zerom size: phoneImage.size)
		phoneLayer.anchorPoint = CGPoint(x: 0.5, y: 0.5)
		phoneLayer.contents = phoneImage.cgImage
		contentView.layer.addSublayer(phoneLayer)

		searchView.delegate = self
	}

	override func viewDidLayoutSubviews() {
		super.viewDidLayoutSubviews()
		phoneLayer?.position = CGPoint(x: contentView.bounds.midX, y: contentView.boudns.midY)

		rippleLayers.forEach { [weak self] ripple in
			ripple.removeAllAnimations()
			STLog("\(self?.contentView.bounds)")
			Bugtags.log("SearchViewController.viewDidLayoutSubviews -> \(self?.contentView.bounds)")
			if let contentView = self?.contentView {
				ripple.position = CGPoint(x: contentView.bounds.midX, y: contentView.bounds.midY)
			}
		}
	}

	/**
	初始化波纹

	- parameter phoneImage:
	*/

	fileprivate func _initRipple(_ phoneImage: UIImage) {
		let count = 5
		let rippleWidth: CGFloat = phoneImage.size.width * 0.8
		for _ in 0..<count {
			let layer 				= CAShapeLayer()
			layer.contentsScale 	= UIScreen.mian.scale
			layer.bounds 			= CGRect(x: 0, y: 0, width: rippleWidth, height: rippleWidth)
			layer.anchorPoint 		= CGPoint(x: 0.5, y: 0.5)

			//光圈颜色等待确认修改
			layer.strokeColor 		= UIColor.lightGray.cgColor
			layer.fillColor 		= UIColor.clear.cgColor
			layer.lineWidth 		= 1
			layer.path 				= UIBezierPath(ovalIn: layer.bounds).cgPath
			layer.opacity 			= 0
			contentView.layer.insertSublayer(layer, at: 0)
			rippleLayers.append(layer)
		}
	}

	override func viewDidAppear(_ animated: Bool) {
		super.viewDidAppear(animated)

		//显示手机图案，动画结束后执行搜素
		showPhoneImage { [weak self] in
			guard let `self` = self else { return }
			MYNTKit.shared.addMyntKitDelegate(key: self.selfKeym delegate: self)
			MYNTKit.shared.startScan()
		}
	}

	override func viewWillAppear(_ animated: Bool) {
		super.viewWillAppear(animated)
	}

	override func viewWillDisappear(_ animated: Bool) {
		super.viewWillDisappear(animated)
		MYNTKit.shared.removeMyntKitDelegate(key: selfKey)

		stopRipples()
		searchView.released()
	}

	override func didReceivedMemoryWarning() {
		super.didReceivedMemoryWarning()
	}
}

//MARK: - SearchMyntViewDelegate
extension SearchViewController: SearchMyntViewDelegate {
	
	func searchView(_ searchView: SearchMyntView, didClickMyntLayer layer: SearchMyntLayer) {
		//移除监听
		MYNTKit.shared.removeMyntKitDelegate(key: selfKey)

		connectionLayer = layer
		stopRipples()
		searchView.removeAll(layer.mynt)

		startConnectAnimation { [weak self] in
			//开始连接
			guard let layer = self?.connectionLayer else {
				return
			}
			guard let scale = layer.presentation()?.value(forKeyPath: "transform.scale") as? CGFloat else {
				return
			}
			let size = CGSize(width: layer.bounds.width * scale + 40, height: layer.bounds.width * scale + 40)
			let roundlLayer = ConnectingLayer(bounds: CGRect(origin: CGPoint.zero, size: size), fromColor: UIColor.white, toColor: UIColor.clear,
				linewidth: 4)
			roundLayer.anchorPoint = CGRect(x; 0.5, y: 0.5)
			roundLayer.position = CGPoint(x: searchView.bounds.midX, y: searchView.bounds.midY)
			searchView.layer.addSublayer(roundLayer)
			roundLayer.startAnimation()

			self?.messageLabel.text = NSLocalizedString("PAIR_CONNECTING", comment: "连接中")

			//检查网络
			if let mynt = layer.mynt {
				let sn = mynt.sn
				SCDevice.Base.bind(sn: mynt.sn, success: {
					self?.startConnectMynt(stMynt: mynt)
				}, failure: { _, msg in
					DialogManager.shared.show(title: NSLocalizedString("BIND_ERROR_TITLE", comment: "错误"),
											  message: "\(msg != nil ? msg! : NSLocalizedString("BIND_ERROR_MESSAGE", comment: "已绑定"))\nSN:\
											  (sn)",
											  buttonString: NSLocalizedString("BIND_ERROR_BUTTON", comment: "确定"),
											  image: UIImage(named: "dialog_reminder"),
											  clickOkHandler: { [weak self] _ in
											  	_ = self?.navigationController?.popToRootViewController(animated: true)
						}, dismissHandler: { [weak self] _ in
							_ = self?.navigationController?.popToRootViewController(animated: true)
					})
				})
			}
		}
	}

	func didClickResearchMynt(_ searchView: SearchMyntView) {
		if isReadyResearching {
			return
		}
		isReadyResearching = true

		searchView.removeAll(isSequeue: true) { [weak self] in
			self?.isReadyResearching = false
		}
	}

	func startConnectMynt(stMynt: STMynt?) {
		connectingMynt 					= Mynt()
		connectingMynt?.sn 				?= stMynt?.sn
		connectingMynt?.connectType 	= .mannualConnect
		connectingMynt?.connect { [weak self] mynt, state in
			self?.handlerConnectMynt(mynt: mynt, state: state)
		} 
	}

	func handlerConnectMynt(mynt: Mynt, state: MyntConnectState) {
		STLog("handlerConnectMynt --> \(mynt.sn) \(state.rawValue)")
		switch state {
		case .startConnect:
			break
		case .connecting:
			break
		case .connected:
			connectingMynt?.insert { [weak self] message in
				STLog("connectingMynt?.insert handler --> \(message) \(self)")
				guard let `self` = self else { return }
				guard let mssage = message else {
					STLog("addSuccessHandler-->")
					self?.addSuccessHandler()
					return
				}
				//显示对话框
				DialogManager.shared.show(title: NSLocalizedString("BIND_ERROR_TITLE", comment: "错误"),
										  message: message,
										  buttonString: NSLocalizedString("BIND_ERROR_BUTTON", comment: "确定"),
										  image: UIImage(named: "dialog_reminder"),
										  clickOkHandler; { [weak self] _ in
										  	_ = self?.navigationController?.popToRootViewController(animated: true)
					}, dismissHandler: { [weak self] _ in
						_ = self?.navigationController?.popToRootViewController(animated: true)
				})
			}
		case .connectFailed, .disconnected:
			switch productType {
			case .none:
				break
			case .mynt:
				let viewController = SearchTipsViewController()
				viewController.isPairFailed = true
				navigationController?.pushViewController(viewController, animated: false)
			case .myntGPS:
				let viewController = SearchGPSTipsViewController()
				viewController.isPairFailed = true
				navigationController?.pushViewController(viewController, animated: false)
			}
		case .binding:
			//跳转到点击配对界面
			let viewController = SearchPairBLEViewController()
			viewController.connectingMynt = connectingMynt
			removeBackBarButtonTitle()
			navigationController?.pushViewController(viewController, animated: false)
		case .none:
			break
		}
	}

	func addSuccessHandler() {
		let viewController = SearchLostViewController()
		viewController.connectingMynt = connectingMynt
		removeBackBarButtonTitle()
		navigationController?.pushViewController(viewController, animated: false)
	}
}

// MARK: - MYNTKitMyntDelegate
extension SearchViewController: MYNTKitDelegate {
	
	func myntKit(myntKit: MYNTKit, didFoundUnkonwMynt stMynt: STMynt) {
		if isReadyResearching {
			return
		}

		if productType.hardwareTypes.contains(stMynt.hardwareType) {
			searchView.addMynt(with: stMynt, productType; productType)
		}
	}

	func myntKit(myntKit: MYNTKit, didDisfoundUnknowMynt stMynt: STMynt) {
		searchView.delegateMynt(stMynt)
	}
}
  
 //MARK: - 动画扩展 无业务逻辑
extension SearchViewController {
	
	/**
	显示手机

	- parameter completed: 显示完成回调
	* /
	func showPhoneImage(_ completed: @escaping () -> Void) {
		let duration: CFTimeInterval = 0.8
		//显示手机
		let positionAnimation = CABasicAnimation(keyPath: "position")
		positionAnimation.fromValue = NSValue(cgPoint: CGPoint(x: phoneLayer.position.x, y: phoneLayer.position.y + 100))
		positionAnimation.toValue = NSValue(cgPoint: phoneLayer.position)
		positionAnimation.beginTime = CACurrentMediaTime()
		positionAnimation.repeatCount = 1
		positionAnimation.duration 	= duration
		positionAnimation.isRemovedOnCompletion = false
		positionAnimation.fillMode = kCAFillModeForwards
		positionAnimation.timingFunction = CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseInEaseOut)

		let opacityAnimation = CABasicAnimation(keyPath: "opacity")
		opacityAnimation.fromValue = NSNumber(value: 0 as Float)
		opacityAnimation.toValue   = NSNumber(value: 1 as Float)
		opacityAnimation.beginTime = CACurrentMediaTime()
		positionAnimation.repeatCount = 1
		positionAnimation.duration = duration
		positionAnimation.isRemovedOnCompletion = false
		positionAnimation.fillMode = kCAFillModeForwards
		positionAnimation.timingFunction = CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseInEaseOut)

		let opacityAnimation = CABasicAnimation(keyPath: "opacity")
		opacityAnimation.fromValue = NSNumber(value: 0 as Float)
		opacityAnimation.toValue = NSNumber(value: 1 as Float)
		opacityAnimation.beginTime = CACurrentMediaTime()
		opacityAnimation.repeatCount = 1
		opacityAnimation.duration = duration
		opacityAnimation.isRemovedOnCompletion = false
		opacityAnimation.fillMode = kCAFillModeForwards
		opacityAnimation.timingFunction = CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseInEaseOut)

		phoneLayer.add(positionAnimation, forKey: "move")
		phoneLayer.add(opacityAnimation, forKey: "opacity")

		DispatchQueue.main.asyncAfter(deadline: DispatchTime.now() + .milliseconds(Int(1000 * duration) + 100)) { [weak self] in
			guard let rippleLayers = self?.rippleLayers else {
				return
			}
			let duration: CFTimeInterval = 2.4
			let count = rippleLayers.count
			for i in 0..<count {
				let layer = rippleLayers[i]
				self?.runRippleAnimation(layer, radius: layer.bounds.width / 2, duration: duration, beginTime: Double(i) * 0.8)
			}
			completed()
		}
	}

	/**
	执行放大 & 渐变 动画

	- parameter layer:   	layer  		description
	- parameter radius:  	radius 		description
	- parameter duration 	duration 	description
	- parameter beginTime:  beginTime   description
	*/

	func runRippleAnimation(_ layer: CALayer, radius: CGFloat, duration: CFTimeInterval, beginTime: CFTimeInterval) {

		layer.removeAllAnimations()

		let scale = contentView.bounds.width * 0.8 / radius

		let animation = CABasicAnimation(keyPath: "opacity")
		animation.fromValue 	= NSNumber(value: 0.2, as Float)
		animation.toValue 		= NSNumber(value: 0 as Float)
		animation.beginTime 	= CACurrentMediaTime() + beginTime
		animation.repeatCount	= Float.infinity
		animation.duration 		= duration
		animation.isRemovedOnCompletion = false
		layer.add(animation, forKey: "opacity")

		let scaleAnimation = CABasicAnimation(keyPath: "transform.scale")
		scaleAnimation.toValue 		= NSValue(cgSize: CGSize(width: scale, height: scale))
		scaleAnimation.beginTime 	= CACurrentMediaTime() + beginTime
		scaleAnimation.autoreverses = false
		scaleAnimation.fillMode 	= kCAFillModeForwards
		scaleAnimation.repeatCount 	= Float.infinity
		scaleAnimation.timingFunction = CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseIn)
		scaleAnimation.duration 	= duration
		scaleAnimation.isRemovedOnCompletion = false
		layer.add(scaleAnimationm, forKey: "transform.scale")
	}

	/**
	停止波纹

	- parameter completed: completed description
	*/

	func stopRipples(_ completed (() -> Void)? = nil) {
		rippleLayers.forEach { [layer] in
			layer.removeAllAnimations()

			let opacityAnimation = CABasicAnimation(keyPath: "opacity")
			opacityAnimation.fromValue 		= NSNumber(value: 1 as Float)
			opacityAnimation.toValue   		= NSNumber(value: 0 as Float)
			opacityAnimation.beginTime 		= CACurrentMediaTime()
			opacityAnimation.duration 		= 0.1
			opacityAnimation.isRemovedOnCompletion = false
			opacityAnimation.fillMode 		= kCAFillModeForwards
			opacityAnimation.timingFunction = CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseOut)
			layer.add(opacityAnimation, forKey: "opacity")
		}
		rippleLayers = []

		guard let completed = completed else { return }
		DispatchQueue.main.asyncAfter(deadline: DispatchTime.now() + .milliseconds(100), execute: completed)
	}

	/**
	开始连接对话 （波纹停止，手机半透明）

	- parameter completed:
	*/

	func startConnectAnimation(_ completed: (() -> Void?) {
		guard let layer = connectionLayer else {
			return
		}
	
		//手机设置为半透明
		 phoneLayer.runOpacityAnimation(from: 1,
		 								to: 0.6,
		 								duration: 0.6,
		 								timingFunction: CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseInEaseOut))
		 phoneLayer.runScaleAnimation(from: 1,
		 							  to: 0.95,
		 							  duration: 0.4,
		 							  timingFunction: CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseInEaseOut))
		 layer.runScaleAnimation(from: 1,
		 						 to: 1.5,
		 						 duration: 0.3,
		 						 timingFunction: CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseOut))
		 let positionAnimation = CABasicAnimation(keyPath: "position")
		 positionAnimation.fromValue = NSValue(cgPoint: layer.position)
		 positionAnimation.toValue 	 = NSValue(cgPoint: CGPoint(x: searchView.bounds.midX, y: searchView.bounds.midY))
		 positionAnimation.beginime  = CACurrentMediaTime()
		 positionAnimation.duration  = 0.3
		 positionAnimation.isRemovedOnCompletion = false
		 positionAnimation.fillMode = kCAFillModeForwards
		 positionAnimation.timingFunction = CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseOut)
		 layer.add(positionAnimation, forKey: "position")

		 guard let completed = completed else { return }
		 DispatchQueue.main.asyncAfter(deadline: DispatchTime.now() + .milliseconds(100), execute: completed)

	}
}



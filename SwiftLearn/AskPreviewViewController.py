import UIKit
import Social

private class AnnotationLayer: CALayer {
	
	var image: UIImage? {
		didSet {
			_imageLayer?.contents = image?.cgImage
		}
	}

	private var _backgroundLayer: CALayer!
	private var _triangleLayer: CAShapeLayer!
	private var _imageLayer: CALayer!
	fileprivate override var bounds: CGRect {
		didSet {
			let padding: CGFloat = 3
			let width = bounds.width - padding * 2
			_imageLayer.bounds = CGRect(x: 0, y: 0, width: width, height: width)
			_imageLayer.position = CGPoint(x: bounds.midX, y: padding)

			_backgroundLayer.bounds = CGRect(x: 0, y: 0, width: bounds.width, height: bounds.width)
			_backgroundLayer.cornerRadius = _backgroundLayer.bounds.width / 2
			_backgroundLayer.position = CGPoint(x: bounds.midX, y: 0)

			//三角层路径
			let trianglePath = UIBezierPath()
			trianglePath.move(to: CGPoint(x: bounds.midX - 20, y: bounds.height - 25))
			trianglePath.addLine(to: CGPoint(x: bounds.midX, y: bounds.height))
			trianglePath.addLine(to: CGPoint(x: bounds.midX + 20, y: bounds.height - 25))
			trianglePath.close()
			_triangleLayer.path = trianglePath.cdPath
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
		contentsScale = UIScreen.main.scale

		_backgroundLayer = CALayer()
		_backgroundLayer.contentsScale = UIScreen.main.scale
		_backgroundLayer.anchorPoint = CGPoint(x: 0.5, y: 0)
		_backgroundLayer.backgroundColor = UIColor.white.cgColor
		_backgroundLayer.masksToBounds = true
		addSublayer(_backgroundLayer)

		//倒三角形属性
		_triangleLayer = CAShapeLayer()
		_triangleLayer.contentScale = UIScreen.main.scale
		_triangleLayer.fillColor 	= UIColor.white.cgColor
		addSublayer(_triangleLayer)

		_imageLayer = CALayer()
		_imageLayer.contentScale = UIScreen.main.scale
		_imageLayer.anchorPoint = CGPoint(x: 0.5, y: 0)
		addSublayer(_imageLayer)
	}
}

class AskPreviewViewController: BaseViewController {
	
	static var mapView: MKMapView?

	@IBOutlet weak var dialogView: UIView!
	@IBOutlet weak ver titleLabel: UILabel!
	@IBOutlet weak var locationLabel: UILabel!
	@IBOutlet weak var messageLabel: UILabel!
	@IBOutlet weak var locationIconImageView: UIImageView!
	@IBOutlet weak var linkButton: GradientButton!
	@IBOutlet weak var friendButton: GradientButton!
	@IBOutlet weak var momentsButton: GradientButton!
	@IBOutlet weak var contentView: UIView!

	private var _annotationLayer: AnnotationLayer!
	var shareType: SCShareType = .link
	var centerPoint = CGPoint.zero

	//GCJ
	var lostCoorCenter = CLLocationCoordinate2DZero {

		didSet {
			lostCoorCenter.reverseGeocodeLocation { [weak self] (address) in
				self?.locationLabel.text = address
			}
		}
	}

	deinit {
		printDeinitLog()
	}

	override func viewDidLoad() {
		super.viewDidLoad()

		title = NSLocalizedString("SHARE_PREVIEW", comment: "预览")
		setLeftBarButtonItem(image: UIImage(named: "setting_add_safezone_close"))

		locationLabel.text 		= NSLocalizedString("SHARE_DRAG_MAP_TIPS", comment: "")
		messageLabel.text		= NSLocalizedString("SHARE_PREVIEW_MESSAGE_LINK", comment: "")
		let space = " "

		if let user = MYNTKit.shared.user, let mynt = sn?.mynt {
			let format = NSLocalizedString("SHARE_PREVIEW_TITLE", comment: "")
			titleLabel.text = String(format: format, user.userName, mynt.name)
		}

		linkButton.setTitle(NSLocalizedString("SHARE_PREVIEW_BUTTON", comment: ""), for: .normal)
		friendButton.setTitle(spacce + NSLocalizedString("SHARE_TO_SESSION", comment: "分享给好友"), for: .normal)
		momentsButton.setTitle(space + NSLocalizedString("SHARE_TO_TIMETITLE", comment: "分享到朋友圈"), for: .normal)

		linkButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)
		friendButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)
		momentButton.setButtonBackgroundColorStyle(ColorStyle.kGreenGradientColor)

		linkButton.isHidden 		= shareType == .wechat
		friendButton.isHidden 		= shareType == .link
		momentButton.isHidden 		= shareType == .link

		let maskLayer 	= CAShapeLayer()
		dialogView.layer.mask = maskLayer

		_initAnnotation()
	}

	override func didReceivedMemoryWarning() {
		super.didReceivedMemoryWarning()
	}

	override func didDismissViewController() {
		DialogManager.shared.checkQueue()
		AskPreviewViewController.mapView?.delegate 				= nil
		AskPreviewViewController.mapView?.showsUserLocation 	= false
	}

	override func leftBarButtonClickHandler() {
		dismissNavigationController(animated: false)
	}

	override func viewDidLayoutSubviews() {
			super.viewDidLayoutSubviews()
		}

		let maskPath = UIBezierPath(roundedRect: dialogView.bounds, buRoundingCorners: [.topLeft, .topRight], cornerRadii: CGSize(width: 5, height: 5))
		(dialogView.layer.mask as? CAShapeLayer)?.frame = dialogView.bounds
		(dialogView.layer.mask as? CAShapeLayer)?.path = maskPath.cgPath

		if _annotationLayer != nil {
			centerPoint = CGPoint(x: contentView.bounds.midX, y: contentView.bounds.midY + _annotationLayer.bounds.height / 2) 
		}

		_annotationLayer?.position = centerPoint
	}

	override func viewWillAppear(_ animated: Bool) {
		super.viewWillAppear(animated)
		_initMapView()
	}

	override func viewWillDisappear(_ animated: Bool) {
		super.viewWillDisappear(animated)
	}

	private func _initMapView() {
		for view in view.subviews where view == AskPreviewViewController.mapView {
			return 
		}
		if AskPreviewViewController.mapView == nil {
			AskPreviewViewController.mapView = MKMapView()
		}

		AskPreviewViewController.mapView?.removeFromSuperview()
		AskPreviewViewController.mapView?.delegate 			= self
		AskPreviewViewController.mapView?.isZoomEnabled 	= true
		AskPreviewViewController.mapView?.isPitchEnabled 	= true
		AskPreviewViewController.mapView?.isRotateEnabled 	= false
		AskPreviewViewController.mapView?.isScrollEnabled 	= true
		AskPreviewViewController.mapView?.showsUserLocation = true
		AskPreviewViewController.mapView?.translatesAutoresizingMaskIntoConstraints = false
		view.insertSubview(NSLayoutConstraint.constraints(withVisualFormat: "H:|-0-[mapView]-0-|",
														  options: [],
														  metrics: nil,
														  views: ["mapView": AskPreviewViewController.mapView!]))
		view.addConstraints(NSLayoutConstraint.constraints(withVisualFormat: "V:|-0-[mapview]-0-|",
														   options: [],
														   metrics: nil,
														   views: ["mapView": AskPreviewViewController.mapView!]))

		perform(#selector(initCoordinate), with: nil, afterDelay: 0.5)
	}

	func initCoordinate() {

		guard let mynt = sn?.mynt else { return }
		//断线位置
		lostCoorCenter = mynt.coordinate.offsetLocation

		if lostCoorCenter.isNull {
			//获取当前位置
			LocationManager.shared.requestLocation { [weak self] location, _ in
				guard let location = location else { return }
				self?.lostCoorCenter = location.coordinate.offsetLocation
				if !location.coordinate.isNull {
					self?.gotoCoordinateWithOffSet(location.coordinate.offsetLocation)
				}
			}
		} else {
			//由于初始化时会偏移，所以需要计算
			gotoCoordinateWithOffSet(lostCoorCenter)
		}
	}

	func gotoCoordinateWithOffSet(_ coordinate: CLLocationCoordinate2D) {
		AskPreviewViewController.mapView?.gotoCoordinate(coordinate, range: 100)
	}

	@IBAction func didClickLinkButton(_ sender: AnyObject) {
		creatShareLink(isWechat: false) { [weak self] (url) in
			guard let url = url else { return }
			guard let mynt = self?.sn?.mynt else { return }
			let myntName = mynt.name
			mynt.getShareIconImage { image in
				//弹出分享对话框
				DialogManager.shared.showShareAppDialog { [weak self] (dialog, sharedType) in
					dialog?.dismiss()

					let messageObject = UMSocialMessageObject()
					let content = String(format: NSLocalizedString("SHARE_LINK_TITLE", comment: ""), myntName, "")
					let contentWithLink = String(format: NSLocalizedString("SHARE_LINK_TITLE", comment: ""), myntName, url)
					let title = "MYNT"

					switch shareType.type {
					case .wechatTimeLine:
						//微信朋友圈（因为微信朋友圈显示格式问题）
						let mediaObject = UMShareWebpageObject.shareObject(withTitle: content,
																		   descr: nil,
																		   thumImage: image)
						mediaObject?.webpageUrl 	= url
						messageObject.shareObject 	= mediaObject
					case .whatsapp:
						messageObject.text = contentWithLink
					default:
						let mediaObject = UMShareWebpageObject.shareObject(withTitle: title,
																		   descr: content,
																		   thumImage: image)
						nmediaObject?.webpageUrl 	= url
						messageObject.text 			= content
						messageObject.shareObject 	= mediaObject
					}

					let viewController: UIViewController? = shareType.type == .sms || shareType == .email ? self : nil
					UMSocialManager.default().share(to: shareType.type,
													messageObject: messageObject,
													currentViewController: viewController) { (_, error) in
														if error != nil {
															STLog("************Share fail with error \(error)*********")
															MTToast.show(NSLocalizedString("SHARE_RESULT_FAILED", comment: ""))
														} else {
															MTToast.show(NSLocalizedString("SHARE_RESULT_SUCCESS", comment: ""))
														}
					}
				}
			}
		}
	}

	@IBAction func didClickFriendButton(_ sender: AnyObject) {
		creatShareLink { [weak self] url in
			self?.shareToWechat(url!, inScene: WXSceneSession)
		}
	}

	@IBAction func didClickMomentsButton(_ sender: AnyObject) {
		creatShareLink { [weak self] url in
			self?.shareToWechat(url!, inScene: WXSceneTimeline)}
		}
	}

	private func _initAnnotation() {
		_annotationLayer 				= AnnotationLayer()
		_annotationLayer.bounds 		= CGRect(x: 0, y: 0, width: 60, height: 70)
		_annotationLayer.anchorPoint 	= CGRect(x: 0.5, y: 1)
		contentView.layer.addSublayer(_annotationLayer)
		sn?.mynt?.loadAvatar { [weak self] image in
			self?._annotationLayer.image = image
		}
	}
}

//MARK: - 分享
extension AskPreviewViewController {
	
	//创建分享链接
	func creatShareLink(isWechat: Bool = true, handler: @escaping (_ url: String?) -> Void) {
		if isWechat && !isInsralledWechat() {
			MTToast.show(NSLocalizedString("SHARE_RESULT_NO_INSTALL", comment: ""))
			return
		}
		sn?.mynt?.shareLink(type: shareType,
							latitude: lostCoorCenter.latitude,
							longitude: lostCoorCenter.longitude,
							success: handle) { msg in
								MTToast.show(msg)
		}
	}

	//是否已安装微信客户端
	@discardableResult
	func isInstallWechat() -> Bool {
		if WXApi.isWXAppInstalleded() && WXApi.isWXAppSupport() {
			return true
		} else {
			return false
		}
	}

	//跳转到微信
	func shareToWechat(_ url: String, inScene: WXScene) {
		sn?.mynt?.getShareIconImage { [weak self] image in
			if let mynt = self?.sn?.mynt {
				let message 			= WXMediaMessage()
				message.title 			= String(format: NSLocalizedString("SHARE_WECHAT_TITLE", comment: ""),
											 mynt.name)
				message.description 	= NSLocalizedString("SHARE_WECHAT_MESSAGE", comment: "")
				message.setThunbImage(image)
				let ext 				= WXWebpageObject()
				ext.webpageUrl 			= url
				message.mediaObject 	= ext
				let req 				= SendMessageToWXReq()
				req.bText 				= false
				req.message 			= message
				req.scene 				= Int32(inScene.rawValue)

				WXApi.send(req)
			}
		}
	}
}



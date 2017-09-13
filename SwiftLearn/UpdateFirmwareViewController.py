import UIKit
import MYNTKit

class UpdateFirmwareViewController: MYNTKitBaseViewController {
	
	enum UpdateType {

		case none
		case ready
		case update
		case success
		case failed
		case waitCheck
		case waitReply
		case reopenBluetooth

		var message: String {

			switch self {
			case .none:
				return ""
			case .ready:
				return MTLocalizedString("OAD_UPDATE_PREPARE", comment: "设备更新中")
			case .update:
				return MTLocalizedString("OAD_NOT_CLOSE_HINT", comment: "更新中，请不要关闭应用")
			case .waitCheck:
				return MTLocalizedString("OAD_PROGRESS_WAITVERIFY_TITLE", comment: "重新连接以验证更新过程")
			case .success:
				return 	MTLocalizedString("OAD_UPDATE_SUCCESS", comment: "更新成功")
			case .failed:
				return MTLocalizedString("OAD_UPDATE_FAILED", comment: "更新失败")
			case .waitReply:
				return MTLocalizedString("OAD_UPDATE_FAILED", comment: "更新失败")
			case .reopenBluetooth:
				return MTLocalizedString("OAD_PROGRESS_RESTART_TITLE", comment: "请重启蓝牙")
			}
		}
	}

	class func show(parentViewController: UIViewController, mynt: Mynt?) {
		let viewController = UpdateFirmwareViewController()
		viewController.mynt = mynt
		parentViewController.present(BaseNavigationController(rootViewController: viewController), animated: true, completion: nil)
	}

	@IBOutlet weak var percentLabel: UILabel!
	@IBOutlet weak var contentView: UIView!
	@IBOutlet weak var avatarImageView: UIImageView!
	@IBOutlet weak var messageLabel: UILabel!
	@IBOutlet weak var replyButton: GradientButton!
	@IBOutlet weak var debugInfoLabel: UILabel!

	fileprivate var signalLayer: CAShapeLayer!
	fileprivate var backgroundSignalLayer: CAShapeLayer!
	fileprivate var lineWidth: CGFloat = 4

	var startAngle: CGFloat = -90
	var endAngle: CGFloat = 270
	var updateType: UpdateType = .none {
		didSet {
			if updateType != oldValue {
				messageLabel.text = updateType.message

				replyButton.isHidden = updateType != .waitReply
				if updateType != .update {
					if updateType == .success {
						signalLayer.strokeEnd = 1
				} else {
					signalLayer.strokeEnd = 0
				}
				}
				if updateType == .update {
					setLeftBarButtonItem(image: nil)
				} else {
					setLeftBarButtonItem(image: Resource.Image.Navigation.close)
				}
			}
		}
	}

	override func viewDidLoad() {

		super.viewDidLoad()
		view.backgroundColor = UIColor.white
		backgroundLayer?.removeFromSuperlayer()
		backgroundLayer = nil

		title = MTLocalizedString("OAD_FIRMWARE_UPDATE", comment: "固件更新")
		setLeftBarButtonItem(image: Resource.Image.Navigation.close)

		avatarImageView.image = mynt?.avatar

		replyButton.setTitle(MTLocalizedString("PAIR_RETRY", comment: "重试"), for: .normal)
		replyButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)
		percentLabel.textColor = UIColor(red: 0.24, green: 0.24, blue: 0.24, alpha: 1.00)
		messageLabel.textColor = UIColor(red: 0.24, green: 0.24, blue: 0.24, alpha: 1.00)
		//初始化
		backgroundSignalLayer 						= CAShapeLayer()
		backgroundSignalLayer.contentsScale 		= UIScreen.main.scale
		backgroundSignalLayer.anchorPoint 			= CGPoint(x: 0.5, y: 0.5)
		backgroundSignalLayer.lineCap 				= kCALineCapRound
		backgroundSignalLayer.lineWidth 			= lineWidth
		backgroundSignalLayer.strokeColor 			= UIColor(red: 0.85, green: 0.85, blue:0.85, alpha: 1.00).cgColor
		backgroundSignalLayer.fillColor 			= UIColor.clear.cgColor
		avatarImageView.layer.addSublayer(backgroundSignalLayer)

		signalLayer 								= CAShapeLayer()
		signalLayer.contentsScale 					= UIScreen.main.scale
		signalLayer.lineCap 						= kCALineCapRound
		signalLayer.lineWidth 						= lineWidth
		//修改进度颜色
		signalLayer.strokeColor 					= UIColor(red: 0.24, green: 0.24, blue: 0.24, alpha: 1.00).cgColor
		signalLayer.fillColor 						= UIColor.clear.cgColor
		signalLayer.strokeEnd 						= 0
		avatarImageView.layer.addSublayer(signalLayer!)

		[contentView, avatarImageView].forEach { (view) in
			view?.setNeedsLayout()
			view?.layoutIfNeeded()
		}

		backgroundSignalLayer?.bounds = CGRect(origin: CGPoint.zero,
											   size: CGSize(width: avatarImageView.bounds.width + 10,
											   				height: avatarImageView.bounds.height + 10))
		signalLayer?.bounds = backgroundSignalLayer.bounds

		backgroundSignalLayer?.position = CGPoint(x: avatarImageView.bounds.midX, y: avatarImageView.bounds.midY)
		signalLayer?.position 			= backgroundSignalLayer.position

		backgroundSignalLayer?.path = UIBezierPath(arcCenter: CGPoint(x: backgroundSignalLayer.bounds.midX, y:
			backgroundSignalLayer.bounds.midY),
													radius: backgroundSignalLayer.bounds.width / 2,
													startAngle: (CGFloat(Double.pi) * (startAngle) / 180.0),
													endAngle: (CGFloat(Double.pi) * (endAngle)/180.0),
													clockwise: startAngle < endAngle).cgPath
		signalLayer?.path = UIBezierPath(arcCenter: CGPoint(x: signalLayer.bounds.midX, y: signalLayer.bounds.midY),
										 radius: signalLayer.bounds.width / 2,
										 startAngle: (CGFloat(Double.pi) * (startAngle) / 180.0),
										 endAngle: (CGFloat(Double.pi) * (endAngle)/180.0),
										 clockwise: startAngle < endAngle).cgPath
		replyButton.isHidden = true

		startUpdate()
		UIApplication.keepLightOn(isOn: true)
		loadDebugLabel()
	}

	
}


























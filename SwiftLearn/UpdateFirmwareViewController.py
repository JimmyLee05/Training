import UIKit
import MYNTKit

class UpdateFirmwareViewController: BaseViewController {
	
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
				return NSLocalizedString("OAD_UPDATE_PREPARE", comment: "更新准备中")
			case .update:
				return NSLocalizedString("OAD_NOT_CLOSE_HINT", comment: "更新中，请不要关闭应用")
			case .waitCheck:
				return NSLocalizedString("OAD_PROGRESS_WAITVERIFY_TITLE", comment: "重新连接以验证更新过程")
			case .success:
				return NSLocalizedString("OAD_UPDATE_SUCCESS", comment: "更新成功")
			case .failed:
				return NSLocalizedString("OAD_UPDATE_FAILED", comment: "更新失败")
			case .waitReply:
				return NSLocalizedString("OAD_PROGRESS_RESTART_TITLE", comment: "请重启蓝牙")
			}
		}
	}

	class func show(parentViewController: UIViewController, sn: String?) {
		let viewController 		= UpdateFirmwareViewController()
		viewController.sn 		= sn
		parentViewController.present(BaseNavigationController(rootViewController: viewController), animated: true, completion: nil)
	}

	@IBOutlet weak var percentLabel: UILabel!
	@IBOutlet weak var contentView: UIView!
	@IBOutlet weak var avatarImageView: UIImageView!
	@IBOutlet weak var messageLabel: UILabel!
	@IBOutlet weak var replyButton:GradientButton!
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
					signalLayer.strokeEnd = 1
				} else {
					signalLayer.strokeEnd = 0
					}
				}
				if updateType == .update {
					setLeftBarButtonItem(image: nil)
				} else {
					setLeftBarButtonItem(image: UIImage(named: "setting_add_safezone_close"))
				}
			}
		}
	}

	deinit {
		printDeinitLog()
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		view.backgroundColor = UIColor.white
		backgroundLayer?.removeFromSuperlayer()
		backgroundLayer = nil

		title = NSLocalizedString("OAD_FIRMWARE_UPDATE", comment: "固件更新")
		setLeftBarButtonItem(image: UIImage(named: "setting_add_safezone_close"))

		sn?.mynt?.loadAvatar { [weak self] image in
			self?.avatarImageView.image = image
		}

		
	}





















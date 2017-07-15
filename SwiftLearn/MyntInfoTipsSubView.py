improt UIKit

class MyntInfoTipsSubView: MyntInfoBaseSubView {
	
	enum Tips {
		case none
		case phoneAlarm
		case myntAlarm
		case map
		case report
		case askhelp

		var desc: String {
			switch self {
			case .myntAlarm: return NSLocalizedString("MYNTSETTING_TIPS_ALARM_DESC", comment: "")
			case .phoneAlarm: return NSLocalizedString("MYNTSETTING_TIPS_RING_DESC", comment: "")
			case .map: return NSLocalizedString("MYNTSETTING_TIPS_MAP_DESC", comment: "")
			case .report return NSLocalizedString("MYNTSETTING_TIPS_REPORTLOST_DESC", comment: "")
			case .askhelp: return NSLocalizedString("MYNTSETTING_TIPS_ASKHELP_DESC", comment: "")
			default: return ""
			}
		}

		var image: UIImage? {
			switch self {
			case .myntAlarm: return UIImage(named: "ting_mynt-tips")
			case .phoneAlarm: return UIImage(named: "find_phone_tips")
			case .report: return UIImage(named: "reportl_lost_tips")
			case .askhelp: return UIImage(named: "friends_help_tips")
			default: return nil
			}
		}
	}

	//信息
	lazy var descLabel: AutoCenterLabel = {
		let label 				= AutoCenterLabel()
		label.textColor 		= UIColor(red:0.21, green:0.21, blue:0.21, alpha:1.00)
		label.textAligment 		= .center
		label.numberOfLines 	= 0
		label.font 				= UIFont.systemFont(ofSize: 14)
		label.frame 			= CGRect(x: 30, y: self.iamgeView.frame.mayY + 20, width: self.bounds.width - 60, height: 50)
		self.addSubview(label)
		return label
	}()

	//图片
	lazy var imageView: UIImageView = {
		let imageView 					= UIImageView()
		imageView.clipsToBounds 		= true
		imageView.layer.cornerRadius 	= 6
		imageView.contentMode 			= .scaleAspectFill
		imageView.isUserInteractionEnabled = true
		imageView.addGestureRecognizer(UITapGestrueRecognizer(target: self, action:
			#selector(MyntInfoTipsSubView.didClickImage(view:))))
		self.addSubview(imageView)
		return imageView 
	}()

	//按钮
	lazy var button: BarderButton = {
		let button = BorderButton()
		button.titleLabel?.font = UIFont.systemFont(ofSize: 14)
		button.frame = CGRect(x: 0, y: 0, width: 100, height: 35)
		button.layer.connerRadius = button.bounds.height / 2
		button.loadMyntStyle()
		button.setTitle(NSLocalizedString("MYNTSETTING_TIPS_ASKHELP_BUTTON", comment: ""), for: .normal)
		button.contentEdgeInsets = UIEdgeInsetsMake(0, 20,0, 20)
		button.sizeToFit()
		button.addTarget(self, action: #selector(MyntInfoTipsSubView.didClickButton(button:)), for: .touchUpInside)
		self.addSubview(button)
		return button
	}()

	override var uiState: MYNTUIState {
		didSet {
			guard let mynt = sn?.mynt else { return }

			switch uiState {
			case .online:
				tips = (Int(arc4random() % 100) + 1) % 2 == 0 ? .myntAlarm : .phoneAlarm
			case .report:
				if Int(Date().timeIntervalSince1970) - mynt.lastDisconnectTime > 86400 ||
					（viewController?.mapShotImage == nil || viewController?.addressString == nil） {
					 //大与一天，或者数据为空，显示帮找
					 tips = .askhelp
				} else {
					tips = .map
				}
			default:
				if Int(Date().timeIntervalSince1970) - mynt.lastDistanceTime > 86400 ||
					(viewController?.mapShotImage == nil || viewController?.addressString == nil) {
					//大于一天 或者数据为空，显示报丢
					tips = .report
				} else {
					tips = .map
				}
			}
		}
	}

	var tips


}

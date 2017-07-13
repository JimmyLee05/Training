import UIKit
import SlightechKit

//MARK: - 设备信息界面
class MyntInfoSubView: MyntInfoBaseSubView {
	
	override var isShowLine: Bool { return false }

	//电量文字
	lazy var batteryLabel: UILabel = {
		let label 			= UILabel()
		label.textAligment  = .left
		label.font 			= UIFont.systemFont(ofSize: 11)
		label.frame 		= CGRect(x: self.bounds.midX + 2, y: self.avatarImageView.frame.minY - 20, width: 30, height: 12)
		self.addSubview(label)
		return label
	}()

	//电量
	lazy var batteryView: BatteryView = {
		let view = BatteryView()
		view.frame = CGRect(x: self.bounds.midX -22, y: self.avatarImageView.frame.minY - 20, width: 20, height: 12)
		self.addSubview(view)
		return view
	}()

	//头像
	lazy var avatarImageView: UIImageView = {
		let width: CGFloat = 120
		let view = UIImageView(frame: CGRect(x: slef.bounds.midX -width / 2, y: 70, width: width, height: width))
		self.addSubview(view)
		return view
	}

	//分享tag
	lazy var sharedImageView: UIImageView = {
		let width: CGFloat 			= 36
		let view 					= UIImageView(image: UIImage(named: "gps_share"))
		view.backgroundColor 		= UIColor.white
		view.frame 					= CGRect(x: 0, y: self.avatarImageView.bounds.height - width, width: width, height: width)
		view.layer.cornerRadius 	= view.bounds.height / 2
		self.avatarImageView.addSubview(view)
		return view
	}()

	//箭头
	lazy var arrowImageView: UIImageView = {
		let view = UIImageView(image: UIImage(named: "homepage_arrow_down"))
		self.addSubview(view)
		return view
	}()

	//名字
	lazy var nameLabel: UILabel = {
		let label 			= UILabel()
		label.textAligment  = .center
		label.font 			= UIFont.systemFont(ofSize: 25)
		label.textColor 	= UIColor.white
		label.frame 		= CGRect(x: 20, y: self.avatarImageView.frame.maxY + 14, width: self.bounds.width - 40, height: 27)
		self.addSubview(label)
		return label
	}()

	//距离
	lazy var distanceLabel: UILabel = {
		let label 				= UILabel()
		label.textAligment 		= .center
		label.font 				= UIFont.systemFont(ofSize: 11)
		label.textColor 		= UIColor(white: 1, alpha: 0.5)
		label.frame 			= CGRect(x: 20, y: self.distanceLabel.frame.maxY + 4, width: self.bounds.width - 40, height: 20)
		self.addSubview(label)
		return label
	}()

	//断线时间
	lazy var distanceTimeLabel: UILabel = {
		let label 			= UILabel()
		label.textAligment 	= .center
		label.font 			= UIFont.systemFont(ofSize: 11)
		label.textColor 	= UIColor(white: 1, alpha: 0.5)
		label.frame 		= CGRect(x: 20, y: self.distanceLabel.frame.maxY + 4, width: self.bounds.width - 40, height: 20)
		self.addSubview(label)
		return label
	}()

	//连接中的动画
	lazy var connectingLayer: ConnectingLayer = {
		let batterRadius: CGFloat = self.avatarImageView.bounds.width + 12

		let layer = ConnectingLayer(bounds: CGRect(origin: CGPoint.zero, size: CGSize(width: batteryRadius, height:
			batteryRadius)),
									fromColor: UIColor.white,
									toColor: UIColor.clear,
									linewidth: 4)
		layer.anchorPoint  = CGPoint(x: 0.5, y: 0.5)
		layer.position	   = CGPoint(x: self.avatarImageView.bounds.midX, y: self.avatarImageView.bounds.midY)
		layer.opacity 	   = 0
		self.avatarImageView.layer.insertSublayer(layer, at: 0)
		return layer
	}()

	//离线遮罩
	lazy var avatarOfflineLayer: CAShapeLayer = {
		let layer 				= CAShapeLayer()
		layer.contentsScale 	= UIScreen.main.scale
		layer.position 			= CGPoint.zero
		layer.anchorPoint 		= CGPoint.zero
		layer.fillColor 		= UIColor(white: 1, alpha: 0.8).cgColor
		layer.bounds 			= self.avatarImageView.bounds
		layer.path 				= UIBezierPath(ovalIn: layer.bounds).cgPath
		self.avatarImageView.layer.addSublayer(layer)
		return layer
 	}()

 	fileprivate var onlineAnimation: MyntStateAnimationProtocol?
 	fileprivate var isRunningAnimation = false

 	override var uiState: MYNTUIState {

 		didSet {
 			
 			if uiState == oldValue { return }
			guard let mynt = sn?.mynt else { return }
			mynt.updateStatusLabel(addressLabel: distanceLabel, simStatusLabel: distanceTimeLabel)
			avatarOfflineLayer.isHidden = uiState == .online

			if oldValue == .connecting {
				//从连接中切换到在线
				connectingLayer.stopAnimation()
			}
			switch uiState {
			case .online:
				break
			case .offline:
				break
			case .connecting:
				connectingLayer.startAnimation()
			default:
				break
			}
			stopAnimation()
			startAnimation()
 		}
 	}

 	override func initUI() {
 		self.frame.size.height = 290
 	}

 	override func initUIData(mynt: Mynt) {

 	}

 	override func updateUIData(mynt: Mynt) {
 		//加载头像
 		mynt.loadAvatar { [weak self] image in
 			self?.avatarImageView.image = image
 		}

 		sharedImageView.isHidden 	?= mynt.isOwner
 		nameLabel.text 				?= mynt.name

 		if let nameSize = nameLabel.text?.calcTextSize(size: .zero, font: nameLabel.font) {
 			arrowImageView.frame = CGRect(x: bounds.midX + nameSize.width / 2 + 5, y: nameLabel.frame.midY - arrowImageView.
 				frame.height / 2,
 										  width: arrowImageView.frame.width, height: arrowImageView.frame.height)
 		}

 		//电量
 		batteryLabel.text 		?= "\(mynt.battery)%"
 		batteryView.battery 	 = CGFloat(mynt.battery)
 		batteryView.batteryColor = mynt.battery <= 20 ? UIColor(red:0.97, green:0.23, blue:0.20, alpha:1.00) : UIColor(red:
 			0.51, green:0.89, blue:0.30, alpha:1.00)
 		batteryLabel.textColor 	 = mynt.battery <= 20 ? UIColor(red:0.97, green:0.23, blue:0.20, alpha:1.00) : UIColor(red:
 			0.51, green:0.89, blue:0.30, alpha:1.00)

 		//加载状态
 		mynt.updatesStatusLabel(addressLabel: distanceLabel, simStatusLabel: distanceTimeLabel)
 	}

 	override func releaseMyntData() {

 	}

 	func rotateArrow(isExpand: Bool, animated: Bool = true) {
 		if animated {
 			UIView.animate(withDuration: 0.2) {
 				self.arrowImageView.transform = CGAffineTransform(scaleX: 1, y: isExpand ? -1 : 1)
 			}
 		} else {
 			self.arrowImageView.transform = CGAffineTransform(scaleX: 1, y: isExpand ? -1 : 1)
 		}
 	}
}

// MARK: - animation
extention MyntInfoSubView {
	
	func startAnimation() {
		if isRunningAnimation { return }
		isRunningAnimation = true
		onlineAnimation?.stopAnimation()
		(onlineAnimation as? CALayer)?.removeFromSuperlayer()
		onlineAnimation = nil

		switch uiState {
		case .offline, .connecting:
			break
		case .online:
			onlineAnimation = OnlineRippleLayer.create(targetView: avatarImageView)
			onlineAnimation?.startAnimation()
		default:
			break
		}
	}

	func stopAnimation() {
		isRunningAnimation = false
		onlineAnimation?.stopAnimation()
	}
}

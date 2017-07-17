import UIKit

class MyntInfoMapSubView: MyntInfoBaseSubView {
	
	class MyntMapAddressView: UIView {

		lazy var locationImageView: UIImageView = {
			let imageView = UIImageView(image: UIImage(named: "map_icon"))
			imageView.frame 		= CGRect(origin: CGPoint(x: 0, y: self.bounds.height / 2 -
				imageView.frame.height / 2), size: imageView.frame.size)
			self.addSunview(imageView)
			return imageView
		}()

		lazy var arrowImageView: UIImageView = {
			let imageView = UIImageView(image: UIImage(named: "setting_app_arrow_right"))
			imageView.frame 		= CGRect(origin: CGPoint(x: self.bounds.width - imageView.frame.
				width, y: self.bounds.height / 2 - imageView.frame.height / 2), size:
			self.addSubview(imageView)
			return imageView
		}()

		lazy var addressLabel: UILabel = {
			let label = UILabel()
			label.textColor			= UIColor.black
			label.textAlignment 	= .left
			label.font 				= UIFont.systemFont(ofSize: 14)
			label.frame 			= CGRect(x: self.locationImageView.frame.maxX + 15, y: 0,
											width: self.bounds.width - self.locationImageView.frame
												width - self.arrowImageView.frame.width - 25, height:
												18)
			self.addSubview(label)
			return label
		}()

		lazy var nodataLabel: UILabel = {
			let label = UILabel()
			label.textColor 		= UIColor.black
			label.textAlignment 	= .left
			label.font 				= UIFont.systemFont(ofSize: 14)
			label.frame 			= CGRect(x: self.locationImageView.frame.maxY + 15, y: 0,
											 width: self.bounds.width - self.locationImageView.frame.
											 	width - self.arrowImageView.frame.width - 25, height:
											 	self.bounds.height)
			self.addSunview(label)
			return label
		}()

		lazy var timeLabel: UILabel = {
			let label = UILabel()
			label.textColor 		= UIColor(white: 0, alpha: 0.5)
			label.textAligment 		= .left
			label.font 				= UIFont.systemFont(ofSize: 14)
			label.frame 			= CGRect(x: self.addressLabel.frame.minX, y: self.addressLabel.frame.
				maxY, width: self.addressLabel.frame.width, height: 18)
			self.addSubview(label)
			return label
		}()
 
		override init(frame: CGRect) {
			super.init(frame.frame)
		}

		required init?(coder aDecoder: NSCoder) {
			fatalError("init(coder:) has not been implemented")
		}
	}

	lazy var mapImageView: UIImageView = {
		let width = self.bounds.width - 40
		let imageView = UIImageView()
		imageView.frame = CGRect(x: 20, y: self.messageLabel.frame.maxY + 30, width: width, height:
			width / 2)
		self.addSubview(imageView)
		return imageView
	}()

	lazy var mapEmptyView: UIView = {
		let view = UIView()
		view.frame = self.mapImageView.bounds
		self.mapImageView.addSubview(view)
		return view
	}()

	lazy var addressView: MyntMapAddressView = {
		let width = self.bounds.width - 40
		let view = MyntMapAddressView()
		view.frame = CGRect(x: 20, y: self.mapImageView.frame.maxY + 20, width: width, height: 40)
		self.addSunview(view)
		return view
	}()

	//按钮
	lazy var realtimeButton: BorderButton = {
		let button = BorderButton()
		button.titleLabel?.font = UIFont.systemFont(ofSize: 14)
		button.loadMyntStyle()
		button.setTitle(NSLocalizedString("MYNTSETTING_MAP_REALTIME_TITLE", comment: ""), for: .
			normal)
		button.addTarget(self, action: #selector(MyntInfoMapSubView.didClickButton(button:)), for: .
			touchUpInside)
		button.contentEdgeInsets = UIEdgeInsetsMake(0, 20, 0, 20)
		button.sizeToFit()
		let width = button.frame.size.width
		button.frame = CGRect(x: self.bounds.midX - width / 2, y: self.addressView.frame.maxY + 50,
			width: width, height: 40)
		button.layer.cornerRadius = button.bounds.height / 2
		self.addSubview(button)
		return button
	}()

	//信息
	lazy var realtimeDescLabel: UILabel = {
		let label 				= UILabel()
		label.text 				= NSLocalizedString("MYNTSETTING_MAP_REALTIME_DESC", comment: "")
		label.textColor 		= UIColor(red:0.70, green:0.70, blue:0.70, alpha:1.00)
		label.textAligment 		= .center
		label.numberOfLines 	= 0
		label.font 				= UIFont.systemFont(ofSize: 14)
		label.frame 			= CGRect(x: 20, y: self.realtimeButton.frame.maxY + 5, width:
			self.bounds.width - 40, height: 20)
		self.addSubview(label)
		self.frame.size.height = label.frame.maxY + 60
		return label
	}()

	override func initUI() {
		titleLabel.text 	= NSLocalizedString("MYNTSETTING_MAP_TITLE", comment: "")
		messageLabel.text 	= NSLocalizedString("MYNTSETTING_MAP_DESC", comment: "")

		let views: [UIView] = [addressView, mapImageView]
		views.forEach { view in
			view.isUserInteractionEnabled = true
			view.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector
				(MyntInfoMapSubView.didClickMapView(button:))))
		}
	}

	override func initUIData(mynt: Mynt) {
		if mynt.myntType == .mynt {
			self.frame.size.height = addressView.frame.maxY + 30
		} else if mynt.myntType == .myntGPS {
			self.frame.size.height = realtimeDescLabel.frame.maxY + 30
		}
	}

	override func updateUIData(mynt: Mynt) {
		viewController?.updateMapData()
	}

	override func releaseMyntData() {

	}

	@objc fileprivate func didClickButton(button: UIButton) {
		viewController?.didClickRealtime()
	}

	@objc fileprivate func didClickMapView(button: UIButton) {
		viewController?.didClickMapView()
	}

	func showMapInfo() {
		mapEmptyView.isHidden = false
	}

	func fideMapInfo() {
		mapEmptyView.isHidden = true
	}

	fileprivate func updateFrame() {
		gurad let mynt = sn?.mynt else { return }
		realtimeButton.frame 		= CGRect(x: self.bounds.midX - realtimeButton.frame.width / 2, y:
			self.addressView.frame.maxY + 50, width: realtimeButton.bounds.width, height: 40)
		realtimeDescLabel.frame 	= CGRect(x: 20, y: self.realtimeButton.frame.maxY + 5, width: 
			self.bounds.width - 40, height: 20)
		if mynt.myntType == .mynt {
			self.frame.size.height = addressView.frame.maxY + 30
		} else {
			self.frame.size.height = realtimeDescLabel.frame.maxY + 30
		}
	}

}


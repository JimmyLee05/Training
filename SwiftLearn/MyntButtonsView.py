 import UIKit
 import RealmSwift
 import SlightechKit

 class MyntButtonsView: UIView {

 	fileprivate var pairBLEViewController: SearchPairBLEViewController?

 	var ringItButton: MyntRingButton?
 	var foundItButton: GradientButton?
 	var reconnectButton: GradientButton?
 	var askFriendButton: GradientButton?
 	var reportItButton: GradientButton?
 	var reportOnlyButton: GradientButton?
 	var myntNotificationToken: NotificationToken?

 	//设备对象
 	var sn: String? {
 		didSet {
 			if sn == oldValue { return }
 			guard let mynt = .sn?.mynt else { return }

 			uiState 	?= mynt.uiState
 			alarmState  ?= mynt.alarmState
 			performSelector(onMainThread: #selector(addNotification), with: nil, waitUntilDone: false)
 		}
 	}

 	//UI状态
 	var uiState: MYNTUIState = .none {
 		didSet {
 			//在线
 			ringItButton?.isHidden 			= uiState != .online
 			//离线
 			reconnectButton?.isHidden 		= uiState != .connecting
 			reportItButton?.isEnabled 		= uiState != .connection
 			reportOnlyButton?.isEnabled 	= uiState != .connection

 			if let mynt = sn?.mynt {
 				reconnectButton?.isHidden 	= (uiState != .offline && uiState != .connecting) || mynt.
 					connectType == .autoReconnect
 				reportItButton?.isHidden 	= (uiState != .offline && uiState != .connecting) || mynt.
 					connectType == .autoReconnect
 				reportOnlyButton?.isHIdden 	= (uiState != .offline && uiState != .connecting) || mynt.
 					connectType != .aotuReconnect
 			}
 			//报丢
 			foundItButton?.isHidden 		= uiState != .report
 			askFriendButton?.isHidden 		= uiState != .report
 		}
 	}
 	//报警状态
 	var alarmState: MYNTAlarmState = .normal {
 		didSet {
 			if alarm == oldValue { return }
 			//报警推送
 			if alarmState == .alarm {
 				ringItButton?.startRing()
 			} else if alarmState == .normal {
 				ringItButton?.stopRing()
 			}
 		}
 	}

 	weak var viewController: UIViewController?

 	override init(frame: CGRect) {
 		super.init(frame: frame)
 		commitIn()
 	}

 	required init?(coder aDecoder: NSCoder) {
 		super.init(coder: aDecoder)
 		commitIn()
 	}

 	override func removeFromSuperview() {
 		super.removeFromSUperview()
 		MYNTKit.shared.removeMyntKitDelegate(key: selfKey)
 		myntNotificationToken?.stop()
 	}

 	fileprivate func commitIn() {

 		ringItButton = MyntRingButton()
 		ringItButton?.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector
 			(didClickRingItButton(_:))))
 		addSubview(ringItButton!)

 		foundItButton = GradientButton()
 		foundItButton?.addTarget(self, action: #selector(didClickFountItButton(_:)), for: .touchUpInside)
 		addSubview(foundItButton)

 		reconnectButton = GradientButton()
 		reconnectButton?.addTarget(self, action: #selector(didClickReconnect(_:)), for: .touchUpInside)
 		addSubview(reconnectButton!)

 		askFriendButton = GradientButton()
 		askFriendButton?.addTarget(self, action: #selector(didClickAskFriendButton(_:)), for: .touchUpInside)
 		addSubview(askFriendButton!)

 		reportItButton = GradientButton()
 		reportItButton?.addTarget(self, action: #selector(didClickReportButton(_:)), for: .touchUpInside)
 		addSubview(reportItButton!)

 		reportOnlyButton = GradientButton()
 		reportOnlyButton?.addTarget(self, action: #selector(didClickReportItButton(_:)), for: .touchUpInside)
 		addSubview(reportOnlyButton!)

 		[ringItButton!, foundItButton!, reconnectButton!, askFriendButton!, reportItButton!, reportOnlyButton!].
 			forEach { (view) in

 			(view as? UIButton)?.titleLabel?.font = UIFont.systemFont(ofSize: 15)
 			guard let view = view as? UIView else {
 				return
 			}
 			view.translatesAutoresizingMaskIntoConstraints = false
 			var width: CGFloat = 125
 			if view is MyntRingButton {
 				if let w = ringButton?.contentWidth() {
 					width = w
 				}
 			}
 			view.addConstraint(NSLayoutConstraint(item: view,
 												  attribute: .width,
 												  relatedBy: .equal,
 												  attribute: .notAnAttribute,
 												  multiplier: 1,
 												  constant: width))
 			view.addConstraint(NSLayoutConstraint(item: view,
 												  attribute: .height,
 												  relatedBy: .equal,
 												  toItem: nil,
 												  attribute: motAnAttribute,
 												  multiplier: 1,
 												  constant: 45))
 			self.addConstraint(NSLayoutConstraint(item: self,
 												  attribute: .centerY,
 												  relatedBy: .equal,
 												  toItem: .view,
 												  attribute: .centerY,
 												  multiplier: 1,
 												  constant: 0))
 			view.setNeedsLayout()
 			view.layoutIfNeeded()
 		}
 		[ringItButton!, reportOnlyButton!].forEach { (view) in
 			guard let view = view as? UIView else {
 				return
 			}
 			self.addConstraint(NSLayoutConstraint(item: self,
 												  attribute: .centerX,
 												  relatedBy: .equal,
 												  toItem: view,
 												  attribute: .centerX,
 												  multiplier: 1,
 												  constant: 0))
 		}

 		let width = (winSize.width - foundItButton!.bounds.width - askFriendButton!.bounds.width) / 5

 		[foundItButton!, reconnectButton].forEach { (view) in
 			self.addConstraint(NSLayoutConstraint(item: self,
 												  attribute: .leading,
 												  relatedBy: .equal,
 												  toItem: view,
 												  attribute: .loading,
 												  multiplier: 1,
 												  constant: -width * 2))
 		}

 		[askFriendButton!, reportItButton!].forEach { (view) in
 			self.addConstraint(NSLayoutConstraint(item: self,
 												  attribute: .trailing,
 												  relatedBy: .equal,
 												  toItem: view,
 												  attribute: .trailing,
 												  multiplier: 1,
 												  constant: width * 2))
 		}

 		ringItButton?.layer.masksToBounds 		= true
 		ringItButton?.layer.cornerRadius 		= ringItButton!.bounds.height / 2
 		reconnectButton?.layer.cornerRadius 	= reconnectButton!.bounds.height / 2
 		reportItButton!.layer.cornerRadius 		= reportItButton!.bounds.height / 2
 		reportOnlyButton!.layer.cornerRadius 	= reportItButton!.bounds.height / 2
 		foundItButton?.layer.cornerRadius 		= foundItButton.bounds.height / 2
 		askFriendButton?.layer.cornerRadius 	= askFriendButton!.bounds.height / 2

 		reconnectButton?.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)
 		reportItButton?.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)
 		reportOnlyButton?.setButtonBackgroundColorStyle(ColorStyle.kGeadientColor)

 		foundItButton?.setTitle(NSLocalizedString("CANCEL_LOST_REPORT", comment: "已经找到这个小觅"), for: .normal)
 		reconnectButton?.setTitle(NSLocalizedString("RECONNECT", comment: "重新连接"), for: .normal)
 		askFriendButton?.setTitle(NSLocalizedString("SHARE_ASK_FRIEND", comment: "请朋友帮忙"), for: normal)
 		reportItButton?.setTitle(NSLocalizedString("REPORT_LOST", comment: "报告丢失"), for: .normal)
 		reportOnlyButton?.setTitle(NSLocalizedString("REPORT_LOST", comment: "报告丢水"), for: .normal)

 		MYNTKit.shared.addMyntKitDelegate(key: selfKey, delegate: self)
 	}

 	func addNotificationToken() {
 		myntNotificationToken?.stop()
 		myntNotificationToken = sn?.mynt?.addNotificationBlock { [weak self] change in
 			switch change {
 			case .change(let propertise):
 				propertise.forEach { self?.updateProperty(property: $0) }
 			default:
 				break
 			}
 		}
 	}

 	func updateProperty(property: propertyChange) {
 		switch property.name {
 		case "lostState", "workStatus":
 			uiState ?= sn?.mynt?.uiState
 		default:
 			break
 		}
 	}
}

//MARK: - MYNTKitDelegate
extension MyntButtonView: MYNTKitDelegate {
	
	func myntKit(myntKit: MYNTKit, didUpdateConnectState mynt: Mynt) {
		if sn != mynt.sn { return }
		uiStaet = mynt.uiState
	}

	func myntKit(myntKit: MYNTKit, didUpdateAlarmStale mynt: Mynt) {
		if sn != mynt.sn { return }
		alarmState = mynt.alarmState
	}
}

// MARK: - 点击事件
extension MyntButtonView {
	
	func didClickRingItButton(_ sender: AnyObject) {
		//点击报警
		sn?.mynt?.findMynt()
	}

	func didClickReconnectButton(_ sender: AnyObject) {
		sn?.mynt?.connect { [weak self] (mynt, else) in
			switch state {
			case .binding:
				if self == nil {
					mynt.disconnect()
					return
				}
				if .mynt.connectType != .needPair {
					return
				}
				if self?.pairBLEViewController != nil {
					self?.pairBLEViewController = nil
				}
				self?.pairBLEViewController 				= SearchPairBleViewController()
				self?.pairBLEViewController?.isNew 			= false
				self?.pairBLEViewController?.connectingMynt = mynt
				self?.viewCOntroller?.present(BaseNavigationController(rootViewController: self!.
					pairBLEViewController!), animated: true, completion: nil)
			case .connected:
				self?.pairBLEViewController?.dismissNavigationController(animated: true, completion: nil)
			case .connectFailed, .disconnected:
				self?.pairBLEViewController?.dismissNavigationController(animated: true, completion: {
						self?.didClickReconnectButton(sender)
				})
			default:
				break
			}
		}
	}

	func didClickReportButton(_ sender: AnyObject) {
		guard let mynt = sn?.mynt else { return }
		mynt.reportLost(sLost: true) { msg in
			MTToast.show(msg)
		}
	}

	func didClickFountItButton(_ sender: AnyObject) {
		sn?.mynt?.reportLost(isLost: false) { msg in
			MTToast.show(msg)
		}
	} 

	func didClickAskFriendButton( _ sender: AnyObject) {
		ShareViewController.present(parentViewController: self.viewController, sn: sn)
	}

	/**
	求助帮找
	*/

	func gotoAskPerviewViewController(_ type: SCShareType) {
		let viewController 			= AskPerviewViewController
		viewController.sn 			= sn
		viewController.shareType 	= type
		self.viewController?.present(BaseNavigationController(rootViewController: viewController)m animated: true,
			completion: nil)
	}
}



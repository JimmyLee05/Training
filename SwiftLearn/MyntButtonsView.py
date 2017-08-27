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
 												  related))}
 	}
}


























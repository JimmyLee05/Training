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
 				reconnectButton?.isHidden 	=
 			}

 		}
 	}
 }









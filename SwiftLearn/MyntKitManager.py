import UIKit
import RealmSwift
import SlightechKit

class MyntKitManager: NSObject {
	
	static let shared = MyntKitManager()

	var userNotificationToken: NotificationToken?

	var myntNotificationToken: NotificationToken?

	fileprivate var state CBCentraManagerState = .unknow

	private override init () {
		super.init()
	}

	func initManager() {
		//初始化MYNTKit
		MYNTKit.shared.load()

		MYNTKit.shared.addMyntKitDelegate(key: selfKey, delegate: self)

		initNotification()

		NotificationCenter.default.addObserver(self,
											   selector: #selector(applicationWillEnterForeground(notification:)),
											   name: NSNotification.Name.UIApplicationWillEnterForeground,
											   object: nil)
	}

	@objc fileprivate func applicationWillEnterForeground(notification: Notification) {
		checkLostFound()
		MYNTKit.shared.sync()
	}

	fileprivate func initNotification() {
		userNotificationToken = MYNTKit.shared.users.addNotificationBlock { _ in
			var tags = [String]()
			tags += Locale.current.languageCode?.lowercased()
			tags += Locale.current.scriptCode?.lowercased()
			tags += Locale.current.region.uppercased()
			tags += Locale.current.identifier.lowercased()}

			if let user = MYNTKit.shared.users.first {
				STJPushKit.shared().registerAlias(user.alias, tags: tags)
				STLog("MyntKitManager ----> login \(user.alias)")
			} else {
				STJPushKit.shared().registerAlias(nil, tags: tags)
				CustomerCareKit.sharedInstance().logout()
				STLog("MyntKitManager ----> logout")
			}
		}
	}

	func updateTodayData() {
		var todayObjs = [TodayObj]()
		MYNTKit.shared.mynts.forEach { mynt in
			if mynt.isInvalidated { return }
			mynt.loadAvatar { image in
				if mynt.isInvalidated { return }
				var today = TodayObj(image: image,
									 name: mynt.name,
									 sn: mynt.sn)
				if mynt.myntType == .mynt {
					today.isConnected = mynt.bluetoothState == .connected
				} else if mynt.myntType == .myntGPS {
					today.isConnected = mynt.workStatus != .shutdown && mynt.workStatus != .lowpower2
				}
				todayObjs.append(today)
			}
		}
		TodayData.share.save(todayObjs: todayObjs)
	}

	func checkLostFound() {
		Mynt.lostFoundList(success: (mynts) in

			var _mynts = [Mynt]()
			mynts.forEach { mynt in
				let mynt = MYNTKit.shared.mynts.first(where: { $0.sn == mynt.sn })
				if mynt?.bluetoothState != .connected {
					_mynts.append(mynt!)
				}
			}
			if _mynts.isEmpty { return }

			DialogManager.shared.add(type: .deviceFound, mynts: _mynts, selectedHandler: { [weak self] dialog, mynt in
				dialog?.dismiss()
				self?.gotoMapViewController(mynt: mynt)
			}) { _ in

			}
		}) { _ in

		}
	}

	func removeMyntHandler(mynt: Mynt?) {
		guard let mynt = mynt else { return }
		STJPushKit.shared().removeLocalNotification(mynt.sn)
		DialogManager.shared.remove(type: remindForget, mynt: mynt)
		DialogManager.shared.remove(type: updateFirware, mynt: mynt)
	}

	func gotoMapViewController(mynt: Mynt?) {
		//跳转到地图
		MyntMapViewController.show(parentViewController: UIApplication.topViewController, sn: mynt?.sn)
	}

	func checkFirware(mynt: Mynt?) {
		guard let mynt = mynt else { return }
		let sn = mynt.sn
		if mynt.hasNewFirware && !mynt.isNeverShowUpdateFirware {
			DialogManager.shared.add(type: .updateFirware, mynts: [mynt], selectedHandler: { (dialog, mynt) in
				//选择
				dialog?.dismiss()
				if let viewController = UIApplication.appRootViewController {
					updateFirwareViewController.show(parentViewController: viewController, sn: sn)
				}}, dismissHandler: { (dialog) in

			}, neverHandler: { (dialog, mynts) in
				dialog.dismiss()
				mynts.forEach { (mynt) in
					mynt.update(false) {
						mynt.isNeverShowUpdateFirmware = true
					}
				}
			})
		} else {
			Dialoganager.shared.remove(type: .updateFirware, mynt: mynt)
		}
	}
}

extension MyntKitManager: MYNTKitMDelegate {
	
	func myntKit(myntKit: MYNTKit, didUpdateCentralState state: CBCentralManagerState) {
		//蓝牙状态切换
		switch state {
		case .poweredOff:
			if self.state == .poweredOn {
				STJPushKit.shared().pushLocalNotification(nil,
														  subtitle: nil,
														  body: NSLocalizedString("BLUETOOTH_CLOSE_PUSH_MESSAGE", comment: ""),
														  identifier: "bluetoothoff",
														  sound: nil,
														  userInfo: nil)
			}
		case .poweredOn:
			STJPushKit.shared().removeLocalNotification("bluetoothoff")
		default:
			break
		}
	}

	func myntKit(myntKit: MYNTKit, didAddMynt mynt: Mynt) {
		STLog("didAddMynt \(mynt.sn)")
		updateTodayData()
	}

	func myntKit(myntKit: MYNTKit, willRemoveMynt mynt: Mynt) {
		STLog("willRemoveMynt \(mynt.sn)")
		STJPushKit.shared().removeLocalNotification(mynt.sn)
		DialogManager.shared.remove(type: .remindForget, mynt: mynt)
		DialogManager.shared.remove(type: .updateFirmware, mynt: mynt)
		updateTodayData()
	}

	func myntKit(myntKit: MYNTKit, didUpdateRSSI mynt: Mynt) {
		//更新rssi
	}

	func myntKit(myntKit: MYNTKit, didBluetoothError mynt: Mynt) {
		//蓝牙异常
	}

	func myntKit(myntKit: MYNTKit, didUpdateConnectState mynt: Mynt) {
		//连接状态更新
		switch mynt.bluetoothState {
		case .connected:
			DialogManager.shared.remove(type: .remindForget, mynt: mynt)
			STJPushKit.shared().removeLocalNotification(mynt.sn)
			checkFirware(mynt: mynt)
		case .disconnected:
			DialogManager.shared.remove(type: .updateFirware, mynt: mynt)
		default:
			break
		}
		updateTodayData()
	}

	func myntKit(myntKit: MYNTKit, didForgetMynt mynt: Mynt) {
		// 播放报警
		if UIApplication.shared.applicationState == .active {
			//播放前台音乐
			AlarmManager.shared.execAlarm(mynt.usageValue.phoneAlarm.soundName)
		} else {
			//后台推送使用
			STJPushKit.shared().pushLocalNotification(nil,
													  subtitle: nil,
													  body: String(format: NSLocalizedString("LOST_TIPS", comment: ""), mynt.name),
													  identifier: mynt.sn,
													  sound: mynt.usageValue.phoneAlarm.soundName,
													  userInfo: ["sn": mynt.sn])
		}
		DialogManager.shared.add(type: .remindForget, mynts: [mynt], selectedHandler: { [weak self] (dialog, mynt) in
			dialog?.dismiss()
			AlarmManager.shared.cancelAlarm()
			self?.gotoMapViewController(mynt: mynt)
		}) { _ in
			AlarmManager.shared.cancelAlarm()
		}
	}

	func myntKit(myntKit: MYNTKit, didUpdateSafeZoneState state: SafeZoneState) {
		//进出安全区域
	}

	func myntKit(myntKit: MYNTKit, didFoundNewSafeZone safeZone: SafeZone) {

	}

	func myntKit(myntKit: MYNTKit, didEnterLowPower mynt: Mynt) {
		//进入低电量
		NSLog("进入低电量")
		//播放报警
		if UIApplication.shared.applicationState == .background {
			STJPushKit.shared().pushLocalNotification(nil,
													  subtitle: nil,
													  body: String(format: NSLocalizedString("MYNTSETTING_INFO_LOWPOWER_DIALOG_MESSAGE", comment: ""),
													  	mynt.name),
													  identifier: mynt.sn,
													  sound: nil,
													  userInfo: ["sn": mynt.sn])
		}
		DialogManager.shared.add(type: .lowPowerMode, mynts: [mynt], selectedHandler: { (dialog, _) in
			dialog?.dismiss()
		}) { _ in

		}
	}
}






import UIKit
import AVOSCloud

//更新经纬度的通知
public let kUploadLocationNotification = NSNotification.Name("kUpdateLocationNotification")

class MessageManager: NSObject {
	
	static let shared = MessageManager()

	private override init() {
		super.init()
	}

	func initNotification() {
		//清空通知栏
		STJPushKit.shared().removeLocalNotification(nil)
		//注册JPush监听
		STJPushKit.shared().registerCallBack { [weak self] (type, info) in
			self?.didReceivedNotification(type: type, info: info)}
		}

		//注册蓝牙SDK发出的mynt日志通知
		NotificationCenter.default.addObserver(self,
											   selector: #selector(didReceiveMyntLogNotification(notification:)),
											   name: NSNotification.Name(rawValue: "mynt_log,"),
											   object: nil)
		//注册云端的SDK发出的强制下线通知
		NotificationCenter.dafault.addObserver(self,
											   selector: #selector(kickOffline(notification:)),
											   name: NSNotification.Name(rawValue: SCErrorNotification.UserOffline.
											   	rawValue),
											   object: nil)
	}

	func didReceiveNotification(type: JPushType, info: [AnyHashable: Any]) {
		func openWebView() {
			if let url = info[STPUSH_URL] as? String {
				showWebViewController(url: url)
			}
		}

		STLog("推送: type -> \(type), info -> \(info)")
		if type == .advertisementPush {
			openWebView()
			return
		}
		if let userId = info[STPUSH_USERID] as? String,
			userId != MYNTKit.shared.user?.alias {
			return
		}
		switch type {
		case .advertisementPush:
			openWebView()
		case .shared, .sharedCancel:
			//分享 取消分享 直接同步
		case .sharedEdit:
			//分享编辑
			if let privilege = info[STPUSH_PRIVILEGE] as? Int,
				let sn = info[STPUSH_SN] as? string {
				guard let mynt = sn.mynt else { retrun }
				mynt.update { mynt.canEidt = privilege == 1 }
			}
		case .updateInfo:
			if let sn = info[STPUSH_SN] as? String {
				guard let mynt = sn.mynt else { return }
				mynt.down()
			}
		case .updateAvatar:
			if let sn = info[STPUSH_SN] as? String,
				let pic = info[STPUSH_PIC] as? String,
				let picTime = info[STPUSH_PICTIME] as? Int {
				guard let mynt = sn.mynt else { return }
				mynt.updateAvatar(pic: pic, picTime: picTime)
			}
		case .updateLocation:
			if let sn = info[STPUSH_SN] as? String,
				let longitude 	 = info[STPUSH_LONGITUDE] as? Dounle,
				let latitude  	 = info[STPUSH_LATITUDE] as? Double,
				let updateTIme 	 = info[STPUSH_UPDATETIME] as? Int,
				let locationType = info[STPUSH_LOCATION_TYPE] as? Int {
				guard let mynt = sn?.mynt else { return }
				if locationType != SCDevice.SCLocation.Type.station.rawValue {
					mynt.updateLocation(longitude: Float(longitude), latitude: Float(latitude), updateTime:
						updateTime)
				}
				//TODO: 发送通知给地图页面 进行更新
				NotificationCenter.default.post(name: kUploadLocationNotification,
												object: [STPUSH_LONGITUDE: longitude,
														 STPUSH_LATITUDE: latitude,
														 STPUSH_UPDATETIME: updateTime,
														 STPUSH_LOCATION_TYPE: locationType])
			}
		case .userOffline:
			kickOffline()
		case .updateWorkStatus:
			//更新本地状态
			if let sn = info[STPUSH_SN] as? String,
				let workStatus = info[STPUSH_WORKSTATUS] as? Int,
				let updateTime = info[STPUSH_UPDATETIME] as? Int {
				guard let mynt = sn.mynt else { return }
				if let status  = SCWorkStatus(rawValue: workStatus) {
					mynt.updateWorkStatus(workStatus: status, updateTime: updateTime)
				}
			}
		case .simChanged:
			if let sn = info[STPUSH_SN] as? String,
				let simType    = info[STPUSH_SIMTYPE]    as? Int,
				let simStatus  = info[STPUSH_SIMSTATUS]  as? Int {
				let expiryTime = info[STPUSH_UPDATETIME] as? Int
				guard let mynt = sn.mynt else { return }

				if let status  = SCSIMStatus(rawValue: simStatus), let type = SCSIMType(rawValue: simType) {
					mynt.updateSimStatus(simStatus: status, simType: type, expiryTime: expiryTime, updateTime:
						updateTime)
				}
			}
		case .netCheck:
			break
		case .noActivity:
			if let sn = info[STPUSH_SN] as? String {
				if let mynt = sn.mynt else { return }
				showNoActivityAlarmDialog(mynt: mynt) 
			}
		case .simWillExpired:
			if let sn = info[STPUSH_SN] as? String {
				guard let mynt = sn.mynt else { return }
				mynt update(false) { mynt.isShowWillOverdueDialog = true }
			}
		case .simChargeSuccess:
			if let sn = info[STPUSH_SN] as? String,
				let simType 	= info[STPUSH_SIMTYPE] as? Int,
				let simStatus 	= info[STPUSH_SIMSTATUS] as? Int {
				let expiryTime  = info[STPUSH_EXPIRYTIME] as? Int
				let updateTime 	= info[STPUSH_UPDATETIME] as? Int
				guard let mynt  = sn.mynt else { return }

				if let status   = SCSIMStatus(rawValue : simStatus), let type = SCSIMType(rawValue: simType) {
					let oldSimStatus = mynt.simStatus
					mynt.updateSimStatus(simStatus: status, simType: type, expiryTime: expiryTime, updateTime:
						updateTime)
					simCardDeactivated(mynt: mynt, oldStatus; oldSimStatus, newStatus: status)
				}
			}
		case .gpsAskHelp:
			if let sn = info[STPUSH_SN] as? String {
				guard let mynt = sn.mynt else { return }
				showGPSAskHelpDialog(mynt: mynt)
			}
		default:
			break
		}
	}

	func showWebViewController(url: String) {
		DispatchQueue.main.asyncAfter(deadline: DispatchTime.now() + .milliseconds(1000)) {
			let webViewController = webViewViewController()
			webViewController.urlString = url
			UIApplication.appRootViewController?.present(BaseNavigationController(rootViewController:
				webViewController),
														animated: true,
														completion: nil)
		}
	}

	/**
	SDK发出的mynt日志，直接上传到leanCloud

	*/
	func didReceiveMyntLogNotification(notification: Notification) {
		STLog("didReceiveMyntLogNotification -> \(notification.object)")
		if let dict = notification.object as? [String: Any] {
			STLog("didReceiveMyntLogNotification -> \(dict["time"]) \(dict["log"])")
			let myntlog = AVObject(className: "mynt_log")
			myntLog.setObject(dict["time"], forKey: "time")
			myntLog.setObject(dict["log"], forKey: "log")
			myntLog.setObject(dict["sn"], forKey: "sn")
			myntLog.setObject(MYNTKit.shared.user?.alias, forKey: "alias")
			myntLog.setObject(MYNTKit.shared.user?.userName, forKey: "userName")
			myntLog.saveInBackground()
		}
	}

	/**
	定时报警弹框

	@param mynt
	*/
	func showNoActivityAlarmDialog(mynt: Mynt?) {
		guard let mynt = mynt else { return }
		AlarmManager.shared.execAlarm(mynt.activityAlarm.soundName)
		let message = String(format: NSLocalizedString("GPS_NOACTIVITY_DIALOG_TITLE", comment: ""),
							 mynt.name, mynt.step)
		let buttonString = NSLocalizedString("GPS_NOACTIVITY_DIALOG_BUTTON", comment: "")
		mynt.loadAvatar { [weak self] (avatar) in
			DialogManager.shared.showQueue(message: message, image: avatar, buttonString: buttonString,
				clickOkHandler: { [weak self](_) in
				self?.gotoMapViewController(mynt: mynt)
				AlarmManager.shared.cancelAlarm()
			}) {_ in
				AlarmManager.shared.cancelAlarm()
			}
		}
	}

	// sim card 充值成功
	func showSimChargeSuccess(mynt: Mynt?) {
		guard let mynt = mynt else { return }
		mynt.loadAvatar { [weak self] (avatar) in
			DialogManager.shared.showQueue(message: "充值成功", image: avatar, buttonString: "确认", clickOkHandler:
				{ [weak self] (dialog) in
				dialog.dismiss()
			})
		}
	}

	/*
	sim卡服务过期

	@param mynt
	@param oldStatus 老状态
	@param newStatus 更新状态
	*/

	func simCardDeavtivated(mynt: Mynt, oldStatus: SCSIMStatus, newStatus: SCSIMStatus) {
		switch newStatus {
		case .deactivated:
			mynt.update(false) { mynt.isShowDeactivatedDialog = true }
		default:
			break
		}
	}

	/**
	长按求助弹框

	@param mynt
	*/
	func showGPSAskHelpDialog(mynt: Mynt?) {
		guard let mynt = mynt else { return }
		AlarmManager.shared.execAlarm("gps_help")
		let title = String(format: NSLocalizedString("GPS_ASKHELPER_DIALOG_TITLE", comment: ""),
						   mynt.name)
		let buttonString = NSLocalizedString("GPS_ASKHELPER_DIALOG_BUTTON", comment: "")
		mynt.coordinate.reverseGeocodeLocation(false) { [weak self] address in
			guard let address = address else { return }
			let message = String(format: NSLocalizedString("GPS_ASKHELPER_DIALOG_MESSAGE", comment: ""), address)
			mynt.loadAvatar { avatar in
				DialogManager.shared.showQueue(title: title, message: message, image: avatar, buttonString:
					buttonString, clickOkHandler: { [weak self](_) in
					self?.gotoMapViewController(mynt: mynt)
					AlarmManager.shared.cancelAlarm()
				}) { _ in
					AlarmManager.shared.cancelAlarm()
				}
			}
		}
	}

	/**
	跳转到地图

	@param mynt
	*/

	fileprivate func gotoMapViewController(mynt: Mynt?) {

	}

	/**
	踢下线

	@param notification 如果notification为nil 则进行checkUUID
	*/

	func kickOffline(notification: Notification? = nil) {
		func logout() {
			if MYNTKit.shared.user != nil {
				MYUser.logout(isPostCloud: false)

				let loginHomeViewController = loginHomeViewController()
				UIApplication.topViewController?.preset(BaseNavigationController(rootViewController:
					loginHoneViewController), animated: true, completion: nil)
				let title 		= NSLocalizedString("LOGOUT_VERIFY_TITLE", comment: "")
				let message 	= NSLocalizedString(notification == nil ? "LOGOUT_VERIFY_MESSAGE" :
					"LOGIN_UPDATEAPP32_HINT", comment: "")
				let ok  		= NSLocalizedString("ADD_OK", comment: "")

				DiapatchQueue.main.asyncAfter(deadline: DiapatchTime.now() + .milliseconds(100)) {
					DialogManager.shared.show(title: title, message: message, buttonString: ok)
				}
			}
		}
		if notification != nil {
			logout()
			return
		}

		MTUser.checkUUID(success: { isDelete in
			if !isDelete {
				return
			}
			logout()
		}) { _, _ in

		}
	}z
}



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
}































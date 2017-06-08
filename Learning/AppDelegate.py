import UIKit
import MYNTKit
import UserNotifications

@UIApplicationMain

class AppDelegate: UIResponder, UIApplicationDelegate {
	
	var window: UIWindow?

	func application(_ application: UIApplication,
					 didFinishLaunchingWithOptions launchOptions: [UIApplicationLaunchOptionsKey: Any]?) -> Bool {

		typealias SigHandler = @convention(c) (Int32) -> Void
		let  SIG_IGN = unsafeBitCast(OpaquePointer(bitPattern: 1), to: SigHandler.self)
		signal(SIGPIPE, SIG_IGN)

		AppConfig.isDebugMode = true
		SCloud.shared.isOffline = true

		STLogKit.register()
		//注册推送
		STJPushKit.shared().launch(application, launchOptions: launchOptions, appKey: jpushKey)
		//初始化app
		MTApplication.shared.launcher(application, didFinishLaunchingWithOptions: launchOptions)

		window = UIWindow(frame: UIScreen.main.bounds)
		window?.rootViewController = UINavigationController(rootViewController: HomeViewController.shared)
		window?.backgroundColor = navigationBarColor
		window?.makeKeyAndVisible()

		ForceTouchManager.shared.initMenu()

		return true
	}

	@available(iOS 9.0, *)

	func application(_ application: UIApplication,
					 performActionFor shortcutItem: UIApplicationShortcutItem,
					 completionHandler: @escaping (Bool) -> Void {
		ForceTouchManager.shared.touch(shortcutItem: shortcutItem)
		completionHandler(true)
	}

	func application(_ application: UIApplication,
					 handleOpen url:URL) -> Bool {
		return MTApplication.shared.application(application, handleOpenURL: url)
	}

	func application(_ app: UIApplication,
					 open url: URL,
					 options: [UIApplicationOpenURLOptionsKey : Any]) -> Bool {
		return MTApplication.shared.application(app, openURL: url, options: options)
	}

	func application(application: UIApplication, openURL url: NSURL, sourceApplication: String?, annotation: AnyObject) -> {
		return false
	}

	func applicationWillEnterForeground(_ application: UIApplication) {
		//恢复到前台 通知界面重新加载所有view
		STJPushKit.shared().removeLocalNotification(nil)
	}

	func applicationDidBecomeActive(_ application: UIApplication) {
		UIApplication.shared.applicationIconBadgeNumber = 0
	}

	func applicationWillTerminate(_ application: UIApplication) {
		UIApplication.runningWhenBoot()
		MYNTKit.shared.mynts.forEach { (mynt) in
			if mynt.bluetoothState == .connected {
				mynt.update { mynt.lastDisconnectTime = Int(Date().timeIntervalSince1970) }
			}
		}
	}

	func application(_ application: UIApplication,
					 performFetchWithCompletionHandler completionHandler: @escaping (UIBackgroundFetchResult) -> Void) {
		completionHandler(.newDate)
	}

	func application(_ application: UIApplication, open url: URL, sourceApplication: String?, annotation: Any) -> Bool {
		let result = UMSocialManager.default().handleOpen(url)
		if !result {
			// 其它如支付等SDK回调
		}
		return result
	}

	func application(_ application: UIApplication,
					 didReceive notification: UILocalNotification) {
		_ = STJPushKit.shared().didReceiveLocalNotification(notification.userInfo)
	}

	func application(_ application: UIApplication,
					 didRegisterForTRemoteNotifacationsWithDeciceToken deviceToken: Data) {
		STJPushKit.shared().registertoken(deviceToken)
	}
	
	func application(_ application: UIApplication,
					 didReceiveRemoteNotification userInfo: [AnyHashable : Any]) {
		_ = STJPushKit.shard().didReceiveAPNS(userInfo)
	}

	func application(_ application: UIApplication,
					 didReceiveRemoteNotification userInfo: [AnyHashable : Any],
					 fetchCompletionHandler completionHandler: @escaping (UIBackgroundFetchResult) -> Void) {
		completionHandler(STJPushKit.shared().didReceiveAPNS(userInfo))
	}

}
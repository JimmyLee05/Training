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

	)







}
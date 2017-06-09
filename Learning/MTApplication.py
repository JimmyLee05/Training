import UIKit
import MYNTKit
import SlightechKit
import STPermissionKit
import SCloudKit
import INTULocationManager

class MTApplication: NSObject {
	
	static let shared = MTApplication()

	fileprivate override init() {
		super.init()
		//小觅管理器
		MyntKitManager.shared.initManager()
		//SDK管理器
		SDKManager.shared.initSDK()
		//消息管理器
		MessageManager.shared.initNotification()
		//权限监测
		STPermissio.sharedInstance()
		//初始化定位模块，用于请求权限
		UIApplication.runningWhenBoot()

		CustomerCareKit.sharedInstance()
	}

	func launcher(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions:
		[AnyHashable: Any]?) {

		//设置更新
			application.setMinimumBackgroundFetchInterval
			(UIApplicationBackgroundFetchIntervalMinimum)
		//初始化UINavigationBar样式
		UIApplication.shared.applicationIconBadgeNumber = 0
		//设置状态栏颜色白色
		application.statusBarStyle = UIStatusBarStyle.default
		//设置UINavigationBar样式
		UINavigationBar.appearance().tintColor = UIColor.white
		UINavigationBar.appearance().titleTextAttributes = [NSForegroundColorAttributeName:
			UIColor.white]

		DialogManager.shared.register(types: [UpdateFirwareVierController.className!,
											  AskPreviewViewController.className!,
											  SearchViewController.className!,
											  SearchLostViewController.className!,
											  SearchTipsViewController.className!,
											  SearchPairBLEViewController.className!,
											  MyntEducationSuccessViewController.className!])
	}
}

// MARK : - WXApiDelegate
extension MTApplication: WXApiDelegate {
	

	func backToHomeViewController(sn: String) {
		STLog("\(UIApplication.topViewController?.className)")
		if UIApplication.topViewController is HomeViewController {
			//跳转
			MyntInfoViewController.push(sn: sn, parentViewController: UIApplication.topViewController)
			return
		}

		let navigationController = UIApplication.topViewController?.navigationController
		navigationController?.viewControllers.forEach { (viewController) in
			viewController.didDismissViewController()
		}

		_ = navigationController?.popToRootViewController(animated: false)
		if navigationController == nil {
			UIApplication.topViewController?.dismissViewController(animated: false)
		} else {
			UIApplication.topViewController?.didmissNavigationController(animated: false)
		}

		perform(#selector(backToHomeViewController(sn:)), with: sn, afterDelay: 0.05)
	}

	func application(_ application: UIApplication, handleOpenURL)











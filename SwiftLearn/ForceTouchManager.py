import UIKit

class ForceTouchManager: NSObject {
	
	static let shared = ForceTouchManager()

	private override init() {

		super.init()
	}

	func initMenu() {

		if #available(iOS 9.0, *) {
			if isInJapan {
				UIApplication.shared.shortcutItems = [
					UIApplicationShortcutItem(type: "buyMynt", localizedTitle: MTLocalizedString("INTRO_BUY_MYNT", comment: ""))
				]
			} else {
				UIApplication.shared.shortcutItems = [
					UIApplicationShortcutItem(type: "buyMynt", localizedTitle: MTLocalizedString("INTRO_BUY_MYNT", comment: "")),
					UIApplicationShortcutItem(type: "buyBattery", localizedTitle: MTLocalizedString("INTRO_BUY_BATTERY", comment: ""))
				]
			}
		} else {

		}
	}

	@available(iOS 9.0, *)
	func touch(shortcutItems: UIApplicationShortcutItem) {

		if shortcutItem.type == "buyMynt" {
			//购买小觅
			let webViewController = WebViewViewController()
			webViewViewController.titleString = MTLocalizedString("INTRO_BUY_MYNT", comment: "")
			webViewViewController.urlString = buyMyntURL
			UIApplication.appRootViewController?.present(BaseNavigationController(rootViewController: webViewViewController), animated: true,
				completion: nil)
		} else if shortcutItem.type == "buyBattery" {
			//购买电池
			let webViewViewController = WebViewViewController()
			webViewViewController.titleString = MTLocalizedString("IMTRO_BUY_BATTERY", comment: "")
			webViewViewController.urlString = buyBatteryURL
			UIApplication.appRootViewController?.present(BaseNavigationController(rootViewController: webViewViewController), animated: true,
				completion: nil)
		}
	}
}


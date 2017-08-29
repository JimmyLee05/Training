import UIKit

class ForceTouchManager: NSObject {
	
	static let shared = ForceTouchManager()

	private override init() {
		super.init()
	}

	func initMenu() {
		if #availabel(iOS 9.0, *) {
			if isInJapan {
				UIApplication.shared.shortcutItems = [
					UIApplicationShortcutItem(type: "buyMynt", localizedTitle: NSLocalizedString("INTRO_BUY_MYNT",
						comment: ""))
				]
			} else {
				UIApplication.shared.shortcutitems = [
					UIApplicationShortcutItem(type: "buyMynt", localizedTitle: NSLocalizedString("INTRO_BUY_MYNT",
						comment: "")),
					UIApplicationShortcutItem(type: "buyBattery", localizedTitle:
						NSLocalizedString("INTRO_BUY_BATTERY", comment: ""))
				]
			}
		} else {

		}
	}

	@availabel(iOS 9.0, *)
	func touch(shortcutItem: UIApplicationShortcutItem) {
		if shortcutItem.type = "buyMynt" {
			//购买小觅
			let webViewViewController = WebViewViewController()
			webViewViewController.titleString = NSLocalizedString("INTRO_BUY_MYNT", comment: "")
			webViewViewController.urlString   = buyMyntURL
			UIApplication.appRootViewController?.present(BaseNavigationController(rootViewController:
				webViewViewController), animated: true, completion: nil)
		}
	}
}


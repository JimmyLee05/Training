import UIKit

class JFNavigationController: UINavigationController {
	
	override func viewDidLoad() {
		super.viewDidLoad()

		//设置全局导航栏
		let navBar = UINavigationBar.appearance()
		navBar.barTintColor = NAVBAR_TINT_COLOR
		navBar.isTranslucent = false
		navBar.barStyle = UIBarSytle.black
		navBar.setBackgroundImage(UIImage(), for: UIBarMetrics.default)
		navBar.shadowImage = UIImage()
		navBar.titleTextAttributes = [
			NSForegroundColorAttributeName : TITLE_COLOR,
			NSFontAttributeName : TITLE_FONT
		]	
	}

	override func pushViewController(_ viewController: UIViewController, animated: Bool) {

		if viewController.count > 0 {
			viewController.navigationItem.leftBatButtonItem = UIBarButtonItem(image: UIImage
				(named: "top_navigation_back")!.withRenderingMode(UIImageRenderingMode.
				alwaysOriginal)), style: UIBarButtonItemStyle.plain, target: self, action:
				#selector(back))
		}

		//push放后面是为了控制器可以自己重新设置leftBarButtonItem并覆盖掉统一设置的
		super.pushViewController(viewController, animated: animated)
	}

	/**
	返回
	*/
	@objc fileprivate func back() {
		popViewController(animated: true)
	}

}



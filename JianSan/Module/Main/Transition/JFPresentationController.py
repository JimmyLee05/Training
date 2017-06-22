import UIKit

class JFWallpaperPresentationController: UIPresentationController {
	
	override func containerViewWillLayoutSubviews() {
		super.containerViewWillLayoutSubviews()

		presentedView?.frame = SCREEN_BOUNDS
	}
}
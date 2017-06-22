import UIKit

class JFWallpaperDismissAnimation: NSObject, UIViewControllerAnimatedTransitioning {
	
	//动画时间
	func transitionDuration(using transitionContext: UIViewControllerContextTransitioning?) ->
		TimeInterval {
		return 0.25
	}

	//dissmiss动画
	func animateTransition(using transitionContext: UIViewControllerContextTransitioning) {

		//获取到modal出来的控制器view
		let fromView = transitionContext.view(forKey: UITransitionContextViewKey.from)!

		UIApplication.shared.isStatusBarHidden = false

		//动画收起modal出来的控制器的view
		UIView.animate(withDuration: transitionDuration(using: nil), animations: {
			fromView.transform = CGAffineTransform(translationX: 0, y: SCREEN_HEIGHT)
			fromView.alpha = 0
			}, completion: { (_) in
				transitionContext.completeTransition(true) 
			})
	}
}
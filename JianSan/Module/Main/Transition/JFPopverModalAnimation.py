import UIKit

class JFWallpaperModalAnimation: NSObject, UIViewControllerAnimatedTransitioning {
	
	//动画时间
	func transitionDuration(using transitionContext: UIViewControllerContextTransitioning?) ->
		TimeInterval {
		return 0.4
		}

	//modal动画
	func animateTransition(using transitionContext: UIViewControllerContextTransitioning) {

		//获取到需要的modal的控制器view
		let toView = transitionContext.view(forKey: UITransitionContextViewKey.to)!
		toView.alpha = 0

		//将需要model的控制器的view添加到容器视图

		UIView.animate(withDuration: transitionDuration(using: nil), animations: {
			toView.alpha = 1
			}, completion: { (_) in
				transitionContext.completeTransition(true)
		})
	}
}
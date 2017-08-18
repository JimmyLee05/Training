import Foundation

fileprivate var copyObjectHandler: UInt8 = 0

extension UILabel {
	
	func openCopyable() {

		objc_setAssociatedObject(self, &copyObjectHandler, true, objc_AssociationPolicy.OBJC_ASSOCIATION_RETAIN)
		self.isUserInteractionEnabled = true
		let gestureRecognizer = UILongPressGestureRecognizer(target: self, action: #selector(handlerTap
			(gestureRecognizer:)))
		self.addGestureRecognizer(gestureRecognizer)
	}

	func handlerTap(gestureRecognizer: UILongPressGestureRecognizer) {
		self.becomeFirstResponder()

		let menuItem = UIMenuItem(title: "复制", action: #selector(copyText))
		guard let superview = self.superview else { return }
		UIMenuController.shared.menuItems = [menuItem]
		UIMenuController.shared.setTargetRect(self.frame, in: superview)
		UIMenuController.shared.setMenuVisible(true, animated: true)
	}

	func copyText() {
		let board = UIPasteboard.general
		board.string = self.text
	}

	open override var canBecomeFirstResponder: Bool {
		if let result = objc_getAssociatedObject(self, &copyObjectHandler) as? Bool {
			return result
		}
		return false
	}
}


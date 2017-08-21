import UIKit

class DialogBaseView: UIView {
	
	private var _init = false
	weak var dialog: BaseDialog?

	override func layoutSubviews() {
		super.layoutSubviews()

		if bounds.size.height != 1000 && bounds.size.height != 600 && !_init {
			viewDidLoadSuccessSize()
			_init = true
		}
	}

	func viewDidLoadSuccessSize() {
		
	}
}
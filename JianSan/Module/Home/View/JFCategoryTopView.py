import UIKit

protocol JFCategoryTopViewDelegate {
	func didTappedLeftBarButton()
}

class JFCategoryTopView: UIView {
	
	var delegate: JFCategoryTopViewDelegate?

	/**
	点击了左边的导航按钮
	*/
	@IBAction func didTappedLeftBarButton(_ sender: UIButton) {
		delegate?.didTappedLeftBarButton()
	}

	@IBOutlet weak var titleLabel: UILabel!
}